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


def missing_months_df(df, from_date, to_date):
    cities = ['Montevideo','Salto', 'Maldonado']
    missing = ['2019-03,Salto']
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
    filename = filename.replace('-1.csv','.csv')
    if 'inscripciones-de-empresas' in filename:
        filename = filename.replace('.csv', '')
        last_digits = filename[-6:]
        month = last_digits[0:2]
        year = last_digits[2:6]
        return '{}-{}'.format(year, month)

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
    df = read_csv_and_rename_columns(filename)

    col = "TIPO"

    print(filename)

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


def files_summary(files) -> dict:
    d = {}
    for filename in files:
        df = pd.read_csv(os.getcwd() + '/csvs/empresa/' + filename, encoding='latin1')
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


def parse_month(d):
    return month_list[int(d[5:7]) - 1]


def has_2_cities(filename):
    return 'montevideo-y-salto' in filename


def add_multiple_cities_files(multiple_city_files):

    return None


def clean_data():
    path = './csvs/empresa'
    all_files = os.listdir(path)
    multiple_city_files = list(filter(lambda x: has_2_cities(x), all_files))#TODO incluir estos que filtre

    files = list(filter(lambda filename: filename not in multiple_city_files, all_files))#TODO incluir estos que filtre


    d = pd.DataFrame.from_dict({'file': files})
    d['city'] = d.file.apply(lambda f: extract_city(f))
    d['date'] = d.file.apply(lambda f: extract_date(f))
    d['year'] = d.date.apply(lambda date: date[0:4])
    d['month'] = d.date.apply(lambda date: parse_month(date))

    file_summary = files_summary(files)

    new_columns = ['srl_count', 'sa_count', 'mono_mides_count', 'unipersonal_count', 'sociedad_de_hecho_count', 'total']
    for col in new_columns:
        d[col] = d.file.apply(lambda f: file_summary[f][col])

    d = add_multiple_cities_files(multiple_city_files)
    df2 = missing_months_df(d, '2017-01', '2020-05')
    return pd.concat([d, df2], sort=False)


def read_csv_and_rename_columns(filename):
    d = pd.read_csv(os.getcwd() + '/csvs/empresa/' + filename, encoding='latin1')
    if len(d.columns) == 1:
        d = pd.read_csv(os.getcwd() + '/csvs/empresa/' + filename, sep=';', encoding='latin1')

    print('antes')
    print(d.columns)
    d = d.rename(
        columns={"Tipo ": "TIPO",
                 "Tipo": "TIPO",
                 "Nombre del proceso": "TIPO",
                 'Tipo de empresa': 'TIPO',
                 'Tipo empresa': 'TIPO'})

    print('despues')
    print(d.columns)

    return d


if __name__ == '__main__':
    df = clean_data()
    df.to_csv('data.csv', index=False)
