import unittest
import pandas as pd
import red_flags


class TestRedFlags(unittest.TestCase):

    def test_scores_by_year(self):
        df = pd.DataFrame.from_dict({
            'row1': ['antel', 2017, 10],
            'row2': ['antel', 2016, 20],
            'row3': ['antel', 2017, 30],
            'row4': ['fuji', 2017, 10],
            'row5': ['kodak', 2017, 10],
        }, orient='index', columns=['name', 'year', 'score'])

        result = red_flags.scores_by_year(df, ['antel'])

        self.assertEqual(1, len(result))
        self.assertEqual('antel', result[0]['name'])
        self.assertEqual(20, result[0]['y'][0])

