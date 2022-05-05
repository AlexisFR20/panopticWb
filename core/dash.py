import dash
import dash_daq as daq
from dash import dcc
from dash import html
from django.http import HttpResponse

def dashapp():  
    app = dash.Dash()
    app.layout = html.Div(id='lerolero', children=[
    html.H1(children='Panoptic Gráficas - Desarrollo'),
    dcc.Graph(id='ejemplo',
        figure={
        'data': [
            {'x': [1, 2, 3, 4], 'y': [1, 8, 3, 7], 'type': 'line', 'name': 'Bicicletas'},
            {'x': [1, 2, 3, 4], 'y': [5, 2, 8, 8], 'type': 'bar', 'name': 'Bicicletas electricas'},
            ],
        'layout': {
        'title': 'Panoptic Gráficas'
            }
        })
    ])       
        
    return (html.Div(), "Learn More")
