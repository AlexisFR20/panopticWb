import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from entorno.models import Incidente
from plotly.offline import plot
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('histograma_delitos', external_stylesheets=external_stylesheets)

incidentes = Incidente.objects.values("fecha", "tipo")
#fig = px.histogram(incidentes, x="fecha", color="tipo", marginal="rug", title="Histograma")

df = pd.DataFrame.from_records(incidentes)
if not incidentes:
    df["fecha"] = ""
    df["tipo"] = ""
df["Date"] = pd.to_datetime(df["fecha"])
df["day"] = df["Date"].dt.day

app.layout = html.Div([html.Div([html.H1("Incidentes Delictivos este Mes")], style={'textAlign': "center"}),
                       html.Div([dcc.Dropdown(
                               id="selected-value", multi=True, 
                               options=[{'label': i, 'value': i} for i in df.tipo.unique()],
                                value=df.tipo.unique(),
                                )],
                                className="row", style={"display": "block", "width": "60%", "margin-left": "auto",
                                                        "margin-right": "auto"}),
                       html.Div([dcc.Graph(id="my-graph")]),
                       html.Div([dcc.RangeSlider(id="day-range", min=1, max=31, step=1, value=[1, 31],
                                                 marks={
                                                "1": str(1),
                                                "5": str(5),
                                                "10": str(10),
                                                "15": str(15), 
                                                "20": str(20), 
                                                "25": str(25)}
                                                )])
                       ], className="container")


@app.callback(
            Output('my-graph', 'figure'),
            [Input('selected-value', 'value'), Input('day-range', 'value')])
def update_figure(selected, day):
    text = {"homicido": "Homicidios", "secuestro": "Secuestro",}
    dff = df[(df["day"] >= day[0]) & (df["day"] <= day[1])]
    trace = []
    colors = {
                "casa_habitación": '#E0AD13',
                "secuestro" : "#37536d",
                "carjacking" : "#3e5ba9",
                "asalto_negocio" : "#0097a7",
                "homicidio" : "#D97402",
                "asalto_transeuntes" : "#009d57",
                "autopartes" : "#a6194a",
        }
    for type in selected:  
        dff2 = dff[dff["tipo"] == type]
        
        trace.append(go.Histogram(x=dff2["day"], opacity=0.7,  name=type, marker_color=colors[str(type)], marker={"line": {"color": "#25232C", "width": 0.2}},
                         xbins={"size": 5}, customdata=dff2["day"], ))
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,
            "layout": go.Layout(title="Incidencia de delitos", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Delitos"}, xaxis={"title": "Fecha"}, bargap=0.15,)}
    