var drawingManager;
var selectedShape;
var map;
var overlay;

function CreateOverlay (image, imageBounds){
    this.imageBounds= imageBounds,
    this.image= image,
    this.overlay = new google.maps.GroundOverlay(
        image, imageBounds);
    this.addOverlay= function(){
        console.log('add');
        this.overlay.setMap(map);
    }

    this.removeOverlay= function(){
        console.log('remove')
        this.overlay.setMap(null);
    }
    this.setOpacity= function(opac){

    }
};

function CreateShape (shp){
    newShape = shp;
    console.log(newShape);
    drawingManager.setDrawingMode(null);
    setSelection(newShape);
    google.maps.event.addListener(newShape,'click', setSelection(newShape));

}

function clearSelection () {
    if (selectedShape) {      
        selectedShape.overlay.editable=false;
        selectedShape = null;
    }
}

function setSelection (shape) {
    console.log('bitch');
    clearSelection();
    shape.overlay.editable = true;
    selectedShape = shape;
}

function deleteSelectedShape () {
    if (selectedShape) {
        selectedShape.setMap(null);
    }
}

function initMap () {

    map = new google.maps.Map(document.getElementById('map'), {
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

    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(shp){
        CreateShape(shp);
    });

    google.maps.event.addDomListener(document.getElementById('add'), 'click', function(){
        console.log("added");
    });
    google.maps.event.addDomListener(document.getElementById('remove'), 'click', console.log('swag'));

    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
    map.addListener(map, 'click', clearSelection);
    google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);
    google.maps.event.addDomListener(document, 'keydown', function (e) {
        if (e.key ==="Backspace" || e.key === "Delete") {
            deleteSelectedShape();
        }
     });

    var imageBounds = {
        north:43.71928751019047, west:-79.47656815720673, south:43.58076648980952, east:-79.2858718427933
    };

    let Overlay1 = new CreateOverlay(image, imageBounds);
}
