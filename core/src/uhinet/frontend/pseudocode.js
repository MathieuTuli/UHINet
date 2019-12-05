function CreateOverlay (image, imageBounds){
    this.addOverlay= function(){};
    this.removeOverlay= function(){};
    this.setOpacity= function(opac){};
};

function CreateShape (shp){
}

function CreateMap (){
    this.clearSelection = function() {};
    this.setSelection = function() {}l
    this.deleteSelectedShape = function() {};
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(shp){
        CreateShape(shp);
    });
}

function CreateButton (name, function){
    google.maps.event.addDomListener(document.getElementById(name), 'click', function);
}

function initMap () {

    map = CreateMap();
    layer1 = CreateOverlay();
    button1 = CreateButton('add',function);

};
