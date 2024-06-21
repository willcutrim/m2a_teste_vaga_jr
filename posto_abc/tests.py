from django.test import TestCase
from .models import Posto, Tanque, Abastecimento, Bomba, PrecoCombustivel


class TestModels(TestCase):
    def setUp(self):
        self.posto = Posto.objects.create(
            nome='Posto ABC',
        )
        self.tanque = Tanque.objects.create(
            tipo_combustivel='GASOLINA',
            capacidade=1000,
            posto=self.posto,
            nivel_atual=1000,
        )
        self.bomba = Bomba.objects.create(
            tanque=self.tanque,
            identificacao='Bomba 1',
        )
        self.preco_combustivel = PrecoCombustivel.objects.create(
            tipo_combustivel=self.tanque.tipo_combustivel,
            preco_por_litro=5.00,
        )

        self.abastecimento = Abastecimento.objects.create(
            bomba=self.bomba,
            litros=100,
        )

    def test_preco_combustivel(self):
        self.assertEqual(PrecoCombustivel.objects.count(), 1)
        self.assertEqual(self.preco_combustivel.preco_por_litro, 5.00)

    def test_criar_nivel_atual(self):
        self.assertEqual(self.tanque.nivel_atual, 1000)

    def test_str(self):
        self.assertEqual(str(self.posto), 'Posto ABC')
        self.assertEqual(str(self.tanque), 'Gasolina - Capacidade: 1000L - Posto: Posto ABC')


    def test_abastecimento(self):
        self.assertEqual(self.abastecimento.litros, 100)