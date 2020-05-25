import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from plotly.graph_objs import Layout, Bar, Scatter


def scores_by_year(df, names_to_filter) -> list:
    df_sorted = df.copy().sort_values(by='year')

    result = []
    x = ['en 2015', 'en 2016', 'en 2017', 'en 2018']

    for name in names_to_filter:
        result.append({
            'x': x,
            'y': df_sorted[df_sorted.name == name].score.values,
            'name': name
        })
    return result


def html_layout():
    df = pd.read_csv('https://raw.githubusercontent.com/johnblanco/datos-abiertos-uy/master/red-flags.csv').sort_values(
        by='PerformanceIndex', ascending=False)
    df = df[['Year', 'OrganistationShortName', 'PerformanceIndex']]
    df.columns = ['year', 'name', 'score']

    top = df.groupby(by='name').sum()
    top.drop(columns='year', inplace=True)
    top = top.sort_values(by='score', ascending=False).head(7).reset_index()

    df_table = top.copy()
    df_table['score'] = df_table.score.apply(lambda x: round(x, 2))
    df_table.columns = ['Organismo', 'Puntaje acumulado']

    return [
        html.H1('Desempeño en las Contrataciones Públicas'),

        html.Div('''
            Puntaje asignado a los organismos del estado que resume el desempeño en las compras públicas. 
            Cuanto más alto el valor, peor el desempeño.
        '''),

        html.Div(['Este es un trabajo derivado del que hizo cívico y la diaria en ', html.A('cuentasclaras.uy',
                                                                                            href='http://cuentasclaras.uy/#/buying-index')]),

        html.Div('Licencia: Creative Commons Attribution-ShareAlike 4.0 International License'),

        html.Strong('[TODO >>>> agregar paginado de tabla]'),

        html.Div(html.Strong('Cuales son los organismos con peor puntaje acumulado?')),

        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_table.columns],
            data=df_table.to_dict('records'),
        ),

        html.Strong('De los organismos de la tabla anterior, que puntaje sacaron cada año?'),

        dcc.Graph(figure={
            'data': list(map(lambda d: Scatter(x=d['x'], y=d['y'], name=d['name']), scores_by_year(df, top.name.unique()))),
            'layout': {
                'title': 'Puntaje acumulado 2015-2018 de los organismos con peor desempeño'
            }
        }),

        html.Div(html.Strong('Cuantas compras hicieron cada anio?')),

        html.Strong('[TODO >>>> grafico de lineas con compras totales de c/u]'),

        html.Div(html.Strong('Detalle de atributos utilizados para el calculo del puntaje')),

        html.Strong('[TODO >>>> un dropdown donde podes elegir el organismo'),

        html.Strong('[TODO >>>> una tabla con columnas 2015,2016, etc, las filas son los diferentes atributos'),

    ]
