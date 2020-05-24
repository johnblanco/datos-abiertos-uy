# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import empresa
import red_flags

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Span('Menu: '),
    dcc.Link('Desempeño en las Contrataciones Públicas', href='/'),
    html.Span(' | '),
    dcc.Link('Empresa en el dia', href='/empresa-en-el-dia'),

    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return red_flags.html_layout()
    else:
        return empresa.html_layout()



@app.callback(
    Output('graph', 'figure'),
    [Input('year', 'value')]
)
def update_year(year):
    return empresa.update_year(year)


@app.callback(
    Output('graph2', 'figure'),
    [Input('year2', 'value'),
     Input('city2', 'value'),
     Input('company_type', 'value'),
     ]
)
def update_inputs_by_type_graph(year2, city2, company_type):
    return empresa.update_inputs_by_type_graph(city2, company_type, year2)


if __name__ == '__main__':
    app.run_server(debug=True)
