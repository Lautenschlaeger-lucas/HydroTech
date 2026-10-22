"""Pontos de risco diretamente do banco usado pelo Django."""
import time

from asgiref.sync import sync_to_async

from rios.models import PontoRisco

from . import config

_cache = {"quando": 0.0, "zonas": None}


def _buscar_zonas(forcar=False):
    agora = time.monotonic()
    if (not forcar and _cache["zonas"] is not None
            and agora - _cache["quando"] < config.CACHE_ZONAS_S):
        return _cache["zonas"]

    zonas = [
        {
            "id": ponto.id,
            "descricao": ponto.descricao,
            "rio": ponto.rio.nome,
            "cidade": ponto.rio.cidade,
            "lat": ponto.latitude,
            "lng": ponto.longitude,
            "raio_m": config.RAIO_ZONA_RISCO_M,
        }
        for ponto in PontoRisco.objects.select_related("rio").all()
    ]
    _cache.update(quando=agora, zonas=zonas)
    return zonas


async def carregar_zonas(forcar=False):
    """Mantém a interface assíncrona esperada pelo cálculo de rotas."""
    return await sync_to_async(_buscar_zonas, thread_sensitive=True)(forcar)
