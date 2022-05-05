mapboxgl.accessToken = "pk.eyJ1IjoiamVzdXNjYW1hcmlsbG8iLCJhIjoiY2szcm1lOXg1MDAwZjNnbGtibjMwN2xxeSJ9.a-4Xcq8tojNuH5Ci6pqHYQ";

var places = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {
        icon: "music",
      },
      geometry: {
        type: "Point",
        coordinates: [-106.44816936788, 31.7521767830]
      }
    }
  ]
};

console.log(places);

var filterGroup = document.getElementById("filter-group");
var mapbylayers = new mapboxgl.Map({
  container: "mapbylayers",
    style: "mapbox://styles/jesuscamarillo/ck3usp7tv1rfa1co2k9xx7vw7",
  center: [31.6185265,-106.3905846],
  zoom: 11.10
});

mapbylayers.on("load", function() {
  // Add a GeoJSON source containing place coordinates and information.
    mapbylayers.addSource("places", {
        type: "geojson",
        data: places
    });

  places.features.forEach(function(feature) {
    var symbol = feature.properties["icon"];
    var layerID = "poi-" + symbol;

    // Add a layer for this symbol type if it hasn't been added already.
    if (!mapbylayers.getLayer(layerID)) {
        console.log(symbol + "-15");
        mapbylayers.addLayer({
        id: layerID,
        type: "symbol",
        source: "places",
        layout: {
          "icon-image": symbol + "-15",
          "icon-allow-overlap": true,
          "icon-size": 2
        },
        filter: ["==", "icon", symbol]
      });

      // Add checkbox and label elements for the layer.
      var input = document.createElement("input");
      input.type = "checkbox";
      input.id = layerID;
      input.checked = true;
      filterGroup.appendChild(input);

      var label = document.createElement("label");
      label.setAttribute("for", layerID);
      label.textContent = symbol;
      filterGroup.appendChild(label);

      // When the checkbox changes, update the visibility of the layer.
      input.addEventListener("change", function(e) {
        mapbylayers.setLayoutProperty(
          layerID,
          "visibility",
          e.target.checked ? "visible" : "none"
        );
      });
    }
  });

  var allImages = map.listImages();
  console.log( allImages );
});
