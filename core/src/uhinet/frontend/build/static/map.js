var map;
var drawingManager;
var selectedShape;
var coords = [];  // coordinates of the created polygon
var coords_bound; // coordinates of the current viewport
var coords_overlay; //coordinates of the current overlay
var overlay = [];
var overlay_index; // Indicate which overlay to display
var image_path = [];
var colors = ['#B0AFAF', '#606060', '#1C1C1C','#32CD32'];
var selectedColor;
var colorButtons = {};





function selectColor (color) {
    selectedColor = color;
    for (var i = 0; i < colors.length; ++i) {
        var currColor = colors[i];
        colorButtons[currColor].style.border = currColor == color ? '2px solid #789' : '2px solid #fff';
    }

    var polygonOptions = drawingManager.get('polygonOptions');
    polygonOptions.fillColor = color;
    drawingManager.set('polygonOptions', polygonOptions);
}

function setSelectedShapeColor (color) {
    if (selectedShape) {
        if (selectedShape.type == google.maps.drawing.OverlayType.POLYLINE) {
            selectedShape.set('strokeColor', color);
        } else {
            selectedShape.set('fillColor', color);
        }
    }
}

function makeColorButton (color) {
    var button = document.createElement('span');
    button.className = 'color-button';
    button.value = color;
    button.style.backgroundColor = color;
    button.style.borderWidth = "thick";    
    google.maps.event.addDomListener(button, 'click', function () {
        selectColor(color);
        setSelectedShapeColor(color);
    });

    return button;
}

function buildColorPalette () {
    var colorPalette1 = document.getElementById('color-palette1');
    var currColor = colors[0];
    var colorButton1= makeColorButton(currColor);
    var t1 = document.createTextNode("Residential");
    colorPalette1.appendChild(colorButton1);
    colorPalette1.appendChild(t1);
    colorButtons[currColor] = colorButton1;

    var colorPalette2 = document.getElementById('color-palette2');
    var currColor = colors[1];
    var colorButton2= makeColorButton(currColor);
    var t2 = document.createTextNode("Commercial");
    colorPalette2.appendChild(colorButton2);
    colorPalette2.appendChild(t2);
    colorButtons[currColor] = colorButton2;

    var colorPalette3 = document.getElementById('color-palette3');
    var currColor = colors[2];
    var colorButton3= makeColorButton(currColor);
    var t3 = document.createTextNode("Parking Lot");
    colorPalette3.appendChild(colorButton3);
    colorPalette3.appendChild(t3);
    colorButtons[currColor] = colorButton3;

    var colorPalette4 = document.getElementById('color-palette4');
    var currColor = colors[3];
    var colorButton4= makeColorButton(currColor);
    var t4 = document.createTextNode("Green Space");
    colorPalette4.appendChild(colorButton4);
    colorPalette4.appendChild(t4);
    colorButtons[currColor] = colorButton4;

    selectColor(colors[0]);
}


// Drawing manager operations

function clearSelection () {
    if (selectedShape) {
        if (selectedShape.type !== 'marker') {
            selectedShape.setEditable(false);
        }
        selectedShape = null;
    }
}

function setSelection (shape) {

    if (shape.type !== 'marker') {
        clearSelection();
        shape.setEditable(true);
        selectColor(shape.get('fillColor') || shape.get('strokeColor'));
    }
    selectedShape = shape;
}

function deleteSelectedShape () {
    if (selectedShape) {
        selectedShape.setMap(null);
    }
}

function showHideLayer(){
    if(overlay.length >= 1){
        var opacity = (document.getElementById("rangeinput").value) / 100.0;
        if(opacity==0){
            overlay[overlay_index].setOpacity(opacity);
            showOverlay();
        }
        else{
            overlay[overlay_index].setOpacity(0);
            showOverlay();
        }

    }
}

function showHidePolygon(){
    console.log('poly');
    if (selectedShape) {
        if (selectedShape.fillOpacity==0){
            console.log('1');
            selectedShape.set('fillOpacity', 0.55);
            selectedShape.set('strokeWeight', 2);
        }
        else{
            console.log('2');
            selectedShape.set('fillOpacity', 0);
            selectedShape.set('strokeWeight', 0);
        }
        
    }
}

// Send coordinates of the polygon and the viewport to the backend
// and get an image from the backend
$(function() {
  $('input#send_coords_button').bind('click', function() {
    if (coords.length < 1){
      window.alert('Please creat a polygon first.');
      return;
    }

    document.getElementById("loading_icon").style.display="block";

    selectedShape.set('strokeColor', '#000000');
    selectedShape.set('strokeWeight', 2);
    selectedShape.set('editable', false);
    selectedShape.set('draggable', false);

    coords_overlay = coords_bound;
    $.getJSON($SCRIPT_ROOT + '/send_coordinates', {
      coords_polygon: JSON.stringify(coords),
      coords_bound: JSON.stringify(coords_bound),
      polygon_color: JSON.stringify(selectedShape.fillColor),
      colors: JSON.stringify(colors),
    }, function(data) {
      image_path = [];
      image_path.push(('/static/' + data.image_names[0]));
      image_path.push(('/static/' + data.image_names[1]));
      image_path.push(('/static/' + data.image_names[2]));
      coords = [];
      coords_overlay = data.coords_bound;
      console.log(coords_overlay);
      document.getElementById("loading_icon").style.display="none";
      if(coords_overlay == null){
        window.alert("Please send coordinates first to get the overlay")
        return
      }
      if(overlay.length >= 1){
        for(var i = 0; i < 3; i = i + 1)
          overlay[i].setMap(null);
      }
      overlay = [];
      for(var i = 0; i < 3; i = i + 1){
          overlay.push(new google.maps.GroundOverlay(image_path[i], coords_overlay));
          var opacity = (document.getElementById("rangeinput").value) / 100.0;
          overlay[i].setOpacity(opacity);
      }
      if(overlay.length < 1){
        window.alert("Please create a overlay first");
        return;
      }
      overlay[overlay_index].setMap(map);      
    });
    return false;
  });
});


// Main function the google map
function initMap () {

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14.1,
        center: new google.maps.LatLng(43.65, -79.4),
        zoomControl: true
    });

    document.getElementById("loading_icon").style.display="none";


    // Set overlay index
    function setOverlayIndex(){
        if(overlay.length >= 1)
            removeOverlay();
        if(document.getElementById('Before').checked)
            overlay_index = 0
        if(document.getElementById('After').checked)
            overlay_index = 1
        if(document.getElementById('Difference').checked)
            overlay_index = 2
        if(overlay.length >= 1)
            showOverlay();
    }
    document.getElementById("rangeinput").value = 100;

    document.getElementById("Before").addEventListener("click", setOverlayIndex);
    document.getElementById("After").addEventListener("click", setOverlayIndex);
    document.getElementById("Difference").addEventListener("click", setOverlayIndex);
    setOverlayIndex();

    function removeOverlay(){
      overlay[overlay_index].setMap(null);
    }

    function showOverlay(){
      if(overlay.length < 1){
        window.alert("Please create a overlay first");
        return;
      }
      overlay[overlay_index].setMap(map);
    }

    var Options = {
        strokeWeight: 0,
        fillOpacity: 0.55,
        strokeColor: '#000000',
        strokeOpacity: 1.0,
        editable: true,
        draggable: true
    };


    // Change opacity of the overlay
    function changeOpacity(){
      if(overlay.length >= 1){
        var opacity = (document.getElementById("rangeinput").value) / 100.0;
        overlay[overlay_index].setOpacity(opacity);
        showOverlay();
      }
    }




    var button_changeOverlay = document.getElementById("rangeinput")
    button_changeOverlay.addEventListener("click", changeOpacity);



    // Keeps track of the coordinates of the current viewport
    google.maps.event.addListener(map, 'bounds_changed', function(){
        coords_bound = map.getBounds();
    });

    drawingManager = new google.maps.drawing.DrawingManager({
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['polygon']
        },
        polygonOptions: Options,
        map: map
    });

    // Google maps drawing manager
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function (shp) {
        var newShape = shp.overlay;
        drawingManager.setDrawingMode(null);
        array = newShape.getPath();
        coords = [];
        for(var i = 0; i < array.length; i++)
            coords.push(array.getAt(i));
        // window.alert(coords);
        google.maps.event.addListener(newShape, 'click', function (shp) {
            setSelection(newShape);
            array = newShape.getPath();
            coords = [];
            for(var i = 0; i < array.length; i++)
                coords.push(array.getAt(i));
            // window.alert(coords);
        });
        setSelection(newShape);
    });

    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
    google.maps.event.addListener(map, 'click', clearSelection);

    buildColorPalette();
}

function clearSelection () {
    if (selectedShape) {
        selectedShape.setEditable(false);
        selectedShape = null;
    }
}

function setSelection (shape) {
    clearSelection();
    shape.setEditable(true);
    selectedShape = shape;
}

function deleteSelectedShape () {
    if (selectedShape) {
        selectedShape.setMap(null);
    }
}
