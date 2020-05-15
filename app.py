# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from plotly.graph_objs import Layout, Bar

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Empresa en el Dia'),

    html.Div(children='''
        Cantidad de empresas creadas, entre 2017 - 2019, a través del sistema de Empresa en el día, agrupado por departamento (Salto, Montevideo y Maldonado).
    '''),

    html.Div(['El dataset es el provisto por Agesic en ', html.A('catalogodatos.gub.uy',
                                                                 href='https://catalogodatos.gub.uy/dataset/agesic-creacion-de-empresas-a-traves-de-empresa-en-el-dia')]),

    html.H2('Totales por mes'),

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

    html.H2('Agrupado por tipo'),

    dcc.RadioItems(
        id='year2',
        options=[
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'},
            {'label': '2019', 'value': '2019'}
        ],
        value='2017',
        labelStyle={'display': 'inline-block'}
    ),

    dcc.RadioItems(
        id='city2',
        options=[
            {'label': 'Montevideo', 'value': 'Montevideo'},
            {'label': 'Salto', 'value': 'Salto'},
            {'label': 'Maldonado', 'value': 'Maldonado'}
        ],
        value='Montevideo',
        labelStyle={'display': 'inline-block'}
    ),

    dcc.Dropdown(
        id='company_type',
        options=[
            {'label': 'SA', 'value': 'SA'},
            {'label': 'SRL', 'value': 'SRL'},
            {'label': 'Unipersonal', 'value': 'Unipersonal'},
            {'label': 'Sociedad de hecho', 'value': 'Sociedad de hecho'},
            {'label': 'Monotributo MIDES', 'value': 'Monotributo MIDES'}
        ],
        value=['SA', 'SRL', 'Monotributo MIDES', 'Unipersonal', 'Sociedad de hecho'],
        multi=True
    ),

    dcc.Graph(
        id='graph2'
    ),

    html.A('Link a Github', href='https://github.com/johnblanco/empresa_en_el_dia'),
    html.Br(),
    html.A('Tareas pendientes', href='https://github.com/johnblanco/empresa_en_el_dia/issues'),

])


@app.callback(
    Output('graph2', 'figure'),
    [Input('year2', 'value'),
     Input('city2', 'value'),
     Input('company_type', 'value'),
     ]
)
def update_inputs_graph2(year2, city2, company_type):
    df = pd.read_csv('https://raw.githubusercontent.com/johnblanco/empresa_en_el_dia/master/data.csv').sort_values(
        by='date')
    df.rename(columns={"srl_count": "SRL", "sa_count": "SA",
                       'mono_mides_count': 'Monotributo MIDES',
                       'sociedad_de_hecho_count': 'Sociedad de hecho',
                       'unipersonal_count': 'Unipersonal'
                       }, inplace=True)
    df = df[(df.year == int(year2)) & (df.city == city2)]

    title = '{}-{}'.format(year2, city2)

    return {
        'data': bars_from_company_type(df, company_type),
        'layout': Layout(barmode='stack', title=title)
    }


def bars_from_company_type(df, company_type):
    bars = []
    all_types = ['SA', 'SRL', 'Monotributo MIDES', 'Unipersonal', 'Sociedad de hecho']
    for c_type in all_types:
        if c_type in company_type:
            bars.append(Bar(
                x=df.month,
                y=df[c_type],
                name=c_type
            ))

    return bars


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
    app.run_server()
