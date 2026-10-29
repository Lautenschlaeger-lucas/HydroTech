"""Geração determinística de leituras para a demonstração acadêmica."""
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import Leitura, Sensor


def _nivel_base_demonstracao(ponto):
    """Faz o terceiro ponto cadastrado demonstrar uma tendência de risco."""
    ids_pontos = list(
        ponto.__class__.objects.order_by('criado_em', 'pk').values_list('pk', flat=True)
    )
    nivel = max(float(ponto.nivel_base or 0), 0.0)
    limite_atencao = float(ponto.limite_atencao)
    if ponto.pk in ids_pontos[:2]:
        return min(nivel, max(0.0, limite_atencao - 0.1))
    if len(ids_pontos) >= 3 and ids_pontos[2] == ponto.pk:
        return limite_atencao
    return nivel


def preparar_sensor_simulado(ponto):
    """Cria ou renova uma série simulada para um ponto, somente em DEBUG."""
    if not settings.DEBUG:
        return None

    nome = f'Ponto de monitoramento {ponto.pk}: {ponto.descricao}'[:100]
    sensor = Sensor.objects.filter(
        rio=ponto.rio,
        nome__startswith=f'Sensor SIMULADO — Ponto {ponto.pk}:',
    ).first()
    if sensor is None:
        sensor, _ = Sensor.objects.get_or_create(
            rio=ponto.rio,
            nome=nome,
            defaults={
                'tipo': 'nivel_agua',
                'unidade': 'm',
                'status': 'ativo',
                'modelo': 'SIMULADO para apresentação; não é telemetria real',
                'latitude': ponto.latitude,
                'longitude': ponto.longitude,
            },
        )
    sensor.nome = nome
    sensor.tipo = 'nivel_agua'
    sensor.unidade = 'm'
    sensor.status = 'ativo'
    sensor.modelo = 'SIMULADO para apresentação; não é telemetria real'
    sensor.latitude = ponto.latitude
    sensor.longitude = ponto.longitude
    sensor.save(update_fields=[
        'nome', 'tipo', 'unidade', 'status', 'modelo', 'latitude', 'longitude',
        'atualizado_em',
    ])

    base = _nivel_base_demonstracao(ponto)
    atencao = float(ponto.limite_atencao)
    emergencia = float(ponto.limite_emergencia)

    if base >= emergencia:
        valores = [base] * 8
    elif base >= atencao:
        passo = min(0.04, (emergencia - base) / 9)
        valores = [round(max(0.0, base - passo * (7 - indice)), 3) for indice in range(8)]
    else:
        # Série estável abaixo da faixa de atenção: cenário sem risco previsto.
        valores = [round(base, 3)] * 8

    agora = timezone.now()
    leituras = list(sensor.leituras.order_by('criado_em', 'id'))
    for indice, valor in enumerate(valores):
        instante = agora - timedelta(minutes=7 - indice)
        if indice < len(leituras):
            Leitura.objects.filter(pk=leituras[indice].pk).update(
                valor=valor,
                criado_em=instante,
            )
        else:
            leitura = Leitura.objects.create(sensor=sensor, valor=valor)
            Leitura.objects.filter(pk=leitura.pk).update(criado_em=instante)

    if len(leituras) > len(valores):
        Leitura.objects.filter(pk__in=[leitura.pk for leitura in leituras[len(valores):]]).delete()

    return sensor


def classificar_cenario_simulado(ponto):
    """Classificação demonstrativa baseada nos níveis cadastrados no ponto."""
    nivel = _nivel_base_demonstracao(ponto)
    limite_atencao = float(ponto.limite_atencao)
    limite_critico = float(ponto.limite_emergencia)

    if nivel >= limite_critico:
        return {
            'status': 'critico',
            'tem_risco': True,
            'estimativa_minutos': 0,
            'mensagem': 'O nível registrado alcançou o limite crítico.',
        }
    if nivel >= limite_atencao:
        taxa = min(0.04, (limite_critico - nivel) / 9)
        estimativa = max(1, round((limite_critico - nivel) / taxa))
        return {
            'status': 'risco',
            'tem_risco': True,
            'estimativa_minutos': estimativa,
            'mensagem': 'A tendência está acima da faixa de atenção e segue em direção ao limite crítico.',
        }
    return {
        'status': 'sem_risco',
        'tem_risco': False,
        'estimativa_minutos': None,
        'mensagem': 'Nível registrado abaixo da faixa de atenção.',
    }
