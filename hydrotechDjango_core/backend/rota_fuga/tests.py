"""Contrato HTTP dos endpoints de rota integrados ao Django."""
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase

from rios.models import PontoRisco, Rios
from usuarios.models import Usuario


class RotasIntegradasTests(SimpleTestCase):
    def test_status_publico(self):
        resposta = self.client.get("/status")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["servico"], "hydrotech-rotas-integrado")

    def test_coordenadas_invalidas(self):
        resposta = self.client.get("/rota-fuga", {"lat": "nan", "lng": -47})
        self.assertEqual(resposta.status_code, 400)

    def test_alerta_invalido(self):
        resposta = self.client.get("/zonas-risco", {"alerta": "1,x"})
        self.assertEqual(resposta.status_code, 400)

    def test_zonas_filtradas(self):
        async def zonas_mock(forcar=False):
            return [
                {"id": 1, "lat": -22.9, "lng": -47.0},
                {"id": 2, "lat": -22.8, "lng": -47.1},
            ]

        with patch("rota_fuga.views.carregar_zonas", zonas_mock):
            resposta = self.client.get("/zonas-risco", {"alerta": "2", "atualizar": "true"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual([zona["id"] for zona in resposta.json()], [2])

    def test_rota_usa_servico_existente(self):
        async def planejar_mock(lat, lng, modo, alertas):
            return {"origem": {"lat": lat, "lng": lng}, "modo": modo, "alertas": sorted(alertas)}

        with patch("rota_fuga.views.planejar_fuga", planejar_mock):
            resposta = self.client.get("/rota-fuga", {
                "lat": -22.9, "lng": -47.0, "modo": "carro", "alerta": "2,1",
            })
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["alertas"], [1, 2])

    def test_nao_calcula_rota_fora_da_area_de_risco(self):
        async def zonas_mock(forcar=False):
            return [{"id": 1, "lat": -22.9, "lng": -47.0, "raio_m": 300}]

        with patch("rota_fuga.servico.carregar_zonas", zonas_mock), \
                patch("rota_fuga.servico.area_mais_segura") as destinos:
            resposta = self.client.get("/rota-fuga", {"lat": -23.0, "lng": -47.0})

        self.assertEqual(resposta.status_code, 422)
        self.assertIn("fora das áreas de risco", resposta.json()["detail"])
        destinos.assert_not_called()

    def test_nao_calcula_rota_sem_pontos_cadastrados(self):
        async def zonas_mock(forcar=False):
            return []

        with patch("rota_fuga.servico.carregar_zonas", zonas_mock):
            resposta = self.client.get("/rota-fuga", {"lat": -22.9, "lng": -47.0})

        self.assertEqual(resposta.status_code, 422)

    def test_falha_na_consulta_de_zonas_nao_gera_rota(self):
        async def zonas_mock(forcar=False):
            raise RuntimeError("Banco indisponível")

        with patch("rota_fuga.servico.carregar_zonas", zonas_mock):
            resposta = self.client.get("/rota-fuga", {"lat": -22.9, "lng": -47.0})

        self.assertEqual(resposta.status_code, 503)


class ZonasDoBancoTests(TestCase):
    def test_zonas_usa_banco_sem_servico_fastapi(self):
        usuario = Usuario.objects.create(
            nome="Teste", email="rotas@example.invalid", senha="teste", data_nascimento="2000-01-01",
        )
        rio = Rios.objects.create(nome="Rio Teste", cidade="Campinas", estado="SP", criado_por=usuario)
        ponto = PontoRisco.objects.create(
            rio=rio, latitude=-22.9, longitude=-47.0, descricao="Ponto simulado", criado_por=usuario,
        )

        resposta = self.client.get("/zonas-risco", {"atualizar": "1"}, HTTP_ORIGIN="https://hydro-tech-psi.vercel.app")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta["Access-Control-Allow-Origin"], "https://hydro-tech-psi.vercel.app")
        self.assertEqual(resposta.json(), [{
            "id": ponto.id,
            "descricao": "Ponto simulado",
            "rio": "Rio Teste",
            "cidade": "Campinas",
            "lat": -22.9,
            "lng": -47.0,
            "raio_m": 300.0,
        }])
