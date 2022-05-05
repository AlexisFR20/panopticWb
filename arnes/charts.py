from plotly.offline import plot
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_daq as daq
from dash import html
from core.models import Planta

def chart_general():  
    fig = go.Figure(data=[
        go.Bar(marker_color='#555', name='Cumplidos', x=["pocentaje"], y=[82.04], showlegend=False, text=[82.04],
        textposition='outside',
        cliponaxis=False),
        go.Bar(marker_color='#990000',name='No cumplidos', x=["pocentaje"], y=[17.96], showlegend=False, text=[17.96],
        textposition='outside',
        cliponaxis=False)
    ])
    fig.update_layout(
        barmode='stack', 
        xaxis_title="<b>General</b>",
        yaxis_title="<b>Porcentajes</b>",
    )
    return plot(fig, auto_open=False, output_type='div')

def chart_cuestionarios():
    xvals = ["Infraestructura", "Seguridad operativa", "Seguridad electronica", "Logistica", "Entorno"]
    yvals = [85.29, 83.33, 77.5, 0, 0 ]
    fig = go.Figure(data=[
        go.Bar( 
        name='Cumplidos', 
        x=xvals, 
        y=yvals, 
        marker_color=["#A9DFF6", "#BFE17B", "#FFF67B", "#F7AA7C", "#7243C8"],
        text=yvals,
        textposition='outside',
        cliponaxis=False)
    ])
    fig.update_layout(
        xaxis_title="<b>Porcentajes por areas</b>",
        yaxis_title="<b>Porcentajes</b>",
        yaxis=dict( range=[0, 100]),
    )
    return plot(fig, auto_open=False, output_type='div')

def chart_seguridad_electronica():
    fig = go.Figure(data=[
        go.Bar( 
        name='Cumplidos', 
        x=["Alarmas", "CCTV", "Control Accesos"], 
        y=[70, 62.5, 100], 
        marker_color=["#F8F47B", "#FFDD7C", "#FFC583"],
        text=[70, 62.5, 100],
        textposition='outside',
        cliponaxis=False),
        
    ])
    """
        go.Bar( 
        name='Recomendaciones no corregidas', 
        x=["Alarmas"], 
        y=[5], 
        marker_color=["#aaa"],
        text=[5],
        textposition='outside',
        cliponaxis=False),
        """
    fig.update_layout(
        xaxis_title="<b>Seguridad electronica</b>",
        yaxis_title="<b>Porcentajes</b>",
        barmode='stack'
    )
    return plot(fig, auto_open=False, output_type='div')


def chart_alarmas():
    fig = go.Figure(data=[
        go.Bar( 
        name='Alarmas', 
        y=["Falta de monitorista", "No cuentan con análisis de ubicacion CCTV", "Falta de poliza de manto a equipamiento"], 
        x=[12.5, 12.5, 12.5], 
        orientation='h',
        marker_color=["#F8F47B", "#FFDD7C", "#FFC583"],
        text=["Falta de monitorista", "No cuentan con análisis de ubicacion CCTV", "Falta de poliza de manto a equipamiento"],
        textposition='outside',
        cliponaxis=False),
    ])
    
    fig.update_layout(
        xaxis=dict( range=[0, 100]),
        xaxis_title="<b>Alarmas</b>",
    )
    return plot(fig, auto_open=False, output_type='div')

def chart_plantas():
    fig = go.Figure()
    plantas = Planta.objects.values()
    dfp = pd.DataFrame.from_records(plantas)
    #for ciudad in selected:
    dff = dfp
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

    fig.update_layout(
        title='Plantas',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        height=350,
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        mapbox=go.layout.Mapbox(
            accesstoken="pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ",
            bearing=0,
            pitch=0,
            zoom=0,
            style='streets',
            center=go.layout.mapbox.Center(
            lat=0,
            lon=-160,
            )
        ),
    )
    return plot(fig, auto_open=False, output_type='div')

