from plotly.offline import plot
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_daq as daq
from dash import html
from .models import Planta

def chart_histograma():  
    df = px.data.tips()
    fig = px.histogram(df, x="total_bill", color="sex")
    return plot(fig, auto_open=False, output_type='div')

def chart_rutas_ceo_master():
    fig = go.Figure(go.Scattermapbox(
    mode = "markers+text+lines",
    lon = [-75, -80, -50], lat = [45, 20, -20],
    marker = {'size': 20, 'symbol': ["bus", "mapbox-logo", "airport"]},
    text = ["Bus", "Harbor", "airport"],textposition = "bottom right"))

    fig.update_layout(
        title='Mapa de Rutas!',        
        autosize=True,
        hovermode='closest',
        showlegend=False,
        height=480,
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        mapbox = {
            'accesstoken': "pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ",            
            'zoom': 0.7,
            'style':"mapbox://styles/jesuscamarillo/ck689p7e514961impenkqakyx",
        })
    
    return plot(fig, auto_open=False, output_type='div')

def mapa_plantas():
    #px.set_mapbox_access_token("pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ")
    plantas = Planta.objects.values()
    df = pd.DataFrame.from_records(plantas)
    fig = go.Figure()
    site_lat = df.lat
    site_lon = df.lng
    locations_name = df.nombre
    fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7,
        ),
        text=locations_name,
        hoverinfo='text'
    ))

    fig.update_layout(
        title='Plantas',
        autosize=True,
        hovermode='closest',
        showlegend=False,
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
    #fig = px.scatter_mapbox(plantas, lat="lat", lon="lng",  color="ciudad", hover_data=["estado", "pais"],
                  #color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10, )
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_grupo_vertical():      
    grupos=['Grupo A', 'Grupo B', 'Grupo C']
    fig = go.Figure(data=[
        go.Bar(name='Hombres', x=grupos, y=[20, 14, 23]),
        go.Bar(name='Mujeres', x=grupos, y=[12, 18, 29])
    ])
    # Cambio en el modo Stack
    fig.update_layout(barmode='stack')
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_grupo_horizontal():      
    grupos=['Grupo A2', 'Grupo B2', 'Grupo C2']
    fig = go.Figure(data=[
        go.Bar(name='Hombres', x=grupos, y=[20, 14, 23]),
        go.Bar(name='Mujeres', x=grupos, y=[12, 18, 29])
    ])
    # Cambio en el modo Stack
    fig.update_layout(barmode='group')
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_grupo_horizontal_lbls_inclinadas():      
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
          'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
        name='Secuestro',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
        name='Homicidio',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_simple_vertical():      
    puntos=['A', 'B', 'C']
    fig = go.Figure([go.Bar(x=puntos, y=[60, 74, 51])])
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_simple_vertical_etiquetas_fijas():      
    x = ['Servicio A', 'Servicio B', 'Servicio C']
    y = [20, 14, 23]

    # Use textposition='auto' for direct text
    fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_color_individual():      
    colors = ['lightslategray',] * 5
    colors[1] = 'crimson'

    fig = go.Figure(data=[go.Bar(
        x=['Homicidio', 'Secuestro', 'Asalto a Tiendas',
        'Aeropuertos', 'Carjacking'],
        y=[20, 14, 23, 25, 22],
        marker_color=colors # marker color can be a single color value or an iterable
    )])
    fig.update_layout(title_text='Actos Delincuenciales')
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_ancho_individual():      
    colors = ['lightslategray',] * 5
    colors[3] = 'crimson'    
    
    fig = go.Figure(data=[go.Bar(
        x=[1, 2, 3, 5.5, 10],
        y=[10, 8, 6, 4, 2],
        width=[0.8, 0.8, 0.8, 3.5, 4], # customize width here
        marker_color=colors # marker color can be a single color value or an iterable
    )])
    return plot(fig, auto_open=False, output_type='div')

def chart_barchart_estilizada():              
    years = [2014, 2015, 2016, 2017, 2018, 2019]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years,
        y=[110, 120, 100, 90, 80, 130],
        name='Homicidio',
        marker_color='rgb(157, 41, 42)'
    ))
    fig.add_trace(go.Bar(x=years,
        y=[4, 2, 1, 5, 2, 3],
        name='Secuestro',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Bar(x=years,
        y=[1, 2, 3, 1, 5, 6],
        name='Carjacking',
        marker_color='rgb(217, 116, 2)'
    ))

    fig.update_layout(
        title='Eventos en Ciudad Juárez en los Últimos 6 años',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='No. Eventos',
            titlefont_size=26,
            tickfont_size=12            
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'            
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.07, # gap between bars of the same location coordinate.
        height=700
    )
    return plot(fig, auto_open=False, output_type='div')
