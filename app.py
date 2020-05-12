# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Empresa en el Dia'),

    html.Div(children='''
        Cantidad de empresas creadas, entre 2017 - 2019, a través del sistema de Empresa en el día, agrupado por departamento (Salto, Montevideo y Maldonado).
    '''),

    html.Label("La gráfica muestra los totales de cada mes (unipersonales, SRL, SA, sociedades de hecho, monotributo MIDES)"),

    html.Div(['El dataset es el provisto por Agesic en ', html.A('catalogodatos.gub.uy', href='https://catalogodatos.gub.uy/dataset/agesic-creacion-de-empresas-a-traves-de-empresa-en-el-dia')]),

    dcc.RadioItems(
        id='year',
        options=[
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'},
            {'label': '2019', 'value': '2019'}
        ],
        value='2017',
        labelStyle={'display': 'inline-block'}
    ),

    dcc.Graph(
        id='graph'
    ),

    html.A('Link a Github', href='https://github.com/johnblanco/empresa_en_el_dia'),
    html.Br(),
    html.A('Tareas pendientes', href='https://github.com/johnblanco/empresa_en_el_dia/issues'),

])


@app.callback(
    Output('graph', 'figure'),
    [Input('year', 'value')]
)
def update_year(year):
    df = pd.read_csv('https://raw.githubusercontent.com/johnblanco/empresa_en_el_dia/master/data.csv').sort_values(
        by='date')
    df_mvd = df[(df.year == int(year)) & (df.city == 'Montevideo')]
    df_salto = df[(df.year == int(year)) & (df.city == 'Salto')]
    df_maldo = df[(df.year == int(year)) & (df.city == 'Maldonado')]

    return {
        'data': [
            {'x': df_mvd['month'], 'y': df_mvd['total'],
             'type': 'bar', 'name': 'Montevideo'},
            {'x': df_salto['month'], 'y': df_salto['total'],
             'type': 'bar', 'name': 'Salto'},
            {'x': df_maldo['month'], 'y': df_maldo['total'],
             'type': 'bar', 'name': 'Maldonado'},
        ],
        'layout': {
            'title': 'Total de Creadas en {}'.format(year)
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
