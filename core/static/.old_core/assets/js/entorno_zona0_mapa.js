var map, heatmap, infowindow;
var markers = [];

alert('hola');

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 30.1523153, lng: -106.8905766},
        mapTypeId: 'satellite'
    });

    infoWindow = new google.maps.InfoWindow;
    
    var markers = setMarkers(map);

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map
    });       
}    

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}

function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
}     

function changeRadius() {
    heatmap.set('radius', heatmap.get('radius') ? null : 20);        
}

function changeOpacity() {
    heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

function changeMarkers() {        
    toggleMarkers(markers);
}

function toggleMarkers(markers) {
    // Loop through all markers and hide each of them
    for (var i = 0; i < markers.length; i++) {
        var marker = markers[i];
        marker.visible ? marker.setVisible(false) : marker.setVisible(true);
        //marker.setVisible(false);
    }        
}   

// Heatmap data: 500 Points
function getPoints() {
    return [
        {% for o in incidentes %}
        new google.maps.LatLng({{ o.lat}}, {{ o.lng }}),                
        {% endfor %}                    
    ];
}

function smoothZoom (map, level, cnt, mode) {
    //alert('Count: ' + cnt + 'and Max: ' + level);

    // If mode is zoom in
    if(mode == true) {

        if (cnt >= level) {
            return;
        }
        else {
            var z = google.maps.event.addListener(map, 'zoom_changed', function(event){
                google.maps.event.removeListener(z);
                smoothZoom(map, level, cnt + 1, true);
            });
            setTimeout(function(){map.setZoom(cnt)}, 50);
        }
    } else {
        if (cnt <= level) {
            return;
        }
        else {
            var z = google.maps.event.addListener(map, 'zoom_changed', function(event) {
                google.maps.event.removeListener(z);
                smoothZoom(map, level, cnt - 1, false);
            });
            setTimeout(function(){map.setZoom(cnt)}, 50);
        }
    }
}

function goUbicacion(lugar) {
    var vLugar = 'Ubicaci??n seleccionada';
    var vzoom = 0;
    var latitude  = 0;
    var longitude = 0;
    var whereMarker = null;

    if (lugar == 'usa_east') {
        latitude  =  36.5522;
        longitude =  -83.9171817;
        vLugar = 'Estados Unidos Este';
        vzoom = 6;            
    }  else if (lugar == 'global') {
        latitude  =  24.6110255;
        longitude = -42.8441299;
        vLugar = 'Vista Global';
        vzoom = 2.75;
    } else if (lugar == 'la') {
        latitude  =  15.2985681;
        longitude =  -78.6551153;
        vLugar = 'Am??rica Latina';
        vzoom = 4;
    } else if (lugar == 'juarez') {
        latitude  =  31.6874405;
        longitude =  -106.4300477;
        vLugar = 'Ciudad Ju??rez';
        vzoom = 12;
    } else if (lugar == 'benitojuarez') {
        latitude  = 30.1523153;
        longitude = -106.8905766;
        vLugar = 'Benito Ju??rez';
        vzoom = 12;
    } else if (lugar == 'europa') {
        latitude  =   52.0930382;
        longitude =  11.3800946;
        vLugar = 'Europa';
        vzoom = 5;
    } else if (lugar == 'asia') {
        latitude  =  33.2888155;
        longitude =  113.5219767;
        vLugar = 'Asia';
        vzoom = 4;
    } else if (lugar == 'oceania') {
        latitude  =  -30.7058591;
        longitude =  143.8021268;
        vLugar = 'Ocean??a';
        vzoom = 5;
    }         

    whereMarker = new google.maps.Marker({
        zoom: vzoom,
        position: new google.maps.LatLng(latitude, longitude),
        title: vLugar,
        icon: "{% static 'core/assets/images/where-ico-marker.png' %}",
        map: map,
    });
    map.panTo(whereMarker.getPosition());
    //smoothZoom(map, vzoom, map.getZoom(), true);
    map.setZoom(vzoom);
}

function setMarkers(map) {
    // Adds markers to the map.
    
    // Shapes define the clickable region of the icon. The type defines an HTML
    // <area> element 'poly' which traces out a polygon as a series of X,Y points.
    // The final coordinate closes the poly by connecting to the first coordinate.
    var shape = {
        coords: [1, 1, 1, 47, 30, 47, 30, 1],
        type: 'poly'
    };

    var iconos = { 
        'homicidio'         : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/homicidio.png' %}" },
        'carjacking'        : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/carjacking.png' %}" },
        'asalto_transeuntes': { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/transeuntes.png' %}" },
        'casa_habitacion'   : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/casa-habitacion.png' %}" },
        'hotel'             : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/hotel.png' %}" },
        'aeropuerto'        : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/aeropuerto.png' %}" },
        'autopartes'        : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/auto-partes.png' %}" },
        'secuestro'         : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/secuestro.png' %}" },            
        'lesiones'          : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/lesiones.png' %}" },            
        'robo_vehiculo'     : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/carjacking.png' %}" },            
        'narcomenudeo'      : { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/narcomenudeo.png' %}" },            
        'violencia_familiar': { 'img': "{% static 'core/assets/images/icons/delincuenciales-color/secuestro.png' %}" },            
    };            

    var czindex = 500;           

    

    var ico_plantas = {             
        'optimo': { 'img': "{% static 'core/assets/images/yazaki/yazaki-marker.png' %}" },
        'relevante': { 'img': "{% static 'core/assets/images/alert-icon-plant.gif' %}" },
    }; 

    // Visualizaci??n de plantas de cliente

    var czindex = 900, vplantStatus;   

    var pnombre = 'Yazaki Benito Juarez'; 
        
    vplantStatus = 'relevante';

    console.log(vplantStatus);

    var marker = new google.maps.Marker({
        position: {lat: 30.1906773, lng: -106.7928537 },
        map: map,
        icon: ico_plantas.relevante.img,
        shape: shape,
        title: pnombre.toUpperCase(),
        zIndex: czindex
    });

    var estado_planta = '<span class="bgp-color-verde">??ptimo</span>';

    if (vplantStatus == 'relevante') {
        estado_planta = '<span class="bgp-color-rojo">Relevante</span>';



        var plantaAlias = "benitojuarez";

        console.log (plantaAlias);

        jQuery('#addCritical').append('<li class="nav-item"><a class="nav-link" onclick="goUbicacion(\'' + plantaAlias.toLowerCase() + '\')"><i class="nav-link-icon lnr-inbox"></i><span class="nombrePlantaCritica"> Yazaki Benito Juarez</span></a></li>');
    }         

    marker.infowindow = new google.maps.InfoWindow({
        content: '<div class="popupCustom"><div class="buHeader"></div><div class="infoUBH5_Wrapper" onclick="location.href=\'ceo_master\'"><img src="/static/core/assets/images/yazaki/yazaki-marker.png"/><h5 class="infoUBH5">' + pnombre.toUpperCase() + '</h5><span class="small">??lvaro Obreg??n, Sin Nombre, 31884, Benito Ju??rez, Chihuahua, M??xico </span></div> <br> <div class="row infoContent"><div class="col-md-6"><p><b>Nivel de Seguridad:</b>' + estado_planta + '</p><p><b>Incidentes log??sticos</b></p><hr/><p><b>PREDICTIVE ANALYTICS</b><br/>COBERTURA<br/><img src="/static/core/assets/images/indicador.jpg"/></p></div><div class="col-md-6"><div class="map_scroll_wrapper"><div class="scroll_content"> <p><b>Seguridad Electr??nica</b>: 84.17%</p><p>Falla el??ctrica total en planta G3783-Yak5 por explosi??n de estaci??n de gasolina.</p><p>La planta Yazaki Benito Juarez qued?? en un 75% afectada por razones de tormentas el??ctricas y vientos fuertes en la ciudad, debido a que se dio una alerta roja desde el gobierno mexicano.<br/>Se tiene un estimado de varias horas antes de que la tormenta y los vientos fuertes se retiren.</p></div></div></div></div></div>',
        maxWidth: 550
    });           
    
    marker.addListener('click', function() {
        this.infowindow.open(map, this);
    });

    google.maps.event.trigger(marker,'click');

    console.log(marker);           
        
    return markers;
}    