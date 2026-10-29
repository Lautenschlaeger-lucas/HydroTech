from datetime import date
from datetime import timedelta
from django.utils import timezone
from unittest.mock import patch
from unittest import skipUnless
import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from usuarios.models import Usuario
from .models import Sensor, SensorGroup, Leitura
from .previsao import prever_sensor


class CompositeSensorTests(TestCase):
    """Testes do padrão Composite aplicado aos sensores."""

    def setUp(self):
        self.grupo_raiz = SensorGroup.objects.create(
            nome='Estação Bacia do Tietê', descricao='Raiz da árvore'
        )
        self.sensor_nivel = Sensor.objects.create(
            nome='Sensor nível Tietê', tipo='nivel_agua', unidade='m'
        )
        self.sensor_vazao = Sensor.objects.create(
            nome='Sensor vazão tributário', tipo='vazao', unidade='m³/s'
        )

    def test_leaf_nao_aceita_filhos(self):
        """Sensor é uma folha e não pode conter filhos."""
        with self.assertRaises(TypeError):
            self.sensor_nivel.adicionar(self.sensor_vazao)
        with self.assertRaises(TypeError):
            self.sensor_nivel.remover(self.sensor_vazao)

    def test_folha_retorna_apenas_si_mesma(self):
        self.assertEqual(self.sensor_nivel.get_sensores(), [self.sensor_nivel])
        self.assertEqual(self.sensor_nivel.get_tipo(), 'sensor')


class PrevisaoHidrologicaTests(TestCase):
    def setUp(self):
        self.grupo_raiz = SensorGroup.objects.create(nome='Grupo teste', descricao='Grupo para regressão')
        self.sensor_nivel = Sensor.objects.create(nome='Sensor nível regressão', tipo='nivel_agua', unidade='m')
        self.sensor_vazao = Sensor.objects.create(nome='Sensor vazão regressão', tipo='vazao', unidade='m³/s')
        self.usuario = Usuario.objects.create(nome='Equipe', email='equipe@example.com', senha='x', data_nascimento='2000-01-01', is_defesa_civil=True)
        from rios.models import Rios, PontoRisco
        self.rio = Rios.objects.create(nome='Rio Teste', cidade='Campinas', estado='SP', criado_por=self.usuario)
        self.ponto = PontoRisco.objects.create(rio=self.rio, latitude=-22.9, longitude=-47.06, descricao='Ponte', limite_emergencia=3, criado_por=self.usuario)
        self.sensor = Sensor.objects.create(nome='Nível teste', tipo='nivel_agua', unidade='m', rio=self.rio, latitude=-22.9, longitude=-47.06)

    def adicionar_leituras(self, valores):
        agora = timezone.now()
        for minutos_atras, valor in valores:
            leitura = Leitura.objects.create(sensor=self.sensor, valor=valor)
            Leitura.objects.filter(pk=leitura.pk).update(criado_em=agora - timedelta(minutes=minutos_atras))

    def test_tendencia_de_subida_estima_horizonte(self):
        self.adicionar_leituras([(30, 1.0), (20, 1.5), (10, 2.0), (0, 2.5)])
        resultado = prever_sensor(self.sensor.id, 3.0)
        self.assertEqual(resultado['status'], 'estimavel')
        self.assertEqual(resultado['estimativa_minutos'], 10)
        self.assertIn(resultado['confianca'], ['baixa', 'moderada', 'alta'])

    def test_sem_historico_nao_inventa_estimativa(self):
        resultado = prever_sensor(self.sensor.id, 3.0)
        self.assertEqual(resultado['status'], 'sem_dados')
        self.assertIsNone(resultado['estimativa_minutos'])

    def test_nivel_ja_critico_retorna_zero(self):
        self.adicionar_leituras([(30, 2.0), (20, 2.2), (10, 2.5), (0, 3.1)])
        resultado = prever_sensor(self.sensor.id, 3.0)
        self.assertEqual(resultado['status'], 'critico')
        self.assertEqual(resultado['estimativa_minutos'], 0)

    def test_endpoint_associa_sensor_proximo_e_retorna_previsao(self):
        self.adicionar_leituras([(30, 1.0), (20, 1.5), (10, 2.0), (0, 2.5)])
        geracao = {'candidates': [{'content': {'parts': [{'text': '{"status":"estimavel","estimativa_minutos":10,"confianca":"moderada","tendencia":"subindo","justificativa":"A série mostra subida contínua."}'}]}}]}
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}), patch('requests.Session.post') as post:
            post.return_value.ok = True
            post.return_value.json.return_value = geracao
            resposta = self.client.get(f'/sensores/previsao/ponto-risco/{self.ponto.id}/')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()['sensor_id'], self.sensor.id)
        self.assertEqual(resposta.json()['estimativa_minutos'], 10)
        self.assertEqual(resposta.json()['provedor_previsao'], 'Gemini')
        self.assertEqual(resposta.json()['analise_ia'], 'A série mostra subida contínua.')

    def test_sem_chave_ia_nao_mostra_estimativa_local_como_previsao(self):
        self.adicionar_leituras([(30, 1.0), (20, 1.5), (10, 2.0), (0, 2.5)])
        with patch.dict('os.environ', {}, clear=True):
            resposta = self.client.get(f'/sensores/previsao/ponto-risco/{self.ponto.id}/')
        self.assertEqual(resposta.json()['status'], 'ia_nao_configurada')
        self.assertIsNone(resposta.json()['estimativa_minutos'])

    def test_endpoint_sem_sensor_retorna_indisponibilidade_clara(self):
        resposta = self.client.get(f'/sensores/previsao/ponto-risco/{self.ponto.id}/')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()['status'], 'sem_sensor')
        self.assertIsNone(resposta.json()['estimativa_minutos'])

    @skipUnless(os.getenv('HYDROTECH_LIVE_GEMINI') == '1', 'Teste online opt-in: defina HYDROTECH_LIVE_GEMINI=1')
    def test_integracao_real_com_gemini(self):
        self.adicionar_leituras([(30, 1.0), (20, 1.5), (10, 2.0), (0, 2.5)])
        resposta = self.client.get(f'/sensores/previsao/ponto-risco/{self.ponto.id}/')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()['provedor_previsao'], 'Gemini')
        self.assertIsInstance(resposta.json()['estimativa_minutos'], int)
        self.assertGreaterEqual(resposta.json()['estimativa_minutos'], 0)

    def test_grupo_agrega_sensores_diretos(self):
        self.grupo_raiz.adicionar(self.sensor_nivel)
        self.grupo_raiz.adicionar(self.sensor_vazao)
        sensores = self.grupo_raiz.get_sensores()
        self.assertEqual(len(sensores), 2)
        self.assertIn(self.sensor_nivel, sensores)
        self.assertIn(self.sensor_vazao, sensores)
        self.assertEqual(self.grupo_raiz.get_total_sensores(), 2)

    def test_grupo_agrega_recursivamente_subgrupos(self):
        subgrupo = SensorGroup.objects.create(nome='Subgrupo Afluente')
        sensor_profundidade = Sensor.objects.create(
            nome='Sensor profundidade', tipo='outro', unidade='m'
        )
        subgrupo.adicionar(sensor_profundidade)
        self.grupo_raiz.adicionar(subgrupo)
        self.grupo_raiz.adicionar(self.sensor_nivel)

        sensores = self.grupo_raiz.get_sensores()
        self.assertEqual(len(sensores), 2)
        self.assertIn(sensor_profundidade, sensores)
        self.assertIn(self.sensor_nivel, sensores)
        self.assertEqual(self.grupo_raiz.get_total_sensores(), 2)

    def test_grupo_remover_componente(self):
        self.grupo_raiz.adicionar(self.sensor_nivel)
        self.grupo_raiz.remover(self.sensor_nivel)
        self.assertIsNone(self.sensor_nivel.grupo)
        self.assertEqual(self.grupo_raiz.get_total_sensores(), 0)

    def test_sensor_fora_de_rio(self):
        """Sensores podem existir fora de um rio (rio=None)."""
        sensor_clima = Sensor.objects.create(
            nome='Pluviômetro urbano', tipo='pluviometria', unidade='mm',
            latitude=-23.55, longitude=-46.63,
        )
        self.assertIsNone(sensor_clima.rio)
        self.assertEqual(sensor_clima.get_tipo(), 'sensor')

    def test_leituras_agregadas_percorrem_subarvore(self):
        subgrupo = SensorGroup.objects.create(nome='Subgrupo')
        subgrupo.adicionar(self.sensor_nivel)
        self.grupo_raiz.adicionar(self.sensor_vazao)
        self.grupo_raiz.adicionar(subgrupo)

        Leitura.objects.create(sensor=self.sensor_nivel, valor=4.2)
        Leitura.objects.create(sensor=self.sensor_vazao, valor=120.5)

        leituras = self.grupo_raiz.get_leituras_agregadas()
        self.assertEqual(len(leituras), 2)


class SensorAPICompositeTests(TestCase):
    """Testes da API REST (Composite via endpoints)."""

    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create(
            nome='Usuário Comum',
            email='sensor-test-1@example.org',
            senha='senha123',
            data_nascimento=date(1990, 1, 1),
        )
        self.defesa_civil = Usuario.objects.create(
            nome='Defesa Civil',
            email='sensor-test-2@example.org',
            senha='defesa123',
            data_nascimento=date(1985, 5, 5),
            is_defesa_civil=True,
        )

    def _auth(self, user):
        self.client.force_authenticate(user=user)

    def test_criar_grupo_e_sensor_requer_defesa_civil(self):
        url_grupo = '/sensores/grupos/'

        self._auth(self.usuario)
        resposta = self.client.post(url_grupo, {'nome': 'Estação Rio'}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

        self._auth(self.defesa_civil)
        resposta = self.client.post(url_grupo, {'nome': 'Estação Rio'}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        grupo_id = resposta.data['id']

        resposta = self.client.post(
            '/sensores/',
            {
                'nome': 'Sensor de Nível',
                'tipo': 'nivel_agua',
                'unidade': 'm',
                'grupo': grupo_id,
            },
            format='json',
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data['grupo'], grupo_id)
        self.assertEqual(resposta.data['grupo_nome'], 'Estação Rio')

    def test_detalhe_do_grupo_retorna_arvore_composta(self):
        self._auth(self.defesa_civil)

        resposta = self.client.post(
            '/sensores/grupos/', {'nome': 'Estação Principal'}, format='json'
        )
        grupo_id = resposta.data['id']
        resposta = self.client.post(
            '/sensores/grupos/',
            {'nome': 'Subgrupo Afluente', 'parent': grupo_id},
            format='json',
        )
        subgrupo_id = resposta.data['id']
        self.client.post(
            '/sensores/',
            {
                'nome': 'Sensor Nível Afluente',
                'tipo': 'nivel_agua',
                'unidade': 'm',
                'grupo': subgrupo_id,
            },
            format='json',
        )

        resposta = self.client.get(f'/sensores/grupos/{grupo_id}/')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data['subgrupos']), 1)
        self.assertEqual(resposta.data['subgrupos'][0]['sensores'][0]['nome'],
                         'Sensor Nível Afluente')
        self.assertEqual(resposta.data['total_sensores'], 1)

    def test_get_sem_autenticacao_retorna_permission_denied(self):
        resposta = self.client.get('/sensores/')
        self.assertIn(resposta.status_code,
                      (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_criar_leitura(self):
        self._auth(self.defesa_civil)
        resposta = self.client.post(
            '/sensores/',
            {
                'nome': 'Sensor de Chuva',
                'tipo': 'pluviometria',
                'unidade': 'mm',
            },
            format='json',
        )
        sensor_id = resposta.data['id']

        resposta = self.client.post(
            f'/sensores/{sensor_id}/leituras/',
            {'valor': 25.4},
            format='json',
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data['sensor'], sensor_id)
