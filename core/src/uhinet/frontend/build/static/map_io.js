var map;
var polygon;
var infoWindow;
var markers = [];
var coords = [];  // coordinates of the created polygon
var coords_bound; // coordinates of the viewport


$(function() {
  $('input#send_coords_button').bind('click', function() {
    if (coords.length < 1){
      window.alert('Please create a polygon first.');
      return;
    }
    $.getJSON($SCRIPT_ROOT + '/send_coordinates', {
      coords_polygon: JSON.stringify(coords),
      coords_bound: JSON.stringify(coords_bound),
    }, function(image_name) {
      document.getElementById('test_image').src='/static/' + image_name;
    });
    return false;
  });
});


function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 43.65, lng: -79.4},
    zoom: 14.1,
  });

  infoWindow = new google.maps.InfoWindow;

  google.maps.event.addListener(map, 'click', function(event){
    addMarker(event.latLng);
  });

  google.maps.event.addListener(map, 'bounds_changed', function(){
    coords_bound = map.getBounds();
  });
}

function addMarker(location){
  var marker = new google.maps.Marker({
    position:location,
    map:map,
  });
  markers.push(marker);
}

function setMapOnAll(map){
  for (var i = 0; i < markers.length; i++){
    markers[i].setMap(map);
  }
}

/* Hide markers */
function clearMarkers(){
  setMapOnAll(null);
}

/* Show hidden markers */
function showMarkers(){
  setMapOnAll(map);
}

/* Delete all markers */
function deleteMarkers(){
  clearMarkers();
  markers = [];
}

/* Construct the polygon using markers */
function addPolygon(){
  if(markers.length == 0){
    window.alert("Please mark locations first.");
    return;
  }

  if(markers.length < 3){
    window.alert("You should mark at least 3 locations.");
    return;
  }

  coords = [];
  for (var i = 0; i < markers.length; i++){
    coords.push(markers[i].getPosition());
  }

  polygon = new google.maps.Polygon({
    paths: coords,
    strokeColor: '#23244b',
    strokeOpacity: 0.8,
    strokeWeight: 3,
    fillColor: '#808080',
    fillOpacity: 0.35,
    draggable: true,
    editable: true,
    geodesic: true
  });

  // Add a listener for the click event.
  polygon.addListener('click', showArrays);
  polygon.setMap(map);
}

/* Delete the current polygon */
function removePolygon(){
  polygon.setMap(null);
  polygon = null;
}

/* Show coordinates of the polygon */
function showArrays(event) {
  var vertices = this.getPath();

  var contentString = '<b>Polygon</b><br>';

  // Iterate over the vertices.
  for (var i =0; i < vertices.getLength(); i++) {
    var xy = vertices.getAt(i);
    contentString += '<br>' + 'Coordinate ' + i + ':<br>' + xy.lat() + ',' +
        xy.lng();
  }

  infoWindow.setContent(contentString);
  infoWindow.setPosition(event.latLng);

  infoWindow.open(map);
} 
