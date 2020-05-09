import os
import re

import pandas as pd


def extract_city(f):
    if 'montevideo' in f or 'mdeo' in f:
        return 'Montevideo'
    if 'salto' in f:
        return 'Salto'
    if 'maldonado' in f:
        return 'Maldonado'
    return 'Montevideo'


def month_from_name(name):
    month_list = 'enero|febrero|marzo|abril|mayo|junio|julio|agosto|setiembre|octubre|noviembre|diciembre'.split("|")
    month = month_list.index(name) + 1
    return f'{month:02}'


def extract_date(filename):
    first_chars = filename[0:6]
    digits = ''.join(c for c in first_chars if c.isdigit())
    if len(digits) == 6:
        return '{}-{}'.format(first_chars[2:6], first_chars[0:2])

    m = re.search('(enero|febrero|marzo|abril|mayo|junio|julio|agosto|setiembre|octubre|noviembre|diciembre)', filename)
    if m:
        month = month_from_name(m.group(1))
        all_digits = ''.join(c for c in filename if c.isdigit())
        year = all_digits if len(all_digits) == 4 else '2018'
        return '{}-{}'.format(year, month)

    return '-'


def files_summary(files):
    d = {}
    for filename in files:
        df = pd.read_csv(os.getcwd() + '/csvs/' + filename, encoding='latin1')
        total = len(df)
        d[filename] = {
            'total': total
        }

    return d


def clean_data():
    files = os.listdir('./csvs/')
    df = pd.DataFrame.from_dict({'file': files})
    df['city'] = df.file.apply(lambda f: extract_city(f))
    df['date'] = df.file.apply(lambda f: extract_date(f))

    file_summary = files_summary(files)

    df['srl_count'] = df.file
    new_columns = ['sa_count', 'mono_mides_count', 'unipersonal_count', 'sociedad_de_hecho_count', 'total']
    for col in new_columns:
        df[col] = df.file.apply(lambda f: file_summary[f][col])

    return df


if __name__ == '__main__':
    df = clean_data()
