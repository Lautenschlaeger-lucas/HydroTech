"""Endpoints públicos do simulador, no mesmo serviço Django existente."""
import asyncio
import logging
import re

from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from . import config
from .roteamento import RotaIndisponivel
from .servico import SemRiscoNaOrigem, filtrar_alertas, planejar_fuga
from .zonas import carregar_zonas

IDS_DE_ALERTA = re.compile(r"^\d+(,\d+)*$")
logger = logging.getLogger(__name__)


def _alertas(request):
    valor = request.GET.get("alerta")
    if valor is None:
        return None
    if not IDS_DE_ALERTA.fullmatch(valor):
        raise ValueError("alerta deve conter IDs numéricos separados por vírgula")
    return {int(item) for item in valor.split(",")}


def _coordenada(request, nome, minimo, maximo):
    try:
        valor = float(request.GET[nome])
    except (KeyError, ValueError):
        raise ValueError(f"{nome} deve ser um número entre {minimo} e {maximo}") from None
    if not minimo <= valor <= maximo:
        raise ValueError(f"{nome} deve ser um número entre {minimo} e {maximo}")
    return valor


@require_GET
def rota_fuga(request):
    try:
        lat = _coordenada(request, "lat", -90, 90)
        lng = _coordenada(request, "lng", -180, 180)
        modo = request.GET.get("modo", "pe")
        if modo not in ("pe", "carro"):
            raise ValueError("modo deve ser pe ou carro")
        alertas = _alertas(request)
    except ValueError as erro:
        return JsonResponse({"detail": str(erro)}, status=400)

    async def calcular():
        return await asyncio.wait_for(
            planejar_fuga(lat, lng, modo, alertas),
            timeout=config.TIMEOUT_PEDIDO_S,
        )

    try:
        return JsonResponse(async_to_sync(calcular)())
    except SemRiscoNaOrigem as erro:
        return JsonResponse({"detail": str(erro)}, status=422)
    except RotaIndisponivel as erro:
        return JsonResponse({"detail": str(erro)}, status=503)
    except asyncio.TimeoutError:
        return JsonResponse({"detail": "Os serviços de mapa estão lentos demais agora. Siga as orientações da Defesa Civil."}, status=503)


@require_GET
def zonas_risco(request):
    try:
        alertas = _alertas(request)
        atualizar = request.GET.get("atualizar", "false").lower()
        if atualizar not in ("true", "false", "1", "0"):
            raise ValueError("atualizar deve ser true ou false")
    except ValueError as erro:
        return JsonResponse({"detail": str(erro)}, status=400)

    try:
        zonas = async_to_sync(carregar_zonas)(forcar=atualizar in ("true", "1"))
    except Exception:
        logger.exception("Falha ao consultar pontos de risco para o simulador")
        return JsonResponse({"detail": "Não foi possível consultar os pontos de risco."}, status=502)
    return JsonResponse(filtrar_alertas(zonas, alertas)[0], safe=False)


@require_GET
def status(request):
    return JsonResponse({
        "servico": "hydrotech-rotas-integrado",
        "desvio_de_zonas": "openrouteservice" if config.ORS_API_KEY else "desativado (OSRM)",
        "raio_zona_risco_m": config.RAIO_ZONA_RISCO_M,
    })
