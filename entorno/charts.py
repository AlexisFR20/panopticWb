from plotly.offline import plot
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from . import models


def chart_histograma_delitos():  
    incidentes = models.Incidente.objects.values("fecha", "tipo")
    if not incidentes:
        return "Sin Datos"
    fig = px.histogram(incidentes, x="fecha", color="tipo", marginal="rug", title="Histograma")
    return plot(fig, auto_open=False, output_type='div')

def chart_scatter():
    foods = models.Food.objects.values()
    fig = px.scatter(foods, x="name", y="weight", color="tipe", facet_col="tipe", marginal_x="rug", marginal_y="violin")
    fig.update_layout(
        template="plotly_dark",
    )
    return plot(fig, auto_open=False, output_type='div')


def chart_lifeexp_gdp():
    df  = px.data.gapminder()
    fig = px.scatter(df, 
        x="gdpPercap", 
        y="lifeExp", 
        animation_frame="year", 
        animation_group="country",
        size="pop", 
        color="continent", 
        hover_name="country", 
        facet_col="continent",
        log_x=True, 
        size_max=45, 
        range_x=[100,100000], 
        range_y=[25,90])
    return plot(fig, auto_open=False, output_type='div')

def chart_custom_controls():
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(df.Date),
            y=list(df.High),
            line=go.scatter.Line(color="green"),
        )
    )

    # Set title and style
    fig.update_layout(
        title_text="Test Custom charts",
        
    )

    # Add range slider
    fig.update_layout(
        xaxis=go.layout.XAxis(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        updatemenus=[
            go.layout.Updatemenu(
                type="buttons",
                direction="right",
                active=0,
                x=0.57,
                y=1.2,
                buttons=list([
                    dict(label="Green",
                        method="restyle",
                        args=[{"line": go.scatter.Line(color="green")}]),
                    dict(label="Blue",
                        method="restyle",
                        args=[{"line": go.scatter.Line(color="blue")}]),
                    
                   
                ]),
                )
        ]

    )
    return plot(fig, auto_open=False, output_type='div')

def custom_dash():
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[0, 1, 2, 3, 4, 5],
            y=[1.5, 1, 1.3, 0.7, 0.8, 0.9]
        ))

    fig.add_trace(
        go.Bar(
            x=[0, 1, 2, 3, 4, 5],
            y=[1, 0.5, 0.7, -1.2, 0.3, 0.4]
        ))
    return plot(fig, auto_open=False, output_type='div')



