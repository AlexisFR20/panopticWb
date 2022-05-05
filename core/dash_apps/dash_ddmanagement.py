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

app = DjangoDash('dash_ddmanagement', meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

plantas = Planta.objects.values()
dfp = pd.DataFrame.from_records(plantas)

app.layout = html.Div([ 
    
    html.Div([dcc.Dropdown(id="selected-values", multi=True, 
                               options=[{'label': i, 'value': i} for i in dfp.ciudad.unique()],
                                value=dfp.ciudad.unique(),
                                )],
                                className="row", style={"display": "none", "width": "60%", "margin-left": "auto",
                                                        "margin-right": "auto"}),

    html.Div([dcc.Dropdown(id="tipo-vista", 
                               options=[
                                   {'label': "Vista Específica", 'value': "especifica"},
                                   {'label': "Vista General", 'value': "general"},
                                ],
                                value="general",
                                clearable=False,
                                )],
                                className="row", style={"display": "block",
                                                        "margin-left": "16px", "width": "300px"}),
    html.Div([
        html.Div([
            html.Div( html.Div([
                html.Div("CARGAS EN RUTA", className="card-header"),
                html.Div(html.Span("5000", className="align-middle"), className="card-body h2 text-center",),
            ], className="card", style={'height': '300px'}), className="col-md-6"),
            html.Div( html.Div([
                html.Div("TIEMPOS REAL/ESTIMADO", className="card-header"),
                html.Div(dcc.Graph(id="bar-estimados"), className="card-body"),
            ], className="card", style={'height': '300px'}), className="col-md-6"),
            html.Div( html.Div([
                html.Div("RUTAS DE RIESGO", className="card-header"),
                html.Div(
                    html.Table([
                        html.Tr([
                            html.Td("ruta de riesgo #1"),
                            html.A("Ver mas", **{"data-toggle":"collapse", "role":"button", "aria-expanded":"false", "aria-controls":"datos_trayecto"}, className="btn btn-primary", href="#datos_trayecto")
                        ]),
                    ], className="table table-striped"), 
                    id="rutas_riesgo", 
                    className="card-body", style={"overflow-y": "scroll"}
                ),
            ], className="card", style={'height': '300px'}), className="col-md-6"),
            html.Div( html.Div([
                html.Div("BINOMIOS", className="card-header"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(src="/static/core/assets/images/manejador.png", className="img-fluid"),
                            html.Div(html.B("Nombre manejador"), style={"background-color": "#ddd"}),
                            html.Div("Jairo Vega"),
                        ], className="col-sm-6"),
                        html.Div([
                            html.Img(src="/static/core/assets/images/perro.png", className="img-fluid"),
                            html.Div(html.B("K9"), style={"background-color": "#ddd"}),
                            html.Div("Rayo"),
                            html.Div(html.B("Puesto"), style={"background-color": "#ddd"}),
                            html.Div("Narcoticos"),
                        ], className="col-sm-6"),
                    ], className="row")
                ], id="binomios", className="card-body"),
            ], className="card", id="binomios_container", style={'height': '300px', "overflow-y": "scroll"}), className="col-md-6"),
        ], className="col-md-6 row"),
        html.Div([
            html.Div( html.Div([
                html.Div("Mapa rutas", className="card-header"),
                html.Div([
                    dcc.Graph(id="my-graph"),
                    html.Div([

                        html.Div([
                            html.Div([
                                html.Span(html.B("Datos del trayecto")),
                                html.A("X", **{"data-toggle":"collapse", "role":"button", "aria-expanded":"false", "aria-controls":"datos_trayecto"}, className="close float-right", href="#datos_trayecto")
                            ], className="card-header"),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Table([
                                            html.Tbody([
                                                html.Tr([
                                                    html.Th("Nombre", id="trayecto_chofer"),
                                                    html.Td("Jorge Alvarez"),
                                                ]),
                                                html.Tr([
                                                    html.Th("Matrícula", id="trayecto_matricula"),
                                                    html.Td("318-SSS-3011"),
                                                ]),
                                                html.Tr([
                                                    html.Th("Destino", id="trayecto_destino"),
                                                    html.Td("Planta 3 Yazaki"),
                                                ]),
                                                html.Tr([
                                                    html.Th("Compañia", id="trayecto_compañia"),
                                                    html.Td("Yazaki"),
                                                ]),
                                                html.Tr([
                                                    html.Th("Notificaciones", id="trayecto_notificaciones"),
                                                    html.Td("Hubo una falla mecanica"),
                                                ])
                                            ])
                                        ], className="table table-striped table-sm table-condensed", style={"font-size": "12px"})
                                    ], className="col-sm-8"),
                                    html.Div( html.Img(src="/static/core/assets/images/conductor.png", className="img-fluid"), className="col-sm-4", style={"padding": "4px", "paddimg": "4px"})

                                ], className="row")
                            ], className="card-body", style={"padding": "8px"})

                        ], id="chofer_container", className="card"),

                    ], id="datos_trayecto", className="collapse",  style={"position": "absolute", "bottom": "16px", "left": "16px", "width": "350px", "opacity": "0.9" }),
                    
                ], className=""),
            ], className="card", style={'height': '600px'}), className="col-md-12"),
        ], className="col-md-6"),



    ], className="row", style={"margin-top": "32px"}),

    html.Div( html.Div([
        html.Div("", className="card-header"),
        html.Div([
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("#FOLIO"),
                        html.Th("TRANSPORTISTA"),
                        html.Th("VALOR"),
                        html.Th("SELLO"),
                        html.Th("REVISIÓN 18 PUNTOS"),
                        html.Th("K9"),
                        html.Th("COMENTARIOS"),
                        html.Th("STATUS"),
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(html.H3("A130")),
                        html.Td("Arnés"),
                        html.Td("2.5M"),
                        html.Td(html.H3("NO")),
                        html.Td(html.H3("SI")),
                        html.Td(html.H3("SI")),
                        html.Td("No fue el que coloca los sellos. se coloco candado y corbata"),
                        html.Td(html.H3("RELEVANTE", style={"color": "red"})),
                    ])
                ])
            ], className="table table-striped")
        ], className=""),
    ], className="card"), className="col-md-12", style={"margin-top": "32px"}),
    
])

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", 
                "https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css",
                "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
                "http://panoptic.iottechnologies.mx/static/core/assets/css/styles.css"]
external_js = ["https://code.jquery.com/jquery-3.4.1.min.js", 
                "https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js",
                "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"]

for css in external_css:
    app.css.append_css({"external_url": css})
for js in external_js:
    app.scripts.append_script({"external_url": js})



@app.expanded_callback(Output('my-graph', 'figure'), [Input('selected-values', 'value'), Input('tipo-vista', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()

    userdict = kwargs["session_state"]["userdict"]
    tipousuario = userdict["tipousuario"]
    
    for ciudad in selected:
        dff = dfp[dfp["ciudad"] == ciudad]
        fig.add_trace(go.Scattermapbox(
            lat=[28.648816, 30.615544, 31.671143],
            #lat=dff.lat,
            lon=[-106.070757, -106.514400, -106.425036],
            #lon=dff.lng,
            mode='markers+lines+text',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7,
            ),
            #text=dff.nombre,
            text=["Chihuahua", "Villahumada", "Juarez"],
            hoverinfo='text'
        ))

    myzoom=0
    mycenterlat=0
    mycenterlng=-205

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
        title='Planta Yazaki - Transporte',
        hovermode='closest',
        autosize=True,
        height=550,
        showlegend=False,
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        mapbox=go.layout.Mapbox(
            accesstoken="pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ",
            bearing=0,
            pitch=0,
            zoom=myzoom,
            style='streets',
            center=go.layout.mapbox.Center(
                lat=mycenterlat,
                lon=mycenterlng
            )
        ),
    )
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

@app.expanded_callback(Output('bar-estimados', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    fig = go.Figure()

    trailers = [1,2,3,4,5,6,7,8,9]

    fig.add_trace(go.Bar(name="Reales", x=trailers, y=[4,3,5.5,1,6,10,8,12,13]))
    fig.add_trace(go.Scatter(name="Estimado", x=trailers, y=[4,3,5,1,6,10.5,8,12.5,13]))

    fig.update_layout(
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        legend_orientation="h",
        height=200,
    )

    return {"data": fig.data,
        "layout": fig.layout}
'''
@app.callback(Output('rutas_riesgo', 'children'), [Input('selected-values', 'value')])
def update_output_div_rutas():
    cont = ""
    

    return cont
'''
    
