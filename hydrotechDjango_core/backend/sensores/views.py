import logging
import os
import json
from math import radians, sin, cos, asin, sqrt

from django.conf import settings
from django.utils import timezone
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Sensor, SensorGroup, Leitura
from .serializers import (
    SensorSerializer,
    SensorGroupSerializer,
    LeituraSerializer,
)
from usuarios.authentication import JWTOrAPITokenAuthentication
from usuarios.permissions import IsDefesaCivilOrAdmin
from rios.models import PontoRisco
from .previsao import prever_sensor
from .simulacao import classificar_cenario_simulado, preparar_sensor_simulado
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class SensoresPermission(IsDefesaCivilOrAdmin):
    """
    Leitura para qualquer usuário autenticado;
    escrita (criar/editar/deletar) apenas para Defesa Civil + Admin.
    """

    def has_permission(self, request, view):
        if not getattr(request.user, 'is_authenticated', False):
            return False
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return super().has_permission(request, view)
        return True


# ---------------------------------------------------------------------------
# Sensores (folhas do Composite)
# ---------------------------------------------------------------------------

class SensorListCreateView(generics.ListCreateAPIView):
    serializer_class = SensorSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return Sensor.objects.select_related('grupo', 'rio').order_by('-id')

    def perform_create(self, serializer):
        serializer.save()
        logger.info(
            f'Sensor criado: {serializer.instance.nome} '
            f'(tipo={serializer.instance.tipo})'
        )


class SensorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return Sensor.objects.select_related('grupo', 'rio')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Sensor atualizado: {serializer.instance.nome}')

    def perform_destroy(self, instance):
        nome = instance.nome
        instance.delete()
        logger.info(f'Sensor deletado: {nome}')


# ---------------------------------------------------------------------------
# Grupos de sensores (composites do padrão Composite)
# ---------------------------------------------------------------------------

class SensorGroupListCreateView(generics.ListCreateAPIView):
    serializer_class = SensorGroupSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return SensorGroup.objects.prefetch_related(
            'sensores', 'subgrupos'
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Grupo de sensores criado: {serializer.instance.nome}')


class SensorGroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorGroupSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return SensorGroup.objects.prefetch_related(
            'sensores', 'subgrupos'
        )

    def perform_update(self, serializer):
        parent = serializer.validated_data.get('parent')
        if parent and parent == serializer.instance:
            raise serializers.ValidationError(
                {'parent': 'Um grupo não pode ser pai de si mesmo.'}
            )
        serializer.save()
        logger.info(f'Grupo de sensores atualizado: {serializer.instance.nome}')

    def perform_destroy(self, instance):
        nome = instance.nome
        instance.delete()
        logger.info(f'Grupo de sensores deletado: {nome}')


# ---------------------------------------------------------------------------
# Leitura (medição de um sensor folha)
# ---------------------------------------------------------------------------

class LeituraListCreateView(generics.ListCreateAPIView):
    serializer_class = LeituraSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs.get('sensor_id')
        return Leitura.objects.filter(sensor_id=sensor_id)

    def perform_create(self, serializer):
        sensor_id = self.kwargs.get('sensor_id')
        serializer.save(sensor_id=sensor_id)
        logger.info(f'Leitura registrada para o sensor {sensor_id}')


class LeituraRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = LeituraSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return Leitura.objects.all()


class PrevisaoPontoRiscoView(APIView):
    """Previsão restrita à Defesa Civil/Admin, com demonstração resiliente."""
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilOrAdmin]

    def post(self, request, ponto_id):
        from datetime import timedelta

        ponto = PontoRisco.objects.select_related('rio').get(pk=ponto_id)
        simulado = settings.DEBUG

        if simulado:
            sensor = preparar_sensor_simulado(ponto)
            classificacao_local = classificar_cenario_simulado(ponto)
            distancia = 0.0
        else:
            sensores = Sensor.objects.filter(
                rio_id=ponto.rio_id,
                tipo='nivel_agua',
                status='ativo',
            )
            candidatos = []
            for candidato in sensores:
                if candidato.latitude is None or candidato.longitude is None:
                    continue
                dlat = radians(candidato.latitude - ponto.latitude)
                dlon = radians(candidato.longitude - ponto.longitude)
                a = sin(dlat / 2) ** 2 + cos(radians(ponto.latitude)) * cos(radians(candidato.latitude)) * sin(dlon / 2) ** 2
                km = 6371 * 2 * asin(sqrt(a))
                ultima_leitura = candidato.leituras.order_by('-criado_em').first()
                if ultima_leitura and ultima_leitura.criado_em >= timezone.now() - timedelta(minutes=30):
                    candidatos.append((km, candidato, ultima_leitura))
            candidatos.sort(key=lambda item: item[0])
            if not candidatos or candidatos[0][0] > 10:
                return Response({
                    'status': 'sem_sensor',
                    'tem_risco': None,
                    'mensagem': 'Não há sensor com leitura recente em até 10 km deste ponto.',
                    'estimativa_minutos': None,
                    'simulado': False,
                    'ponto_id': ponto.id,
                    'limite_critico': ponto.limite_emergencia,
                })
            distancia, sensor, _ = candidatos[0]
            base = prever_sensor(sensor.id, ponto.limite_emergencia)
            nivel = base.get('nivel_atual')
            limite_atencao = float(ponto.limite_atencao)
            limite_critico = float(ponto.limite_emergencia)
            if nivel is not None and nivel >= limite_critico:
                classificacao_local = {'status': 'critico', 'tem_risco': True, 'estimativa_minutos': 0}
            elif nivel is not None and (nivel >= limite_atencao or base.get('status') == 'estimavel'):
                classificacao_local = {'status': 'risco', 'tem_risco': True, 'estimativa_minutos': base.get('estimativa_minutos')}
            else:
                classificacao_local = {'status': 'sem_risco', 'tem_risco': False, 'estimativa_minutos': None}

        calculo_base = prever_sensor(sensor.id, ponto.limite_emergencia)
        if simulado:
            calculo_base.update(classificacao_local)
            calculo_base['confianca'] = 'demonstrativa'
            calculo_base['mensagem'] = classificacao_local['mensagem']

        resultado_base = {
            **calculo_base,
            **classificacao_local,
            'simulado': simulado,
            'fonte_previsao': 'reserva_local',
            'ponto_id': ponto.id,
            'ponto_descricao': ponto.descricao,
            'rio_nome': ponto.rio.nome,
            'limite_critico': ponto.limite_emergencia,
            'distancia_sensor_km': round(distancia, 2),
            'sensor_nome': sensor.nome,
        }

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            resultado_base['mensagem_reserva'] = 'Estimativa local.'
            return Response(resultado_base)

        import requests

        leituras = list(sensor.leituras.order_by('-criado_em')[:24])
        leituras.reverse()
        ultima = leituras[-1]
        historico = [
            {
                'minutos_antes_da_ultima': round((ultima.criado_em - item.criado_em).total_seconds() / 60, 2),
                'nivel_m': item.valor,
            }
            for item in leituras
        ]
        contexto_leitura = 'série demonstrativa' if simulado else 'medições do sensor'
        prompt = f'''Você é um modelo de previsão hidrológica de apoio à Defesa Civil. Analise a série abaixo ({contexto_leitura}) e responda exclusivamente JSON com: status ("sem_risco", "risco" ou "critico"), estimativa_minutos (inteiro ou null), confianca ("baixa", "moderada" ou "alta"), tendencia (texto curto em português), justificativa (até 2 frases). Considere os limites de atenção e crítico. Se o nível atual já atingiu o limite crítico, use critico e 0. Se a série está abaixo da atenção e não projeta subida ao limite, use sem_risco e null. Se há tendência de subida em direção ao limite, use risco e estime o tempo. Redija a justificativa em tom formal e conciso, sem mencionar demonstrações, simulações ou alertas oficiais.
Rio: {ponto.rio.nome}; região: {ponto.descricao}; sensor: {sensor.nome}; nível atual: {leituras[-1].valor} m; limite de atenção: {ponto.limite_atencao} m; limite crítico: {ponto.limite_emergencia} m; histórico do mais antigo ao mais novo: {historico}'''
        try:
            modelo = os.getenv('GEMINI_FORECAST_MODEL', 'gemini-3-flash-preview')
            sessao = requests.Session()
            sessao.trust_env = False
            esquema = {
                'type': 'OBJECT',
                'properties': {
                    'status': {'type': 'STRING', 'enum': ['sem_risco', 'risco', 'critico']},
                    'estimativa_minutos': {'type': 'INTEGER', 'nullable': True},
                    'confianca': {'type': 'STRING', 'enum': ['baixa', 'moderada', 'alta']},
                    'tendencia': {'type': 'STRING'},
                    'justificativa': {'type': 'STRING'},
                },
                'required': ['status', 'estimativa_minutos', 'confianca', 'tendencia', 'justificativa'],
            }
            resposta = sessao.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent',
                headers={'x-goog-api-key': api_key, 'Connection': 'close'},
                json={
                    'contents': [{'parts': [{'text': prompt}]}],
                    'generationConfig': {
                        'responseMimeType': 'application/json',
                        'responseSchema': esquema,
                        'maxOutputTokens': 2048,
                    },
                },
                timeout=(3, 8),
            )
            if not resposta.ok:
                logger.warning('Gemini retornou HTTP %s; usando previsão local.', resposta.status_code)
                resultado_base['mensagem_reserva'] = 'Estimativa local.'
                return Response(resultado_base)

            geracao = json.loads(resposta.json()['candidates'][0]['content']['parts'][0]['text'])
            status_modelo = geracao.get('status')
            estimativa = geracao.get('estimativa_minutos')
            confianca = geracao.get('confianca')
            tendencias_validas = {'sem_risco', 'risco', 'critico'}
            confiancas_validas = {'baixa', 'moderada', 'alta'}
            if status_modelo != classificacao_local['status']:
                raise ValueError('Gemini classificou diferente do cenário simulado configurado')
            if estimativa is not None and (isinstance(estimativa, bool) or not isinstance(estimativa, int) or not 0 <= estimativa <= 10080):
                raise ValueError('Estimativa Gemini fora dos limites')
            if status_modelo == 'risco' and (estimativa is None or estimativa <= 0):
                raise ValueError('Gemini não estimou prazo para cenário de risco')
            if status_modelo == 'critico' and estimativa != 0:
                raise ValueError('Cenário crítico precisa retornar zero minutos')
            if status_modelo == 'sem_risco' and estimativa is not None:
                raise ValueError('Cenário sem risco não deve retornar prazo')
            if status_modelo not in tendencias_validas or confianca not in confiancas_validas:
                raise ValueError('Resposta Gemini fora do esquema esperado')

            resultado_base.update({
                'estimativa_minutos': estimativa,
                'confianca': 'demonstrativa' if simulado else confianca,
                'tendencia': geracao.get('tendencia', ''),
                'analise_ia': geracao.get('justificativa', ''),
                'fonte_previsao': 'Gemini',
                'modelo_ia': modelo,
            })
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as erro:
            logger.warning('Falha na previsão Gemini: %s; usando estimativa local.', erro)
            resultado_base['mensagem_reserva'] = 'Estimativa local.'

        return Response(resultado_base)
