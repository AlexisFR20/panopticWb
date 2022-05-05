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
from plotly.subplots import make_subplots
import dash_dangerously_set_inner_html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"})

app = DjangoDash('dash_zona0', meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

incidentes = Incidente.objects.values()
dfi = pd.DataFrame.from_records(incidentes)
#print(dfi)

def serve_layout(**kwargs):
    incidentes = Incidente.objects.values()
    dfi = pd.DataFrame.from_records(incidentes)

    cards = []

    """
        <div class="card mb-10" >
            <div class="card-header" style="background-color: #eee">
                Indice delictivo
            </div>
            <div class="card-body row">
                <div class="card col-md-3">
                    <div class="card-body row">
                        <div class="col-sm-3"><img src="/static/core/assets/images/blue_pin.png" class="img-fluid" height="40px"></img></div>
                        <div class="col-sm-9">
                            <p>Juarez</p>
                            <p><h3>
    ''' + str(dfi.cantidad.sum()) + '''
                            </h3></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <br>
        """

    for pais in dfi.pais.unique():
        suma = dfi[dfi["pais"] == pais].cantidad.sum()
        cards.append(html.Div([
            html.Div([
                html.Div(html.Img(src="/static/core/assets/images/blue_pin.png", className="img-fluid", style={"height": "40px"}), className="col-sm-3"),
                html.Div([
                    html.P(pais),
                    html.H3(suma)
                ], className="col-sm-9")
            ], className="card-body row"),
        ], className="card", style={"width": "18rem"}))

    return html.Div([ 
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
        <link href="/static/core/base.css" rel="stylesheet">
        <link href="/static/core/assets/css/styles.css" rel="stylesheet"> 
    '''),
        html.Div([
            html.Div([
                dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
            '''),
            html.Div([dcc.Dropdown(id="selected-values", multi=True, 
                               options=[{'label': i, 'value': i} for i in dfi.tipo.unique()],
                                value=dfi.tipo.unique(),
                                )],
                                className="row", style={"display": "none", "width": "60%", "margin-left": "auto",
                                                        "margin-right": "auto"}),
            ], className="col-md-6", id="algo1"),
            html.Div([
                 dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
            '''),
            ], className="col-md-6", id="algo2"),
            
        ], id="innerZ", className="row"), 
        
        html.Div([
            html.Div([
                dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''

            <div id="indicesDelincuenciales" class="mb-3 card">
                    <div class="card-header-tab card-header-tab-animation card-header">
                        <div class="card-header-title">
                            <i class="header-icon bgp-color-rojo pe-7s-note2"></i>
                            Índices Delincuenciales
                        </div>
                        <div class="btn-actions-pane-right">
                            <small class="bgp-color-naranja opacity-9 pr-1">En los últimos 7 días</small>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="tab-content">
                            <h6 class="bgp-color-rojo negrita text-uppercase font-size-md">Ciudad Juárez</h6>
                            <!-- Listado de ïconos delincuenciales -->
                            <ul class="rm-list-borders rm-list-borders-scroll list-group list-group-flush">
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bck-white">
                                                <img width="42" class="rounded-circle icod-bw" src="/static/core/assets/images/icons/delincuenciales-color/casa-habitacion.png" alt="Casa Habitación">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Casa Habitación</div>
                                                <div class="widget-subheading">Incremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">20%</small>
                                                    <span>19</span>
                                                    <small class="text-danger pl-2">
                                                        <i class="fa fa-arrow-up"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle icod-bw" src="/static/core/assets/images/icons/delincuenciales-color/homicidio.png" alt="Homicidio">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Homicidio</div>
                                                <div class="widget-subheading">Incremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">40%</small>
                                                    <span>32</span>
                                                    <small class="text-danger pl-2">
                                                        <i class="fa fa-arrow-up"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle icod-bw" src="/static/core/assets/images/icons/delincuenciales-color/secuestro.png" alt="Secuestro">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Secuestro</div>
                                                <div class="widget-subheading">Decremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">10%</small>
                                                    <span>25</span>
                                                    <small class="text-success pl-2">
                                                        <i class="fa fa-arrow-down"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle icod-bw" src="/static/core/assets/images/icons/delincuenciales-color/carjacking.png" alt="Carjacking">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Carjacking</div>
                                                <div class="widget-subheading">Incremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">4%</small>
                                                    <span>21</span>
                                                    <small class="text-danger pl-2">
                                                        <i class="fa fa-arrow-up"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle" src="/static/core/assets/images/icons/delincuenciales-color/asalto-a-negocios.png" alt="Asalto a Negocios">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Asalto a Negocios</div>
                                                <div class="widget-subheading">Decremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">12%</small>
                                                    <span>9</span>
                                                    <small class="text-success pl-2">
                                                        <i class="fa fa-arrow-down"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle" src="/static/core/assets/images/icons/delincuenciales-color/transeuntes.png" alt="Transeúntes">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Transeúntes</div>
                                                <div class="widget-subheading">Decremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">22%</small>
                                                    <span>17</span>
                                                    <small class="text-success pl-2">
                                                        <i class="fa fa-arrow-down"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle" src="/static/core/assets/images/icons/delincuenciales-color/auto-partes.png" alt="Auto Partes">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Auto Partes</div>
                                                <div class="widget-subheading">Incremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">3%</small>
                                                    <span>11</span>
                                                    <small class="text-danger pl-2">
                                                        <i class="fa fa-arrow-up"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle" src="/static/core/assets/images/icons/delincuenciales-color/tiendas-establecidas.png" alt="Tiendas Establecidas">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Tiendas Establecidas</div>
                                                <div class="widget-subheading">Decremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">1%</small>
                                                    <span>3</span>
                                                    <small class="text-success pl-2">
                                                        <i class="fa fa-arrow-down"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle" src="/static/core/assets/images/icons/delincuenciales-color/hotel.png" alt="Hotel">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Hotel</div>
                                                <div class="widget-subheading">Incremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">2%</small>
                                                    <span>11</span>
                                                    <small class="text-danger pl-2">
                                                        <i class="fa fa-arrow-up"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li class="list-group-item">
                                    <div class="widget-content pad-lista-iconos-delincuenciales bgp-grislight">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left mr-3 bgp-white">
                                                <img width="42" class="rounded-circle" src="/static/core/assets/images/icons/delincuenciales-color/aeropuerto.png" alt="Aeropuerto">
                                            </div>
                                            <div class="widget-content-left">
                                                <div class="widget-heading">Aeropuerto</div>
                                                <div class="widget-subheading">Decremento </div>
                                            </div>
                                            <div class="widget-content-right">
                                                <div class="font-size-xlg text-muted">
                                                    <small class="bgp-color-naranja opacity-9 pr-1">1%</small>
                                                    <span>11</span>
                                                    <small class="text-success pl-2">
                                                        <i class="fa fa-arrow-down"></i>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

            '''),
            ], className="col-md-4 col-xs-12", id="tabla_indicadores"),
            html.Div(dcc.Graph(id="my-barchart"), className="col-md-8 col-xs-12")
        ], id="inner3_indices", className="row"),
])

app.layout = serve_layout

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
                "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
                "http://panoptic.iottechnologies.mx/static/core/assets/css/styles.css" ]

for css in external_css:
    app.css.append_css({"external_url": css})
"""
@app.expanded_callback(Output('my-graph', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):

    fig = go.Figure()
    incidentes = Incidente.objects.values()
    dfi = pd.DataFrame.from_records(incidentes)
    frames = []
    #mapa de calor delincuencial
    for indicador in selected:
        dfindi = dfi[dfi["tipo"] == indicador]
        frames.append(dfindi)
    dffinal = pd.concat(frames)
    fig.add_trace(go.Densitymapbox(lat=dffinal.lat, lon=dffinal.lng, radius=5, text=dffinal.tipo, hovertemplate="%{text} <br>(%{lat}, %{lon})"))
    #print("muestra" + str(dfindi.tipo))
                                 

    fig.update_layout(
        title='Indice delictivo',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        height=500,
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        mapbox=go.layout.Mapbox(
            accesstoken="pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ",
            bearing=0,
            pitch=0,
            zoom=1.2,
            style='stamen-terrain',
            center=go.layout.mapbox.Center(
            lat=0,
            lon=-195
            )
        ),
    )


    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": fig.data,
            "layout": fig.layout}

"""

@app.expanded_callback(Output('my-barchart', 'figure'), [Input('selected-values', 'value')])
def update_figure(selected, *args, **kwargs):
    #grafica de barras para incidencias con porcentajes
    #fig = go.Figure()

        
    userdict = kwargs["session_state"]["userdict"]
    tipousuario = userdict["tipousuario"]
    print("tipousuario: "+str(tipousuario))

    incidentes = Incidente.objects.values()
    dfi = pd.DataFrame.from_records(incidentes)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    counts = []
    indicators = []
    indicatorColors = []
    porcentajes = []
    colors = {
                "casa_habitacion": '#E0AD13',
                "secuestro" : "#37536d",
                "carjacking" : "#3e5ba9",
                "asalto_negocio" : "#0097a7",
                "homicidio" : "#D97402",
                "asalto_transeuntes" : "#009d57",
                "autopartes" : "#d92550",
                "aeropuerto" : "#a6194a",
                "hotel": "#a6194a",
                "lesiones": '#E0AD13',
                "violencia_familiar" : "#37536d",
                "robo_vehiculo" : "#3e5ba9",
                "narcomenudeo" : "#0097a7",
        }
    for indicador in selected:
        dfindi = dfi[dfi["tipo"] == indicador]
        indicators.append(indicador)
        counts.append(dfindi.cantidad.sum())
        p = (100/dfi.cantidad.sum())*dfindi.cantidad.sum()
        porcentajes.append(p)
        #indicatorColors.append(colors[indicador])

    fig.add_trace(go.Bar(name="Hechos Delictivos", x=indicators, y=counts, marker={'color': "#5588ff"}))        

    fig.add_trace(go.Line(name="Porcentajes", x=indicators, y=porcentajes, marker={'color': "#dc3545", "size": 10}), secondary_y=True,)
        
    fig.update_layout(
            title="Índice delictivo",
            height=920,
        )                       
    fig.update_yaxes(title_text="<b>Hechos Delictivos</b> cantidades", secondary_y=False)
    fig.update_yaxes(title_text="<b>Porcentaje</b>", secondary_y=True)

    
    
        #trace.append(go.bar(x=dff["Date"], y=dff[type], name=text[type], mode='lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {
        "data": fig.data,
        "layout": fig.layout
        }

             
    
