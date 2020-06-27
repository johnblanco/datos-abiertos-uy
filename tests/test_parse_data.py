import os
import unittest

from mockito import when

import parse_data
import pandas as pd


class TestParseData(unittest.TestCase):

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

    def test_montevideo_oct_2019(self):
        filename = 'inscripciones-de-empresas-montevideo-102019.csv'

        res = parse_data.load_file_details(filename)

        self.assertEqual(17, res['unipersonal_count'])
        self.assertEqual(1, res['sociedad_de_hecho_count'])

    def test_has_2_cities_true(self):
        filename = 'inscripciones-de-empresas-montevideo-y-salto_112019.csv'

        self.assertTrue(parse_data.has_2_cities(filename))

    def test_has_2_cities_false(self):
        filename = '032019_datos-abiertos-maldonado.csv'

        self.assertFalse(parse_data.has_2_cities(filename))

    def test_missing_months(self):
        # recibe un df[date_str, ciudad] y rango deseado
        # devuelve un df con las rows que le estan faltando
        df = pd.DataFrame.from_dict({'1': ['2019-01', 'Montevideo'], '2': ['2019-02', 'Montevideo']}, orient='index',
                                    columns=['file', 'city'])
        res = parse_data.missing_months_df(df, '2019-01', '2019-03')

        self.assertEqual(1, len(res[(res.date == '2019-03') & (res.city == 'Montevideo') & (res.total == 0)]))
        self.assertEqual(1, len(res[(res.date == '2019-01') & (res.city == 'Salto') & (res.total == 0)]))
        self.assertEqual(1, len(res[(res.date == '2019-02') & (res.city == 'Maldonado') & (res.total == 0)]))
        self.assertEqual(9, len(res))

    def test_add_multiple_cities_files(self):
        d = pd.DataFrame.from_dict({'file': [], 'city': [], 'date': [], 'year': [], 'month': [], 'srl_count': [], 'sa_count': [], 'mono_mides_count': [], 'unipersonal_count': [], 'sociedad_de_hecho_count': [], 'total': []})
        d2 = parse_data.add_multiple_cities_files([])


if __name__ == '__main__':
    unittest.main()
