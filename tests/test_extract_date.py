import unittest

import parse_data


class TestExtractDate(unittest.TestCase):

    def test_using_prefix(self):
        res = parse_data.extract_date('062018_datos-abiertos-maldonado.csv')

        self.assertEqual('2018-06', res)

    def test_using_sufix(self):
        res = parse_data.extract_date('montevideo-febrero-2017.csv')

        self.assertEqual('2017-02', res)

    def test_without_year(self):
        res = parse_data.extract_date('salto-abril-.csv')

        self.assertEqual('2018-04', res)

        res = parse_data.extract_date('mdeo-mayo.csv')

        self.assertEqual('2018-05', res)

        res = parse_data.extract_date('salto-mayo-.csv')

        self.assertEqual('2018-05', res)

    def test_date_from_new_format(self):
        res = parse_data.extract_date('inscripciones-de-empresas-montevideo_102019.csv')

        self.assertEqual('2019-10', res)



if __name__ == '__main__':
    unittest.main()
