"""Previsão conservadora do tempo até o limite de emergência por sensor."""
from datetime import timedelta
from statistics import median

from django.utils import timezone

from .models import Sensor, Leitura


def prever_sensor(sensor_id, limite, janela=12):
    sensor = Sensor.objects.get(pk=sensor_id)
    leituras = list(Leitura.objects.filter(sensor_id=sensor_id).order_by('-criado_em')[:janela])
    leituras.reverse()
    agora = timezone.now()
    if not leituras:
        return {'status': 'sem_dados', 'mensagem': 'Ainda não há medições reais para este sensor.', 'estimativa_minutos': None, 'confianca': 'insuficiente', 'sensor_id': sensor.id}
    ultima = leituras[-1]
    idade = (agora - ultima.criado_em).total_seconds()
    if idade > 30 * 60:
        return {'status': 'dados_desatualizados', 'mensagem': 'A última medição tem mais de 30 minutos; atualize o sensor antes de usar a previsão.', 'estimativa_minutos': None, 'confianca': 'insuficiente', 'sensor_id': sensor.id, 'nivel_atual': ultima.valor, 'limite_critico': limite, 'medido_em': ultima.criado_em}
    if ultima.valor >= limite:
        return {'status': 'critico', 'mensagem': 'O nível medido já atingiu ou ultrapassou o limite crítico.', 'estimativa_minutos': 0, 'confianca': 'alta', 'sensor_id': sensor.id, 'nivel_atual': ultima.valor, 'limite_critico': limite, 'medido_em': ultima.criado_em}
    pares = []
    for a, b in zip(leituras, leituras[1:]):
        dt = (b.criado_em - a.criado_em).total_seconds() / 60
        if dt > 0:
            pares.append((b.valor - a.valor) / dt)
    if len(leituras) < 4 or not pares:
        status_ = 'dados_insuficientes'
        rate = None
    else:
        # Mediana das taxas locais reduz o efeito de picos de uma única leitura.
        rate = median(pares[-8:])
        status_ = 'estimavel' if rate > 0 else 'estavel_ou_abaixando'
    minutos = ((limite - ultima.valor) / rate) if rate and rate > 0 else None
    if minutos is not None and minutos > 7 * 24 * 60:
        minutos = None
        status_ = 'fora_do_horizonte'
    variacao = max((max(x.valor for x in leituras) - min(x.valor for x in leituras)), 1e-6)
    ruido = median([abs(x) for x in pares]) if pares else 0
    confianca = 'alta' if len(leituras) >= 8 and idade <= 10 * 60 and ruido <= max(rate or 0, 1e-6) * 0.5 else ('moderada' if len(leituras) >= 5 and idade <= 20 * 60 else 'baixa')
    return {'status': status_, 'mensagem': 'Estimativa matemática da tendência recente; não substitui alerta oficial nem avaliação técnica.', 'estimativa_minutos': round(minutos) if minutos is not None else None, 'taxa_metros_por_minuto': round(rate, 6) if rate is not None else None, 'confianca': confianca if status_ == 'estimavel' else 'insuficiente', 'leituras_usadas': len(leituras), 'nivel_atual': ultima.valor, 'limite_critico': limite, 'sensor_id': sensor.id, 'sensor_nome': sensor.nome, 'rio_id': sensor.rio_id, 'medido_em': ultima.criado_em}
