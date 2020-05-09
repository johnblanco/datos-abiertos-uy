import unittest

import parse_data


class TestExtractDate(unittest.TestCase):

    def test_using_prefix(self):
        res = parse_data.extract_date('062018_datos-abiertos-maldonado.csv')

        self.assertEqual('2018-06', res)

    def test_using_sufix(self):
        res = parse_data.extract_date('montevideo-diciembre-2017.csv')

        self.assertEqual('2017-12', res)


if __name__ == '__main__':
    unittest.main()