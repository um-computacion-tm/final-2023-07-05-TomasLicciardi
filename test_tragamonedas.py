import unittest
from unittest.mock import patch

from tragamonedas import (
    Tragamonedas,
    NoHayMonedaException,
    NoHayMonedasParaPremioException,
)


class TestTragamonedas(unittest.TestCase):
    def setUp(self):
        self.tragamonedas = Tragamonedas()
        self.tragamonedas.monedas = 1000

    def test_init(self):
        self.assertEqual(
            self.tragamonedas.monedas,
            1000,
        )
        self.assertEqual(
            self.tragamonedas.monedas_tirada,
            0,
        )

    def test_insertar_moneda(self):
        self.tragamonedas.insertar_moneda()
        self.assertEqual(
            self.tragamonedas.monedas,
            1001,
        )
        self.assertEqual(
            self.tragamonedas.monedas_tirada,
            1,
        )

    def test_insertar_varias_monedas(self):
        for _ in range(10):
            self.tragamonedas.insertar_moneda()

        self.assertEqual(
            self.tragamonedas.monedas,
            1010,
        )
        self.assertEqual(
            self.tragamonedas.monedas_tirada,
            10,
        )

    def test_no_insertar_si_no_hay_para_premio(self):
        self.tragamonedas.monedas = 50
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        with self.assertRaises(NoHayMonedasParaPremioException):
            self.tragamonedas.insertar_moneda()
        self.assertEqual(
            self.tragamonedas.monedas,
            55,
        )
        self.assertEqual(
            self.tragamonedas.monedas_tirada,
            5,
        )

    @patch('random.randint', side_effect=[1, 2, 3])
    def test_tirar_descuenta_moneda(self, patched_randint):
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.tirar()
        self.tragamonedas.insertar_moneda()
        self.assertEqual(
            self.tragamonedas.monedas,
            1003,
        )
        self.assertEqual(
            self.tragamonedas.monedas_tirada,
            1,
        )

    def test_tirar_sin_moneda(self):
        with self.assertRaises(NoHayMonedaException):
            self.tragamonedas.tirar()
        self.assertEqual(
            self.tragamonedas.monedas,
            1000,
        )

    @patch('random.randint', side_effect=[1, 2, 3])
    def test_tirar_sin_moneda_a_la_segunda(self, patched_randint):
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.tirar()
        with self.assertRaises(NoHayMonedaException):
            self.tragamonedas.tirar()
        self.assertEqual(
            self.tragamonedas.monedas,
            1002,
        )
        self.assertEqual(
            self.tragamonedas.monedas_tirada,
            0,
        )

    @patch('random.randint', side_effect=[1, 2, 3])
    def test_tirar_sin_premio(self, patched_randint):
        self.tragamonedas.insertar_moneda()
        premio = self.tragamonedas.tirar()
        self.assertEqual(
            premio,
            0,
        )

    @patch('random.randint', side_effect=[1, 1, 1])
    def test_tirar_con_premio(self, patched_randint):
        self.tragamonedas.insertar_moneda()
        premio = self.tragamonedas.tirar()
        self.assertEqual(
            premio,
            1,
        )

    @patch('random.randint', side_effect=[1, 1, 1])
    def test_tirar_con_premio_3_monedas_numero_1(self, patched_randint):
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        premio = self.tragamonedas.tirar()
        self.assertEqual(
            premio,
            3,
        )

    def test_tirar_dos_veces_con_premio(self):
        for _ in range(10):
            self.tragamonedas.insertar_moneda()
        with patch('random.randint', side_effect=[1, 2, 3]):
            premio = self.tragamonedas.tirar()
        self.assertEqual(
            premio,
            0,
        )
        self.assertEqual(
            self.tragamonedas.monedas,
            1010,
        )
        self.tragamonedas.insertar_moneda()
        self.tragamonedas.insertar_moneda()
        with patch('random.randint', side_effect=[5, 5, 5]):
            premio = self.tragamonedas.tirar()
        self.assertEqual(
            premio,
            10,
        )
        self.assertEqual(
            self.tragamonedas.monedas,
            1002,
        )


if __name__ == '__main__':
    unittest.main()
