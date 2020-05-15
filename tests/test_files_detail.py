import os
import unittest

from mockito import when

import parse_data


class TestFilesSummary(unittest.TestCase):

    def setUp(self):
        root_path = os.getcwd().replace('/tests', '')
        when(os).getcwd().thenReturn(root_path)

    def test_maldonado(self):
        filename = '012019_datos-abiertos-maldonado.csv'

        res = parse_data.load_file_details(filename)

        self.assertEqual(1, res['sociedad_de_hecho_count'])
        self.assertEqual(11, res['mono_mides_count'])

    def test_montevideo(self):
        filename = '012019_datos-abiertos-montevideo.csv'

        res = parse_data.load_file_details(filename)

        self.assertEqual(3, res['sa_count'])
        self.assertEqual(5, res['srl_count'])
        self.assertEqual(3, res['sociedad_de_hecho_count'])
        self.assertEqual(20, res['mono_mides_count'])

    def test_maldonado2(self):
        filename = '102018_datos-abiertos-maldonado.csv'

        res = parse_data.load_file_details(filename)

        self.assertEqual(4, res['sociedad_de_hecho_count'])
        self.assertEqual(23, res['unipersonal_count'])

    def test_salto(self):
        filename = '122018_datos-abiertos-salto.csv'

        res = parse_data.load_file_details(filename)

        self.assertEqual(18, res['mono_mides_count'])

    def test_salto3(self):
        filename = '042019_datos-abiertos-salto.csv'

        res = parse_data.load_file_details(filename)

        self.assertEqual(21, res['mono_mides_count'])
        self.assertEqual(4, res['sociedad_de_hecho_count'])


if __name__ == '__main__':
    unittest.main()
