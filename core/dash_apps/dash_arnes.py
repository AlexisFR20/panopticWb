import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from core.models import Planta
from plotly.subplots import make_subplots
import dash_dangerously_set_inner_html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"})

app = DjangoDash('dash_arnes', meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

plantas = Planta.objects.values()
dfp = pd.DataFrame.from_records(plantas)

areas_options  = {
    "Infraestructura" : ["Muros Perimetrales", "Control de Accesos", "Perimetros Internos", "Interior del Edificio", ""],
    "Seguridad operativa" : ["Procedimiento", "Embarques Exterior", "Embarques Interior", "Recurso Humano"] ,
    "Seguridad Electrónica" : ["Alarmas", "CCTV", "Control Accesos"],
    "Logística" : ["Logística",],
    "Entorno" : ["Entorno",]
}


app.layout = html.Div([ 
    dcc.Location(id='url', refresh=False),
    html.P(id="page-path"),
    html.Div([dcc.Dropdown(id="selected-values", multi=True, 
                               options=[{'label': i, 'value': i} for i in dfp.ciudad.unique()],
                                value=dfp.ciudad.unique(),
                                )],
                                className="row", style={"display": "block", "width": "80%", "margin-left": "auto",
                                                        "margin-right": "auto",'display': 'none'}),
    html.Div([
        html.Div( html.Div([
            html.Div("Mapa plantas ", className="card-header"),
            html.Div(dcc.Graph(id="my-graph"), className=""),
        ], className="card"), className="col-md-4"),
         html.Div( html.Div([
            html.Div("Plantas", className="card-header"),
            html.Div(id="table-plantas", className="card-body",  style={"height": "500px", "overflow-y": "scroll"}),
        ], className="card"), className="col-md-8"),
    ], id="map-table-container", className="row", style={"margin-top": "32px", "display":"none"}),

    html.Div([
        html.Div([
            dcc.Graph(id="chart_general")
        ], className="col-xl-2 col-sm-4"),
        html.Div([
            dcc.Graph(id="chart_areas")
        ], className="col-xl-4 col-sm-8"),
        html.Div([
            dcc.Dropdown(
                id='area-dropdown',
                options=[{'label': k, 'value': k} for k in areas_options.keys()],
                value='Seguridad Electronica'
            ),
            dcc.Graph(id="chart_area")
        ], className="col-xl-3 col-sm-6"),
        html.Div([
            dcc.Dropdown(id='encuesta-dropdown'),
            dcc.Graph(id="chart_encuesta")
        ], className="col-xl-3 col-sm-6")
        
    ], className="row", style={"margin-top": "32px"}),

    html.Div( html.Div([
            html.Div("Recomendaciones ", className="card-header"),
            html.Div(id="table-recomendaciones", className="card-body",  style={"height": "500px", "overflow-y": "scroll"}),
        ], className="card"), className="col-md-12"),
    
])

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", 
                "https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css",
                "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
                "http://panoptic.iottechnologies.mx/static/core/assets/css/styles.css"]
external_js = ["https://code.jquery.com/jquery-3.4.1.min.js", 
                "https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"]

for css in external_css:
    app.css.append_css({"external_url": css})
for js in external_js:
    app.scripts.append_script({"external_url": js})


@app.expanded_callback(Output('map-table-container', 'style'), [Input('selected-values', 'value')])
def disply_container(selected, *args, **kwargs):
    if kwargs["session_state"]["planta_id"]:
        return {"margin-top": "32px", "display":"none"}
    else:
        return {"margin-top": "32px"}

@app.expanded_callback(Output('my-graph', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()

    userdict = kwargs["session_state"]["userdict"]
    tipousuario = userdict["tipousuario"]
    print("tipousuario: "+str(tipousuario))

    plantas = Planta.objects.filter(cliente__id=userdict["cliente_id"]).values()
    dfp = pd.DataFrame.from_records(plantas)
    LA_list = ['Mexico', 'México', 'Colombia', "Argentina", "Brasil"]
    Mexico_list = ['Mexico', 'México']
    if(tipousuario == "VICEPRESIDENTE LA"):
        dfp = dfp[dfp.pais.isin(LA_list)]
    
    if(tipousuario == "GERENTE REGIONAL"):
        dfp = dfp[dfp.pais.isin(Mexico_list)]

    if(tipousuario == "GERENTE DE PLANTA" or tipousuario == "GERENTE DE PLANTAS PLUS"):
        dfp = dfp[dfp.nombre == "Yazaki Planta 1"]
    
    for ciudad in selected:
        dff = dfp[dfp["ciudad"] == ciudad]
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

    myzoom=0
    mycenterlat=0
    mycenterlng=-205

    #zoomceo=1
    #centerceo=-190
    if(tipousuario == "VICEPRESIDENTE LA"):
        myzoom=1.8
        mycenterlat=-10.2835133
        mycenterlng=-72.7243782
    
    if(tipousuario == "GERENTE REGIONAL"):
        myzoom=3.3
        mycenterlat=24.2578675
        mycenterlng=-101

    if(tipousuario == "GERENTE DE PLANTA" or tipousuario == "GERENTE DE PLANTAS PLUS"):
        myzoom=10
        mycenterlat=31.6854218
        mycenterlng=-106.4193661

    fig.update_layout(
        title='Plantas',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        height=500,
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        mapbox=go.layout.Mapbox(
            accesstoken="pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ",
            bearing=0,
            pitch=0,
            zoom=myzoom,
            style='streets',
            center=go.layout.mapbox.Center(
            lat=mycenterlat,
            lon=mycenterlng,
            )
        ),
    )
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}





@app.expanded_callback(Output('table-plantas', 'children'), [Input('selected-values', 'value')])
def update_output_div(selected, *args, **kwargs):

    userdict = kwargs["session_state"]["userdict"]
    plantas = Planta.objects.filter(cliente__id=userdict["cliente_id"]).values()
    dfp = pd.DataFrame.from_records(plantas)

    cont = ""
    #return "asdasdad"
    lis = []
    lis.append(html.Thead(html.Tr([
            html.Th("Nombre"),
            html.Th("Dirección"),
            html.Th("Ciudad"),
            html.Th("Estado"),
            html.Th("País"),
            html.Th("Estatus"),
        ])))
    tbody = []
    for ciudad in selected:
        dff = dfp[dfp["ciudad"] == ciudad]
        #dff = dfp
        #print(dff)
        i = 0
        if not dff.empty:
            while i < len(dff):
                print(dff.nombre.iloc[i])
                if not dff.nombre.iloc[i]:
                    i += 1
                    continue
                print("Nombre: "+dff.nombre.iloc[i])
                tbody.append(html.Tr([
                    html.Td(str(dff.nombre.iloc[i])),
                    html.Td(str(dff.direccion.iloc[i])),
                    html.Td(str(dff.ciudad.iloc[i])),
                    html.Td(str(dff.estado.iloc[i])),
                    html.Td(str(dff.pais.iloc[i])),
                    html.Td(str(dff.status.iloc[i])),
                ]))
                i += 1
    lis.append(html.Tbody(tbody))

    cont = html.Table(lis, className="table", id="tablep")
    return cont

@app.expanded_callback(Output('chart_general', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
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

    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('chart_areas', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()
    
    xvals = ["Infraestructura", "Seguridad operativa", "Seguridad electrónica", "Logistica", "Entorno"]
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
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('chart_area', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
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
        xaxis_title="<b>Seguridad Electrónica</b>",
        yaxis_title="<b>Porcentajes</b>",
        barmode='stack'
    )
    
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('chart_encuesta', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure(data=[
        go.Bar( 
        name='Alarmas', 
        y=["Falta de monitorista", "No cuentan con análisis de ubicación CCTV", "Falta de poliza de manto a equipamiento"], 
        x=[12.5, 12.5, 12.5], 
        orientation='h',
        marker_color=["#F8F47B", "#FFDD7C", "#FFC583"],
        text=["Falta de monitorista", "No cuentan con análisis de ubicación CCTV", "Falta de poliza de manto a equipamiento"],
        textposition='outside',
        cliponaxis=False),
    ])
    
    fig.update_layout(
        xaxis=dict( range=[0, 100]),
        xaxis_title="<b>Alarmas</b>",
    )
    
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('table-recomendaciones', 'children'), [Input('selected-values', 'value')])
def update_output_div(selected, *args, **kwargs):
    cont = ""
    #return "asdasdad"
    lis = []
    lis.append(html.Thead(html.Tr([
            html.Th("Recomendaciones"),
            html.Th("Costo"),
            html.Th("Sin costo"),
            html.Th("Fecha Límite"),
            html.Th("%"),
            html.Th("Registro"),
            html.Th("Evidencia"),
        ])))
    tbody = []
    
    tbody.append(html.Tr([
        html.Td("Solicitar y contratar minosristas"),
        html.Td("X"),
        html.Td(),
        html.Td("10 Enero 2020"),
        html.Td("5%"),
        html.Td("En Proceso", style={"background-color": "yellow"}),
        html.Td(),
    ]))

    tbody.append(html.Tr([
        html.Td("Solicitar a un esterno un estudio de seguridad de puntos vulnerables del sistema de CCTV"),
        html.Td("X"),
        html.Td(),
        html.Td("10 Enero 2020"),
        html.Td("10%"),
        html.Td("En Proceso", style={"background-color": "#f55", "color": "#fff"}),
        html.Td(),
    ]))

    tbody.append(html.Tr([
        html.Td("Llegar a un acuerdo con el departamento de sistemas para crear el programa de mantenimiento preventivo para el CCTV"),
        html.Td("X"),
        html.Td(),
        html.Td("10 Enero 2020"),
        html.Td("10%"),
        html.Td("En Proceso", style={"background-color": "#f55", "color": "#fff"}),
        html.Td(),
    ]))

    lis.append(html.Tbody(tbody))

    cont = html.Table(lis, className="table", id="tablep")
    return cont

@app.expanded_callback(Output('encuesta-dropdown', 'options'),[Input('area-dropdown', 'value')])
def set_encuesta_options(selected_area, *args, **kwargs):
    print(selected_area)
    print([{'label': i, 'value': i} for i in areas_options[selected_area]])
    return [{'label': i, 'value': i} for i in areas_options[selected_area]]

@app.expanded_callback(Output('encuesta-dropdown', 'value'), [Input('encuesta-dropdown', 'options')])
def set_encuesta_value(available_options, *args, **kwargs):
    return available_options[0]['value']
    

                                        
    
