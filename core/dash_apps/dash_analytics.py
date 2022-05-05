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
from flask import request

# ... inside app.callback ... 



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"})

app = DjangoDash('dash_analytics', meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

plantas = Planta.objects.values()
dfp = pd.DataFrame.from_records(plantas)


app.layout = html.Div([ 
    html.Div([dcc.Dropdown(id="selected-values", multi=True, 
                               options=[{'label': i, 'value': i} for i in dfp.ciudad.unique()],
                                value=dfp.ciudad.unique(),
                                )],
                                className="row", style={"display": "none", "width": "90%", "margin-left": "auto",
                                                        "margin-right": "auto"}),
    html.Div([
        html.Div( html.Div([
            html.Div("Mapa plantas ", className="card-header"),
            html.Div(dcc.Graph(id="my-graph"), className=""),
        ], className="card"), className="col-md-6"),
        html.Div( html.Div([
            html.Div([
                html.Img(src="/static/core/assets/images/flecha03.png", className="img-fluid float-left", style={"height": "18px"}),
                html.Span("Rotación", id="pie1-header", style={"min-width": "150px"}),
                html.Div([
                     html.Img(src="/static/core/assets/images/flecha02.png", className="img-fluid", style={"height": "18px"}),
                    html.Img(src="/static/core/assets/images/print.gif", className="img-fluid", style={"height": "18px", "margin-left":"8px"}),
                ], className="float-right")
            ], className="card-header text-center"),
            html.Div(dcc.Graph(id="pie-rotacion"), className="card-body"),
        ], className="card"), className="col-md-3"),
        html.Div(html.Div([
            html.Div([
                html.Img(src="/static/core/assets/images/flecha03.png", className="img-fluid float-left", style={"height": "18px"}),
                html.Span("Ausentismo", id="pie2-header", className="float-center", style={"min-width": "150px"}),
                html.Div([
                     html.Img(src="/static/core/assets/images/flecha02.png", className="img-fluid", style={"height": "18px"}),
                    html.Img(src="/static/core/assets/images/print.gif", className="img-fluid", style={"height": "18px", "margin-left":"8px"}),
                ], className="float-right")
               
            ], className="card-header text-center"),
            html.Div(dcc.Graph(id="pie-ausentismo"), className="card-body"),
        ], className="card"), className="col-md-3"),
    ], className="row", style={"margin-top": "32px"}),

    
    html.Div( html.Div([
        html.Div([
            "Plantas",
            html.Img(src="/static/core/assets/images/print.gif", className="img-fluid float-right", style={"height": "18px", "margin-left":"8px"}),
        ], className="card-header"),
        html.Div(id="table-plantas", className="card-body",  style={"height": "300px", "overflow-y": "scroll"}),
    ], className="card"), className="col-md-12"),

    html.Div([
        html.Div( html.Div([
            html.Div([
                "Capacitacion",
                html.Img(src="/static/core/assets/images/print.gif", className="img-fluid float-right", style={"height": "18px", "margin-left":"8px"}),
            ], className="card-header"),
            html.Div(dcc.Graph(id="bar-capacitacion"), className="card-body"),
        ], className="card"), className="col-md-7"),
        
        html.Div( html.Div([
            html.Div(["Cobertura",
            html.Img(src="/static/core/assets/images/print.gif", className="img-fluid float-right", style={"height": "18px", "margin-left":"8px"}),
            ], className="card-header"),
            html.Div(dcc.Graph(id="bar-cobertura"), className="card-body"),
            html.Div([
                html.B("Cobertura Semanal"),
                html.H2("75%", id="porcentaje-cobertura"),
            ], className="card card-body", style={"position": "absolute", "bottom": "8px", "right": "8px", "width": "120px"})
        ], className="card"), className="col-md-5"),

    ], className="row", style={"margin-top": "32px"}),
    html.Script('setTimeout(function(){jQuery("#tablep").DataTable({language:{url:"//cdn.datatables.net/plug-ins/1.10.20/i18n/Spanish.json"}})},6e3);'),

    
    
    
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

@app.expanded_callback(Output('my-graph', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()
    #print("flask request: "+str(request.args))
    userdict = kwargs["session_state"]["userdict"]
    tipousuario = userdict["tipousuario"]
    print("tipousuario: "+str(tipousuario))
    print("User "+str(userdict))
    plantas = Planta.objects.filter(cliente__id=userdict["cliente_id"]).values()
    dfp = pd.DataFrame.from_records(plantas)

    LA_list = ['Mexico', 'México', 'Colombia', "Argentina", "Brasil"]
    Mexico_list = ['Mexico', 'México']
    if(tipousuario == "VICEPRESIDENTE LA"):
        dfp = dfp[dfp.pais.isin(LA_list)]
    
    if(tipousuario == "GERENTE REGIONAL"):
        dfp = dfp[dfp.pais.isin(Mexico_list)]

    if(tipousuario == "GERENTE DE PLANTA" or tipousuario == "GERENTE DE PLANTAS PLUS"):
        dfp = dfp[dfp.nombre == "Yazaki Benito Juarez"]



    fig.add_trace(go.Scattermapbox(
            lat=dfp.lat,
            lon=dfp.lng,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(0, 200, 0)',
                opacity=0.7,
            ),
            text=dfp.nombre,
            hoverinfo='text'
        ))

    if kwargs["session_state"]["planta_id"]:
        dff = dfp[dfp.nombre == "Yazaki Benito Juarez"]
        fig.add_trace(go.Scattermapbox(
                lat=dff.lat,
                lon=dff.lng,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=17,
                    color='rgb(255, 0, 0)',
                ),
                text=dff.nombre,
                hoverinfo='text'
            ))
    
    #for ciudad in selected:
    #    dff = dfp[dfp["ciudad"] == ciudad]
        

    """
    fig.add_trace(go.Scattermapbox(
            name="Relevante",
            lat=[31.6104556],
            lon=[-106.3969567],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7,
            ),
            text=["Yazaqui planta 1"],
            hoverinfo='text'
        ))
    """

    myzoom=0.5
    mycenterlat=0
    mycenterlng=-205

    #zoomceo=1
    #centerceo=-190
    if(tipousuario == "VICEPRESIDENTE LA"):
        myzoom=1.8
        mycenterlat=-10.2835133
        mycenterlng=-72.7243782
    
    if(tipousuario == "GERENTE REGIONAL"):
        myzoom=3.9
        mycenterlat=24.2578675
        mycenterlng=-101

    if(tipousuario == "GERENTE DE PLANTA" or tipousuario == "GERENTE DE PLANTAS PLUS"):
        myzoom=10.5
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
    print("map updated")
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('pie-rotacion', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()
    labels = ['Rotacion', 'Normal']
    values = [25, 75]
    valuesGeneral = [2, 98]
    colors = ["#36A1DD", "#74CEFF"]

    if kwargs["session_state"]["planta_id"]:
        fig.add_trace(go.Pie(labels=labels, values=values))
    else:
        fig.add_trace(go.Pie(labels=labels, values=valuesGeneral))

    fig.update_layout(
        autosize=True,
        showlegend=True,
        margin = dict(l = 16, r = 16, t =16, b = 16),
    )
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('pie-ausentismo', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()
    
    labels = ['Ausentismo', 'Asistencia']
    values = [25, 75]
    valuesGeneral = [3, 97]
    if kwargs["session_state"]["planta_id"]:
        fig.add_trace(go.Pie(labels=labels, values=values))
    else:
        fig.add_trace(go.Pie(labels=labels, values=valuesGeneral))

    fig.update_layout(
        autosize=True,
        showlegend=True,
        margin = dict(l = 16, r = 16, t = 16, b =16),
    )
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('bar-capacitacion', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()

    #jhbdiuwe bdweidbedbw ediewub diedbweidubei uwebdewuide wdwed

    #datos Generales
    normalGeneral = ['C-TPAC', "Recorrido inteligente", "Control de accesos", "Liderasgo y calidad", "LLenado de bitacoras", "Acoso sexual", "Revisión de gafete", "Detección de sospechosos", "Condiciones inseguras"]
    normalGeneralValues = [15, 7, 11, 1, 5, 1, 1, 1, 1]
    relevanteGeneral = ["Sistemas de emergencia", "Sustancias prohibidas", "Llamadas de extorsión"]
    relevanteGeneralValues = [0, 0, 0]

    #datos especificos
    normalCeo = ['C-TPAC', "control de accesos", "LLenado de bitacoras"]
    normalCeoValues = [1, 1, 1]
    relevanteCeo = ["Sistemas de emergencia", "Recorrido inteligente", "Liderasgo y calidad",  "Sustancias prohibidas", "Llamadas de extorsión", "Acoso sexual", "Revisión de gafete", "Detección de sospechosos", "Condiciones inseguras"]
    relevanteCeoValues = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    if kwargs["session_state"]["planta_id"]:
        fig.add_trace(go.Bar(name="Normal", x=normalCeo, y=normalCeoValues, text=normalCeoValues, textposition='outside'))
        fig.add_trace(go.Bar(name="Relevante", x=relevanteCeo, y=relevanteCeoValues, text=relevanteCeoValues, textposition='outside'))
    else:
        fig.add_trace(go.Bar(name="Normal", x=normalGeneral, y=normalGeneralValues, text=normalGeneralValues, textposition='outside'))
        fig.add_trace(go.Bar(name="Relevante", x=relevanteGeneral, y=relevanteGeneralValues, text=relevanteGeneralValues, textposition='outside'))

    fig.update_layout(
        autosize=True,
        showlegend=True,
        yaxis_title="<b>Capacitación mensual</b>",
        margin = dict(l = 16, r = 16, t = 16, b =16),
    )
    
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('bar-cobertura', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()
    
    dias = ["Lunes", "Martes", "Miercoles", "Juevez", "Viernes"]
    porcentaje = [75, 75, 75, 75, 75, 75, 75]
    porcentaje2 = [75, 75, 75, 75, 75, 75, 75]

    porcentajeGeneral = [91, 100, 98, 105, 98, 98, 99]
    porcentaje2General = [91, 100, 100, 100, 98, 98, 99]

    colores = ["#A9DFF6", "#A9DFF6", "#A9DFF6", "#A9DFF6", "#A9DFF6", "#A9DFF6", "#A9DFF6"]
    coloresGeneral = ["#A9DFF6", "#A9DFF6", "#A9DFF6", "#990000", "#A9DFF6", "#A9DFF6", "#A9DFF6"]

    if kwargs["session_state"]["planta_id"]:
        fig.add_trace(go.Bar(name="Real", x=dias, y=porcentaje, marker_color=colores, text=porcentaje, textposition='outside'))
        fig.add_trace(go.Scatter(name="Debe ser", x=dias, y=porcentaje2))
    else:
        fig.add_trace(go.Bar(name="Real", x=dias, y=porcentajeGeneral, marker_color=coloresGeneral, text=porcentajeGeneral, textposition='outside'))
        fig.add_trace(go.Scatter(name="Debe ser", x=dias, y=porcentaje2General))

    fig.update_layout(
        autosize=True,
        showlegend=True,
        xaxis_title="<b>Día</b>",
        yaxis_title="<b>Cobertura</b>",
        margin = dict(l = 16, r = 16, t = 16, b =16),
    )
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('porcentaje-cobertura', 'children'), [Input('selected-values', 'value')])
def update_output_div(selected, *args, **kwargs):
    if kwargs["session_state"]["planta_id"]:
        return "75%"
    else:
        return "98%"


@app.expanded_callback(Output('table-plantas', 'children'), [Input('selected-values', 'value')])
def update_output_div(selected, *args, **kwargs):

    userdict = kwargs["session_state"]["userdict"]
    tipousuario = userdict["tipousuario"]
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
    
    #filtro por rol
    plantas = Planta.objects.filter(cliente__id=userdict["cliente_id"]).values()
    if plantas.count() == 0:
        return "NO hay Plantas"
    dfp = pd.DataFrame.from_records(plantas)
    LA_list = ['México', 'México', 'Colombia', "Argentina", "Brasil"]
    Mexico_list = ['Mexico', 'México']
    if(tipousuario == "VICEPRESIDENTE LA"):
        dfp = dfp[dfp.pais.isin(LA_list)]
    
    if(tipousuario == "GERENTE REGIONAL"):
        dfp = dfp[dfp.pais.isin(Mexico_list)]

    if(tipousuario == "GERENTE DE PLANTA" or tipousuario == "GERENTE DE PLANTAS PLUS"):
        dfp = dfp[dfp.nombre == "Yazaki Planta 1"]

    for ciudad in selected:
        dff = dfp[dfp["ciudad"] == ciudad]

        #dff = dfp
        #print(dff)
        i = 0
        if not dff.empty:
            while i < len(dff):
                #print(dff.nombre.iloc[i])
                if not dff.nombre.iloc[i]:
                    i += 1
                    continue
                print("Nombre planta: "+dff.nombre.iloc[i])
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

                                        
    
