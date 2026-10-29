import logging
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
    """Estimativa restrita à Defesa Civil e a administradores."""
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilOrAdmin]

    def get(self, request, ponto_id):
        from math import radians, sin, cos, asin, sqrt
        from django.utils import timezone
        from datetime import timedelta

        ponto = PontoRisco.objects.select_related('rio').get(pk=ponto_id)
        sensores = Sensor.objects.filter(rio_id=ponto.rio_id, tipo='nivel_agua', status='ativo')
        candidatos = []
        for sensor in sensores:
            if sensor.latitude is None or sensor.longitude is None:
                continue
            dlat = radians(sensor.latitude - ponto.latitude)
            dlon = radians(sensor.longitude - ponto.longitude)
            a = sin(dlat / 2) ** 2 + cos(radians(ponto.latitude)) * cos(radians(sensor.latitude)) * sin(dlon / 2) ** 2
            km = 6371 * 2 * asin(sqrt(a))
            ultima = sensor.leituras.order_by('-criado_em').first()
            if ultima and ultima.criado_em >= timezone.now() - timedelta(minutes=30):
                candidatos.append((km, sensor, ultima))
        candidatos.sort(key=lambda item: item[0])
        if not candidatos or candidatos[0][0] > 10:
            return Response({'status': 'sem_sensor', 'mensagem': 'Não há sensor de nível ativo com leitura recente em até 10 km deste ponto.', 'estimativa_minutos': None, 'confianca': 'insuficiente', 'ponto_id': ponto.id, 'limite_critico': ponto.limite_emergencia})
        distancia, sensor, ultima = candidatos[0]
        resultado = prever_sensor(sensor.id, ponto.limite_emergencia)
        resultado.update({'ponto_id': ponto.id, 'ponto_descricao': ponto.descricao, 'rio_nome': ponto.rio.nome, 'distancia_sensor_km': round(distancia, 2)})
        # A previsão numérica é produzida pelo Gemini com base nas medições reais.
        import os
        import requests
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            from .models import Leitura
            leituras = list(Leitura.objects.filter(sensor=sensor).order_by('-criado_em')[:24])
            leituras.reverse()
            historico = [{'minutos_antes_da_ultima': round((ultima.criado_em - item.criado_em).total_seconds() / 60, 2), 'nivel_m': item.valor} for item in leituras]
            prompt = f'''Você é um modelo de previsão hidrológica de apoio à Defesa Civil. Analise somente a série de medições reais abaixo e estime, com cautela, o tempo até o nível atingir o limite de emergência. Responda exclusivamente JSON com as chaves: status ("estimavel", "critico", "estavel_ou_abaixando" ou "dados_insuficientes"), estimativa_minutos (inteiro ou null), confianca ("baixa", "moderada" ou "alta"), tendencia (texto curto em português), justificativa (até 2 frases). Não invente medições nem trate como alerta oficial. Se a série for curta, irregular, antiga ou contraditória, use dados_insuficientes e null.
Rio: {ponto.rio.nome}; região: {ponto.descricao}; sensor: {sensor.nome}; unidade: {sensor.unidade}; limite crítico: {ponto.limite_emergencia} {sensor.unidade}; última medição UTC: {ultima.criado_em.isoformat()}; histórico do mais antigo ao mais novo: {historico}'''
            try:
                modelo = os.getenv('GEMINI_FORECAST_MODEL', 'gemini-3-flash-preview')
                sessao = requests.Session()
                # Em Windows, o proxy herdado pelo requests causava timeout; conexão direta validada.
                sessao.trust_env = False
                esquema = {'type': 'OBJECT', 'properties': {'status': {'type': 'STRING', 'enum': ['estimavel', 'critico', 'estavel_ou_abaixando', 'dados_insuficientes']}, 'estimativa_minutos': {'type': 'INTEGER', 'nullable': True}, 'confianca': {'type': 'STRING', 'enum': ['baixa', 'moderada', 'alta']}, 'tendencia': {'type': 'STRING'}, 'justificativa': {'type': 'STRING'}}, 'required': ['status', 'estimativa_minutos', 'confianca', 'tendencia', 'justificativa']}
                resposta = sessao.post(f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent', headers={'x-goog-api-key': api_key, 'Connection': 'close'}, json={'contents': [{'parts': [{'text': prompt}]}], 'generationConfig': {'responseMimeType': 'application/json', 'responseSchema': esquema, 'maxOutputTokens': 2048}}, timeout=(5, 35))
                if resposta.ok:
                    import json
                    geracao = json.loads(resposta.json()['candidates'][0]['content']['parts'][0]['text'])
                    estados_validos = {'estimavel', 'critico', 'estavel_ou_abaixando', 'dados_insuficientes'}
                    estimativa = geracao.get('estimativa_minutos')
                    if geracao.get('status') not in estados_validos or (estimativa is not None and (not isinstance(estimativa, int) or estimativa < 0 or estimativa > 10080)):
                        raise ValueError('Resposta estruturada fora dos limites esperados')
                    resultado.update({'status': geracao['status'], 'estimativa_minutos': estimativa, 'confianca': geracao.get('confianca', 'baixa'), 'tendencia': geracao.get('tendencia', ''), 'analise_ia': geracao.get('justificativa', ''), 'modelo_ia': modelo, 'provedor_previsao': 'Gemini'})
                else:
                    logger.error('Gemini retornou HTTP %s: %s', resposta.status_code, resposta.text[:300])
                    resultado.update({'status': 'ia_indisponivel', 'estimativa_minutos': None, 'confianca': 'insuficiente', 'provedor_previsao': None, 'mensagem': 'A IA não está disponível para gerar a previsão neste momento.'})
            except (requests.RequestException, KeyError, IndexError, ValueError) as erro:
                logger.warning('Falha na previsão hidrológica Gemini: %s', erro)
                resultado.update({'status': 'ia_indisponivel', 'estimativa_minutos': None, 'confianca': 'insuficiente', 'provedor_previsao': None, 'mensagem': 'A IA não conseguiu gerar uma previsão válida neste momento.'})
        else:
            resultado.update({'status': 'ia_nao_configurada', 'estimativa_minutos': None, 'confianca': 'insuficiente', 'provedor_previsao': None, 'mensagem': 'Configure GEMINI_API_KEY para habilitar a previsão por IA.'})
        return Response(resultado)
