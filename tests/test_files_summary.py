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

        res = parse_data.files_summary([filename])

        self.assertEqual(12, res[filename]['total'])

    def test_salto(self):
        filename = '062019_datos-abiertos-salto.csv'

        res = parse_data.files_summary([filename])

        self.assertEqual(1, res[filename]['total'])


if __name__ == '__main__':
    unittest.main()
