var drawingManager;
var selectedShape;

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

function initialize () {

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14.1,
        center: new google.maps.LatLng(43.65, -79.4),
        zoomControl: true
    });

    var Options = {
        strokeWeight: 0,
        fillOpacity: 0.45,
        editable: true,
        draggable: true
    };

    drawingManager = new google.maps.drawing.DrawingManager({
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['polygon','rectangle']
        },
        rectangleOptions: Options,
        polygonOptions: Options,
        map: map
    });

    google.maps.event.addListener(drawingManager, 'overlaycomplete', function (shp) {
        var newShape = shp.overlay;
        drawingManager.setDrawingMode(null);
        google.maps.event.addListener(newShape, 'click', function (shp) {
            setSelection(newShape);
        });
        
        google.maps.event.addListener(newShape,'mouseover', function (shp) { //this part doesnt work at all yet
            
            var vertices = this.getPath();

            var contentString = '<b>Polygon</b><br>';

            for (var i =0; i < vertices.getLength(); i++) {
                var xy = vertices.getAt(i);
                contentString += '<br>' + 'Coordinate ' + i + ':<br>' + xy.lat() + ',' +
                xy.lng();
            }

            infoWindow.setContent(contentString);=
            infoWindow.open(map);
        });
        setSelection(newShape);
    });

    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
    google.maps.event.addListener(map, 'click', clearSelection);
    google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);
    google.maps.event.addDomListener(document, 'keydown', function (e) {
        if (e.key ==="Backspace" || e.key === "Delete") {
            deleteSelectedShape();
        }
    });

}
google.maps.event.addDomListener(window, 'load', initialize);