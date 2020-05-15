import os
import re

import pandas as pd

month_list = 'enero|febrero|marzo|abril|mayo|junio|julio|agosto|setiembre|octubre|noviembre|diciembre'.split("|")


def extract_city(f):
    if 'montevideo' in f or 'mdeo' in f:
        return 'Montevideo'
    if 'salto' in f:
        return 'Salto'
    if 'maldonado' in f:
        return 'Maldonado'
    return 'Montevideo'


def month_from_name(name):
    month = month_list.index(name) + 1
    return f'{month:02}'


def missing_months_df():
    missing = ['2017-01,Maldonado',
               '2017-02,Maldonado',
               '2017-03,Maldonado',
               '2017-04,Maldonado',
               '2017-05,Maldonado',
               '2017-06,Maldonado',
               '2017-07,Maldonado',
               '2017-08,Maldonado',
               '2017-09,Maldonado',
               '2017-10,Maldonado',
               '2017-11,Maldonado',
               '2017-12,Maldonado',
               '2018-01,Maldonado',
               '2018-02,Maldonado',
               '2018-03,Maldonado',
               '2018-04,Maldonado',
               '2018-05,Maldonado',
               '2019-05,Montevideo',
               '2019-07,Montevideo',
               '2019-08,Montevideo',
               '2019-09,Montevideo',
               '2019-10,Montevideo',
               '2019-05,Maldonado',
               '2019-07,Maldonado',
               '2019-08,Maldonado',
               '2019-09,Maldonado',
               '2019-10,Maldonado',
               '2019-11,Maldonado',
               '2019-12,Maldonado',
               '2019-05,Salto',
               '2019-07,Salto',
               '2019-08,Salto',
               '2019-09,Salto',
               '2019-10,Salto',
               '2019-11,Salto',
               '2019-12,Salto']
    rows = {}
    for a in missing:
        date = a.split(',')[0]
        city = a.split(',')[1]
        rows[a] = [
            'not_found',
            city,
            date,
            date[0:4],
            month_list[int(date[5:7]) - 1],
            0, 0, 0, 0, 0, 0]

    return pd.DataFrame.from_dict(rows, orient='index',
                                  columns=['file', 'city', 'date', 'year', 'month', 'srl_count', 'sa_count',
                                           'mono_mides_count', 'unipersonal_count', 'sociedad_de_hecho_count',
                                           'total'])


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


def load_file_details(filename):
    df = pd.read_csv(os.getcwd() + '/csvs/' + filename, encoding='latin1')
    if '-2019.csv' in filename:
        df = pd.read_csv(os.getcwd() + '/csvs/' + filename, sep=';', encoding='latin1')

    sa_count = 0
    srl_count = 0
    mono_mides_count = 0
    unipersonal_count = 0
    sociedad_de_hecho_count = 0

    df = df.rename(columns={"Tipo ": "TIPO", "Tipo": "TIPO", "Nombre del proceso": "TIPO"})

    col = "TIPO"

    sa_count = len(df[(df[col].str.contains('SA')) | (df[col].str.contains('SOCIEDAD AN'))])
    srl_count = len(df[(df[col].str.contains('SRL'))])
    mono_mides_count = len(df[(df[col].str.contains('MONO')) | (df[col].str.contains('MS'))])
    unipersonal_count = len(df[(df[col].str.contains('UNI'))])
    sociedad_de_hecho_count = len(df[(df[col].str.contains('SH')) | (df[col].str.contains('SOCIEDAD DE HECHO'))])

    return {
        'sa_count': sa_count,
        'srl_count': srl_count,
        'mono_mides_count': mono_mides_count,
        'unipersonal_count': unipersonal_count,
        'sociedad_de_hecho_count': sociedad_de_hecho_count
    }


def files_summary(files):
    d = {}
    for filename in files:
        df = pd.read_csv(os.getcwd() + '/csvs/' + filename, encoding='latin1')
        total = len(df)
        file_detail = load_file_details(filename)
        d[filename] = {
            'total': total,
            'sa_count': file_detail['sa_count'],
            'srl_count': file_detail['srl_count'],
            'mono_mides_count': file_detail['mono_mides_count'],
            'unipersonal_count': file_detail['unipersonal_count'],
            'sociedad_de_hecho_count': file_detail['sociedad_de_hecho_count']
        }

    return d


def clean_data():
    files = os.listdir('./csvs/')
    df = pd.DataFrame.from_dict({'file': files})
    df['city'] = df.file.apply(lambda f: extract_city(f))
    df['date'] = df.file.apply(lambda f: extract_date(f))
    df['year'] = df.date.apply(lambda d: d[0:4])
    df['month'] = df.date.apply(lambda d: month_list[int(d[5:7]) - 1])

    file_summary = files_summary(files)

    new_columns = ['srl_count', 'sa_count', 'mono_mides_count', 'unipersonal_count', 'sociedad_de_hecho_count', 'total']
    for col in new_columns:
        df[col] = df.file.apply(lambda f: file_summary[f][col])

    df2 = missing_months_df()
    return pd.concat([df, df2], sort=False)


if __name__ == '__main__':
    df = clean_data()
    df.to_csv('data.csv', index=False)
