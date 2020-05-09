import os
import pandas as pd


def extract_city(f):
    if 'montevideo' in f or 'mdeo' in f:
        return 'Montevideo'
    if 'salto' in f:
        return 'Salto'
    if 'maldonado' in f:
        return 'Maldonado'
    return 'Montevideo'


def extract_date(f):
    first_chars = f[0:6]
    digits = ''.join(c for c in first_chars if c.isdigit())
    if len(digits) == 6:
        return '{}-{}'.format(first_chars[2:6], first_chars[0:2])

    return 'UNK'


files = os.listdir('./csvs/')
df = pd.DataFrame.from_dict({'file': files})
df['city'] = df.file.apply(lambda f: extract_city(f))
df['date'] = df.file.apply(lambda f: extract_date(f))
