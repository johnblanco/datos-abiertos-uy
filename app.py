# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/johnblanco/empresa_en_el_dia/master/data.csv').sort_values(by='date')

df_mvd_17 = df[(df.year == 2017) & (df.city == 'Montevideo')]
df_salto_17 = df[(df.year == 2017) & (df.city == 'Salto')]

app.layout = html.Div(children=[
    html.H1(children='Empresa en el Dia '),

    html.Div(children='''
        Cantidad de empresas creadas, entre 2017 - 2019, a través del sistema de Empresa en el día, discriminado por departamento (Salto, Montevideo y Maldonado)
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df_mvd_17['month'], 'y': df_mvd_17['total'],
                 'type': 'bar', 'name': 'Montevideo'},
                {'x': df_salto_17['month'], 'y': df_salto_17['total'],
                 'type': 'bar', 'name': 'Salto'},
            ],
            'layout': {
                'title': 'Creadas en 2017'
            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
