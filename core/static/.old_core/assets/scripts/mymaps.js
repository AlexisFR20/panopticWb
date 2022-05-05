var pathnameInDashboardHome = window.location.pathname;
console.log ( pathnameInDashboardHome );
if (pathnameInDashboardHome == '/inicio') {
    
    mapboxgl.accessToken = 'pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ';

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/jesuscamarillo/ck3usp7tv1rfa1co2k9xx7vw7',
        center: [-106.3955138, 31.6677033],
        zoom: 14
    });
        
        var jsonDataGeo = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"dbh":99},"geometry":{"type":"Point","coordinates":[-106.3973228,31.6680723]}},{"type":"Feature","properties":{"dbh":119},"geometry":{"type":"Point","coordinates":[-106.3990667,31.6695727]}},{"type":"Feature","properties":{"dbh":99},"geometry":{"type":"Point","coordinates":[-106.4008102,31.6694498]}},{"type":"Feature","properties":{"dbh":79},"geometry":{"type":"Point","coordinates":[-106.4096167,31.6839375]}},{"type":"Feature","properties":{"dbh":39},"geometry":{"type":"Point","coordinates":[-106.4071047,31.6882471]}}]}';

        var jsonDataGeo2 = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"dbh":99},"geometry":{"type":"Point","coordinates":[-106.3273228,31.6680723]}},{"type":"Feature","properties":{"dbh":119},"geometry":{"type":"Point","coordinates":[-106.3290667,31.6695727]}},{"type":"Feature","properties":{"dbh":99},"geometry":{"type":"Point","coordinates":[-106.3808102,31.6694498]}},{"type":"Feature","properties":{"dbh":79},"geometry":{"type":"Point","coordinates":[-106.3796167,31.6839375]}},{"type":"Feature","properties":{"dbh":39},"geometry":{"type":"Point","coordinates":[-106.3871047,31.6882471]}}]}';
        
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-106.3955138, 31.6677033],
            zoom: 11
        });

        map.on('load', function() {

            map.loadImage(
                    '',
                    function(error, image) {
                        if (error) throw error;
                        map.addImage('cat', image);
                        map.addLayer({
                            'id': 'points',
                            'type': 'symbol',
                            'source': {
                            'type': 'geojson',
                            'data': {
                            'type': 'FeatureCollection',
                            'features': [
                                {
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Point',
                                        'coordinates': [-106.3990667,31.6695727]
                                    }
                                }
                            ]
                        }
                    },
                    'layout': {
                        'icon-image': 'cat',
                        'icon-size': 0.1
                        }
                    });
                }
            );

            map.addSource('trees', {
                "type": "geojson",
                "buffer": 1,
                "data":  JSON.parse(jsonDataGeo)
            });           

            map.addSource('trees2', {
                "type": "geojson",
                "buffer": 2,
                "data":  JSON.parse(jsonDataGeo2)
            });           

            map.addLayer({
                "id": "trees-heat",
                "type": "heatmap",
                "source": "trees",
                "maxzoom": 18,
                "paint": {
                // increase weight as diameter breast height increases
                    "heatmap-weight": {
                        "property": "dbh",
                        "type": "exponential",
                        "stops": [
                            [1, 0],
                            [62, 1]
                        ]
                    },
                // increase intensity as zoom level increases
                    "heatmap-intensity": {
                        "stops": [
                            [11, 1],
                            [15, 3]
                        ]
                    },
                // use sequential color palette to use exponentially as the weight increases
                    "heatmap-color": [
                        "interpolate",
                        ["linear"],
                        ["heatmap-density"],
                        0, "rgba(255,255,255,0.1)",
                        0.2, "red",
                        0.4, "orange",
                        0.6, "yellow",
                        0.8, "green"
                    ],
                    // increase radius as zoom increases
                    "heatmap-radius": {
                        "stops": [
                            [14, 19],
                            [19, 26]
                        ]
                    },
                    // decrease opacity to transition into the circle layer
                    "heatmap-opacity": {
                        "default": 1,
                        "stops": [
                            [14, 1],
                            [15, 0]
                        ]
                    },
                }
            }, 'waterway-label');

            map.addLayer({
                "id": "trees-heat2",
                "type": "heatmap",
                "source": "trees2",
                "maxzoom": 18,
                "paint": {
                // increase weight as diameter breast height increases
                    "heatmap-weight": {
                        "property": "dbh",
                        "type": "exponential",
                        "stops": [
                            [1, 0],
                            [62, 1]
                        ]
                    },
                // increase intensity as zoom level increases
                    "heatmap-intensity": {
                        "stops": [
                            [11, 1],
                            [15, 3]
                        ]
                    },
                // use sequential color palette to use exponentially as the weight increases
                    "heatmap-color": [
                        "interpolate",
                        ["linear"],
                        ["heatmap-density"],
                        0, "rgba(255,255,255,0.1)",
                        0.2, "purple",
                        0.4, "brown",
                        0.6, "pink",
                        0.8, "cyan"
                    ],
                    // increase radius as zoom increases
                    "heatmap-radius": {
                        "stops": [
                            [14, 19],
                            [19, 26]
                        ]
                    },
                    // decrease opacity to transition into the circle layer
                    "heatmap-opacity": {
                        "default": 1,
                        "stops": [
                            [14, 1],
                            [15, 0]
                        ]
                    },
                }
            }, 'waterway-label');
        
            
        
    });
}