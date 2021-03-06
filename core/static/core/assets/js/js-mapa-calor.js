//JS Mapa de Calor 
let map, heatmap;

var gDefault = [
            'rgba(70, 0, 0, 0)',
            'rgba(0, 255, 0, 1)',
            'rgba(255, 255, 0, 1)',
            'rgba(255, 165, 0, 1)',
            'rgba(255, 0, 0, 1)',
            'rgba(153, 50, 204, 1)',
            'rgba(165, 42, 42, 1)'
        ];

var color = 'azul';

// Extracción de movimientos finalizados
function callAjax(planta_id) {
    var dContent = '';

    // Inserción de Información de Movimiento Finalizados
    $.ajax({
        async: false,
        url:  '{% url "administrador:ajax_heatmap_movs_finalizados" %}',
        data: { 'planta_id': planta_id },
        datatype: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',            
        success: function (mf) {
            var ty =planta_id;
            var el = null;
            if (ty == 2) {
                //console.log('Lista de Movimientos Finalizados en callAjax ...');
                var m_final_Array = mf.movs_finalizados;   
                var parrContent = null;                 
                for (i = 0; i < m_final_Array.length; i++) {                      
                    //console.log(m_final_Array[i].fields.nombre);                      
                    el = "finalizados_mov_"+ty.toString();
                    //console.log('el:', el);
                    $(el).text(m_final_Array[i].fields.nombre);
                    parrContent = m_final_Array[i].fields.nombre + '<br/>';
                    el = null;
                } // end for              
                
            }   // end if     
            dContent = parrContent        
        }
    });  

    return dContent;
}


function initMap() {
    // Inicialización de mapa de calor
    map = new google.maps.Map(document.getElementById("mapacalor"), {
        zoom: 12,
        center: {lat: 31.6540214, lng: -106.5189754},
        mapTypeId: "roadmap"
    });    

    // Integración de marcadores de unidades de negocio y de ventana de información respectivas
    setMarkers(map);

    // Generación de puntos de calor a partir de incidentes delictivos y de problemas en Unidades de Negocios
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map,
        radius: 50,
        gradient: gDefault
    });      
}

// Cambio de color en puntos de calor
function changeGradient() {
        const gradient = [
            'rgba(255, 0, 0, 0)',
            'rgba(255, 0, 0, 1)',
            'rgba(255, 255, 0, 1)',
            'rgba(0, 255, 0, 1)',
            'rgba(173, 255, 47, 1)',
            'rgba(255, 0, 0, 1)'    
        ];

        const gDefault = [
            'rgba(70, 0, 0, 0)',
            'rgba(0, 255, 0, 1)',
            'rgba(255, 255, 0, 1)',
            'rgba(255, 165, 0, 1)',
            'rgba(255, 0, 0, 1)',
            'rgba(153, 50, 204, 1)',
            'rgba(165, 42, 42, 1)' 
        ];
        
        if (color == 'rojo') {
            heatmap.set("gradient", gDefault);
            color='azul';
        } else if (color == 'azul') {
            heatmap.set("gradient", gradient);
            color='rojo';
        }
        
}

// Cambio en el radio de puntos de mapa de calor
function changeRadius() {
  heatmap.set("radius", heatmap.get("radius") ? null :50);
}

// Iteración de puntos - coordenadas de registros delictivos
function getPoints() {
        return [
            {% for o in incidentes %}            
            new google.maps.LatLng({{ o.lat}}, {{ o.lng }}),                
            {% endfor %}                    
        ];
}

function setMarkers(map) {        

    var ico_plantas = {             
        'optimo': { 'img': "{% static 'core/assets/images/planta-marker-ico.png' %}" },        
        'estable': { 'img': "{% static 'core/assets/images/planta-marker-ico-estable.png' %}" },        
        'relevante': { 'img': "{% static 'core/assets/images/alert-icon-planta-relevante.gif' %}" }
    };    

    
    var czindex = 1000;    // Los marcadores se generan a partir de la capa 1000    
    var infowindow = new google.maps.InfoWindow({ // Inicialización de instancia de InfoWindow
        content: ''
    });
    
    {% for planta in plantas %}      
        var planta_id = {{planta.id}};
        var planta_nombre = '{{planta.nombre}}';         
        var planta_foto = '{{planta.foto}}';        
        var planta_gradio = {{planta.gradio}};
        var planta_lat = {{ planta.lat}};
        var planta_lng = {{ planta.lng}};
        var estatus_cobertura_estable = {{planta.estatus_cobertura_estable}};
        var estatus_cobertura_relevante = {{planta.estatus_cobertura_relevante}};
        var criterioPlantaEstable = estatus_cobertura_estable;
        var criterioPlantaRelevante = estatus_cobertura_relevante;        
        var planta_cobertura = getCobertura(planta_id);
        var vp_plantaEstatus = '{{ planta.status }}';        
        var cliente_id = {{cliente.id}};
        var gPlantaEstatusColor = {'optimo': '#78916e', 'medio': '#feffc3', 'relevante': '#9D292A'};        
        
        // Feed de Ajax
        function getPonderacion(planta_id) {            
            var ponderacion=0;            
            $.ajax({
                async: false,
                url:  '{% url "administrador:get_ajax_ponderacion" %}',
                data: {'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',            
                
                success: function (result) {                           
                    ponderacion = result.ponderacion;                                 
                }
            }); // end ajax    

            ponderacion = Math.round(parseFloat(ponderacion));
            return ponderacion;
        }

        function getCapacitacion(planta_id) {            
            var capacitacion=null;            
            $.ajax({
                async: false,
                url:  '{% url "administrador:get_ajax_capacitacion" %}',
                data: {'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',            
                
                success: function (result) {                    
                    capacitacion = result.capacitaciones[0] + "%";                  
                }
            }); // end ajax    
            return capacitacion;
        }

        function getCobertura(planta_id) {                  
            var cobertura=null;            
            $.ajax({
                async: false,
                url:  '{% url "administrador:get_ajax_cobertura_planta" %}',
                data: {'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',            
                
                success: function (result) {                    
                    //console.log('cobertura', cobertura);
                    cobertura = result.cobertura;                       
                }
            }); // end ajax    
            return cobertura;
        }

        function getRondines(planta_id) {
            var rondines=null;            
            $.ajax({               
                async: false,
                url:  '{% url "administrador:get_ajax_ceo_numero_rondines" %}',
                data: {'planta_id': planta_id },
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',            
                
                success: function (result) {  
                  rondines = result.rondines;                  
                }
            });  // end ajax  
            return rondines;
        }

        function getIncidentesRondines(planta_id) {
            var incidentesr = null;
            $.ajax({
                async: false,
                url: '{% url "administrador:get_ajax_ceo_numero_incidentes_rondines" %}',
                data: {'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',

                success: function (result) {
                    incidentesr = result.incidentes;
                }
            });
			console.log("INCIDENTES RONDINES");
			console.log(incidentesr);
            return incidentesr;
        }

        function get18puntos(planta_id) {
            let puntos = null;
            $.ajax({
                async: false,
                url: '{% url "administrador:get_ajax_ceo_18_puntos" %}',
                data: {'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',

                success: function (result) {
                    puntos = result.puntos;
                }
            });
            return puntos;
        }

        function getRecomendaciones(planta_id) {
            var recomendaciones = null;
            $.ajax({
                async: false,
                url: '{% url "administrador:get_ajax_ceo_recomendaciones" %}',
                data: {'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',

                success: function (result) {
                    recomendaciones = result;
                }
            });
            console.log(recomendaciones);
            return recomendaciones;
        }

        function getEmpleadoSG(planta_id) {
            var empleadosg=null;            
            $.ajax({               
                async: false,
                url:  '{% url "administrador:get_ajax_ceo_personal_sin_gafete" %}',
                data: {'planta_id': planta_id },
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',            
                
                success: function (result) {                    
                    empleadosg = result.ambos;                  
                }
            });  // end ajax  
            return empleadosg;
        }

        function getVisitantes(planta_id) {
            var visitantes=0;            
            $.ajax({               
                async: false,
                url:  '{% url "administrador:get_ajax_num_visitantes" %}',
                data: {'planta_id': planta_id },
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; charset=utf-8',            
                
                success: function (result) {              
                    console.log('Num de Visitantes');
                    console.log(visitantes);
                    visitantes = result.visitantes;                  
                }
            });  // end ajax  
            return visitantes;
        }

        function getVulnerabilidadGeneral(planta_id, cliente_id, dgVulnerabilidad) {
            var chartObj = null;            
            $.ajax({
                async: false,
                url:  '{% url "administrador:ajax_analisis_de_riesgo_vulnerabilidadgral" %}',
                data: { 'cliente_id': cliente_id, 'planta_id': planta_id},
                datatype: 'json',
                type: 'GET',
                contentType: 'application/json; char=utf-8',
                dataType: 'json',
                success: function (result) {
					console.log("HERE ONIX");
                    console.log("result", result);                    
                    
                    var labelsVul = ["Entorno", "Infraestructura", "Seguridad Operativa", "Seguridad Electrónica", "Logistica"];
                    var valVul = [result["v_entorno"], result["v_infraestructura"], result["v_seguridad_operativa"], result["v_seguridad_electronica"], result["v_logistica"]];
                    var vulGral = (result["v_entorno"]+result["v_infraestructura"]+result["v_seguridad_operativa"]+result["v_seguridad_electronica"]+result["v_logistica"])/5;

                    console.log('Suma V: ', vulGral);
                    vulGral = vulGral.toFixed(2);

                    catEntornoAvg = result["cat_entorno_avg"];                    
                    catInfraAvg = result["cat_infraestructura_avg"];                    
                    catSegopAvg = result["cat_seg_operativa_avg"];                    
                    catSegelecAvg = result["cat_seg_electrica_avg"];                    
                    catLogisticaAvg = result["cat_logistica_avg"];                    

                    var optionsVulGral = {
                        title: {
                          text: 'Vulnerabilidad General',
                          align: 'left'
                        },
                        series: [{
                            name: 'Vulnerabilidad General',
                            data: [100-vulGral, vulGral],

                        }],
                        chart: {
                            type: 'bar',
                            height: 150
                        },
                        colors: ['#D97402','#999'],
                        labels: ["Seguridad", "Vulnerabilidad"],
                        legend: {
                            position: 'bottom'
                        },
                        plotOptions: {
                            bar: {
                                horizontal: true,
                                tal: false,                                
                                distributed: true
                            },
                        },
                         
                    } //end optionsVulGral                                  
                    
                    setTimeout(function(){       
                        setTimeout(function(){       
                            if ( $('[id^=apexchart]').length > 1 ) { 
                                var i;
                                for (i = 1; i < $('[id^=apexchart]').length; i++) {
                                    $('[id^=apexchart]').eq(i).remove(); 
                                } // for               
                            } // end if    
                        }, 500);  
                        $('.wait').hide();
                        $('.planta-wrapper-vulnerabilidad').show();
                        chartObj = new ApexCharts(document.querySelector("#"+dgVulnerabilidad), optionsVulGral);      
                        chartObj.render();                                                                   
                     }, 500);
                    
                }                
            }); // end ajax            
            return chartObj;            
        } // Vulnerabilidad General
        
        //Clonado de baseCustom
        var contentClone = $('#baseCustom').clone();
        contentClone.find('.escondido').removeClass('escondido');        
        
        var CircleColorFill = '#A6FF4D';
        var CircleColorLine = '#36D900';        
        
        if (planta_cobertura > criterioPlantaEstable) {  // En rango óptimo            
            estadoPlanta = ico_plantas.optimo.img;
            CircleColorFill = '#A6FF4D';
            CircleColorLine = '#36D900'; 
        } else if (planta_cobertura <= criterioPlantaEstable && planta_cobertura > criterioPlantaRelevante ) { // En rango estable
            estadoPlanta = ico_plantas.estable.img;
            CircleColorFill = '#FFBF00';
            CircleColorLine = '#D96D00'; 
        } else if (planta_cobertura <= criterioPlantaRelevante ) { // En rango relevante            
            estadoPlanta = ico_plantas.relevante.img;
            CircleColorFill = '#FF3737';
            CircleColorLine = '#B20000'; 
        }               
        
        var marker_{{planta.id}} = new google.maps.Marker({            
            position: new google.maps.LatLng(planta_lat, planta_lng),
            id : 'planta_' + planta_id,
            bounds: true,
            map: map,
            icon: estadoPlanta,                        
            title: planta_nombre.toUpperCase()            
        });

        marker_{{planta.id}}.setZIndex(czindex);
        
        // Generación de variables DINAMICAS
        var planta_id_{{planta.id}} = planta_id;        
        var planta_foto_{{planta.id}} = planta_foto;
        var cliente_id_{{planta.id}} = cliente_id;
        
        // Asignación de infoWindow
        google.maps.event.addListener(marker_{{planta.id}}, 'click', function() {  
            // Inserción de foto de Unidad de Negocio            
            var vp_nombre_{{planta.id}} = '{{planta.nombre}}';            
            var pic = planta_foto_{{planta.id}};                                
            contentClone.find('.planta-wrapper-vulnerabilidad').attr('id', 'planta-wrapper-vulnerabilidad_'+planta_id_{{planta.id}});
            
            if (pic != '' && pic != null) {                                    
                contentClone.find('.buHeader').css('backgroundImage', 'url(/media/'+pic);                
            } else {
                contentClone.find('.buHeader').css('backgroundImage',"url({% static 'core/assets/images/planta-default.jpg' %})");                
            }
            
            vp_cobertura_{{planta.id}} = getCobertura(planta_id_{{planta.id}});            

            if (vp_cobertura_{{planta.id}} > criterioPlantaEstable) {                 
                
                contentClone.find('.planta-cobertura').removeClass('bgp-color-rojo').removeClass('bgp-color-naranja').addClass('bgp-color-verde negrita');
                vp_plantaEstatusTxt_{{planta.id}} = 'Óptimo';

            } else if (vp_cobertura_{{planta.id}} <= criterioPlantaEstable && vp_cobertura_{{planta.id}} > criterioPlantaRelevante ) { 
                
                contentClone.find('.planta-cobertura').removeClass('bgp-color-verde').removeClass('bgp-color-rojo').addClass('bgp-color-naranja negrita');
                vp_plantaEstatusTxt_{{planta.id}} = 'Estable';

            } else if (vp_cobertura_{{planta.id}} <= criterioPlantaRelevante ) { 
                
                contentClone.find('.planta-cobertura').removeClass('bgp-color-verde').removeClass('bgp-color-naranja').addClass('bgp-color-rojo negrita');
                vp_plantaEstatusTxt_{{planta.id}} = 'Relevante';

            }      
              
            contentClone.find('.planta-cobertura').text(vp_cobertura_{{planta.id}}+'%');                 
            contentClone.find('.planta-ubicacion').text('{{planta.direccion}}, en {{planta.ciudad}}, {{planta.estado}}. {{planta.pais}}');
            contentClone.find('.planta-estatus').text(vp_plantaEstatusTxt_{{planta.id}});
            contentClone.find('.planta-ponderacion').text(getPonderacion(planta_id)); 
            contentClone.find('.planta-capacitacion').text(getCapacitacion(planta_id)); 
            //contentClone.find('.planta-rondines').text(getRondines({{planta.id}}) + "/" + getIncidentesRondines({{planta.id}}));  
            contentClone.find('.planta-empleadosg').text(get18puntos({{planta.id}}));        
            contentClone.find('.planta-visitantes').text(getVisitantes({{planta.id}}));        
            contentClone.find('.planta-nombre').text(vp_nombre_{{planta.id}} + ' | Cliente: {{planta.cliente}}');
            contentClone.find('.a_movs_activo').attr('id', 'linkActivo_'+planta_id_{{planta.id}});
            contentClone.find('.a_movs_activo').attr('planta-id', planta_id_{{planta.id}});
            contentClone.find('.a_movs_activo').attr('onClick','showMovimientosActivos({{planta.id}})');
            contentClone.find('.a_movs_finalizado').attr('onClick','showMovimientosFinalizados({{planta.id}})');
            contentClone.find('.a_movs_finalizado').attr('id', 'linkFinalizado_'+planta_id_{{planta.id}});        
            contentClone.find('.a_movs_regresar').attr('onClick','regresarMovimientos()');    
            $('#gVulnerabilidad_'+planta_id).remove();
            contentClone.find('#planta-wrapper-vulnerabilidad_'+planta_id_{{planta.id}}).html('<div id="gVulnerabilidad_'+planta_id+'"></div>');
            //contentClone.find('#row_recomendaciones').html('<tr><td>test</td></tr>');
            var rec = contentClone.find('#row_recomendaciones');                                                                                        
            
            let x = getRecomendaciones({{planta.id}});                                                                           
            var htmlinner = "";
            if (x != null){
                for(let i = 0; i < x.length; i++){
                    htmlinner+="<tr><th scope='row'><i class='header-icon lnr-checkmark-circle bgp-color-verde negrita'</i></th><td><div><span class='item-alerta'>"+ x[i].fields.descripcion+"</span></div></td></tr>";
                }
            } else{
htmlinner+="<tr><th scope='row'><i class='header-icon bgp-color-verde negrita'</i></th><td><div><span class='item-alerta'>No hay recomendaciones</span></div></td></tr>";
            }
            rec.html(htmlinner);
            var elemento = contentClone;
            var classObj_{{planta.id}} =elemento;                    
            
            getVulnerabilidadGeneral( planta_id_{{planta.id}}, cliente_id_{{planta.id}}, 'gVulnerabilidad_'+planta_id);    
            //getCapacitacion( planta_id_{{planta.id}});      
            //getRondines(planta_id_{{planta.id}});   
            //getEmpleadoSG(planta_id_{{planta.id}});
            Xcontent_{{planta.id}} = contentClone.html();
            infowindow.close();
            infowindow.setContent(Xcontent_{{planta.id}});
            infowindow.open(map,marker_{{planta.id}});            

            

        });      

        // Radio de Unidad de Negocio
        circle = new google.maps.Circle({
            map: map,
            radius: planta_gradio,
            fillColor: CircleColorFill,
            strokeColor: CircleColorLine
        });

        circle.bindTo('center', marker_{{planta.id}}, 'position');          
        
    {% endfor %}  
    
    
}   // end of setMarkers


function showMovimientosActivos(showMActivosPlantaID) {    
    // Usar ajax de movimientos Activos 
    $.ajax({
        url:  '{% url "administrador:ajax_heatmap_movs_activos" %}',
        data: { 'planta_id': showMActivosPlantaID },
        datatype: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',            
        success: function (ma) {
            if (ma.movs_activos.length == 0) {
                alert("La planta con ID " + showMActivosPlantaID + ', no tiene movimientos activos.');    
            } else {
                $('.sonbotones').hide();
                $('.mapacalorscroll').show();    
                $('.listaActivos').show();    
                var m_activo_Array = ma.movs_activos;   
                var parrContent = "";                 
                for (i = 0; i < m_activo_Array.length; i++) {                                          
                    parrContent = parrContent + '<a href="/backstage/movimientos/'+ m_activo_Array[i].pk +'"><span class="negrita truncate">Nombre:</span><span>' + m_activo_Array[i].fields.nombre + '</span><br/>' +  '<span class="negrita truncate">Fecha:</span><span>' + m_activo_Array[i].fields.fecha + '</span><hr/>';     
                } 
                
                console.log('parrContent', parrContent);
                $('.listaActivos').append(parrContent);

            } // end if
            console.log(ma);
        }
    });  

} // showMovimientosActivos

function showMovimientosFinalizados(showMFinalizadosPlantaID) {
    // Usar ajax de movimientos Finalizados 

    $.ajax({
        url:  '{% url "administrador:ajax_heatmap_movs_finalizados" %}',
        data: { 'planta_id': showMFinalizadosPlantaID },
        datatype: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',            
        success: function (mf) {

            if (mf.movs_finalizados.length == 0) {
                alert("La planta con ID " + showMFinalizadosPlantaID + ', no tiene movimientos finalizados.');    
            } else {
                $('.sonbotones').hide();
                $('.mapacalorscroll').show();    
                $('.listaFinalizados').show();    
                var m_final_Array = mf.movs_finalizados;   
                var parrContent = "";                 
                for (i = 0; i < m_final_Array.length; i++) {                                          
                    parrContent = parrContent + '<a href="/backstage/movimientos/'+ m_final_Array[i].pk +'"><span class="negrita truncate">Nombre:</span><span>' + m_final_Array[i].fields.nombre + '</span><br/>' +  '<span class="negrita truncate">Fecha:</span><span>' + m_final_Array[i].fields.fecha + '</span><hr/>';                         
                } 
                
                //console.log('parrContent', parrContent);
                $('.listaFinalizados').append(parrContent);     
                //console.log('listaFinalizados length', $('.listaFinalizados').length);

            } // end if  
            
        }
    });  

} // showMovimientosActivos

function regresarMovimientos() {
    $('.mapacalorscroll').hide();    
    $('.listaFinalizados').hide();    
    $('.sonbotones').show();
}
