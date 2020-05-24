import unittest
import pandas as pd
import red_flags


class TestRedFlags(unittest.TestCase):

    def test_worst_performers(self):
        df = pd.DataFrame.from_dict({'name': [], 'year':[], 'score': []})

        result = red_flags.worst_performers(df, ['name1', 'name2'])

        self.assertTrue(False)
