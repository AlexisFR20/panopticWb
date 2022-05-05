import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from core.models import Planta
from entorno.models import Incidente

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('dash_plantas', external_stylesheets=external_stylesheets)

plantas = Planta.objects.values()
df = pd.DataFrame.from_records(plantas)

incidentes = Incidente.objects.values()
dfi = pd.DataFrame.from_records(incidentes)

app.layout = html.Div([
    html.Div([html.H1("Localización de plantas")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
    html.Div([dcc.Dropdown(id="ciudad-selected", value=['Juarez'], multi=True,
                           options=[{'label': i, 'value': i} for i in df.ciudad.unique()],
                           style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "50%"})]),
    html.Div(dcc.Graph(id="my-graph")),
    html.Div(dcc.Graph(id="my-barras"))
], className="container")

@app.callback(Output('my-graph', 'figure'), [Input('ciudad-selected', 'value')])
def update_figure(selected):
    fig = go.Figure()
    
    for ciudad in selected:
        dff = df[df["ciudad"] == ciudad]
        fig.add_trace(go.Scattermapbox(
            lat=dff.lat,
            lon=dff.lng,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7,
            ),
            text=dff.nombre,
            hoverinfo='text'
        ))

    #mapa de calor delincuencial
    fig.add_trace(go.Densitymapbox(lat=dfi.lat, lon=dfi.lng, z=dfi.cantidad,
                                 radius=10, text=dfi.tipo, hoverinfo="text"))

    fig.update_layout(
        title='Plantas',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        height=700,
        mapbox=go.layout.Mapbox(
            accesstoken="pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ",
            bearing=0,
            pitch=0,
            zoom=9,
            style='streets',
            center=go.layout.mapbox.Center(
            lat=31.6185265,
            lon=-106.3905846
            )
        ),
    )
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

                                        
    
