//cloud mask
var geometry = ee.Geometry.Rectangle([-79.49947,43.607519,-79.269364,43.71388])
function maskL8sr(image) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively.
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);
  // Get the pixel QA band.
  var qa = image.select('pixel_qa');
  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                 .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return image.updateMask(mask);
}

//vis params
var vizParams = {
  bands: ['B5', 'B6', 'B4'],
  min: 0,
  max: 4000,
  gamma: [1, 0.9, 1.1]
};
var vizParams2 = {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 3000,
  gamma: 1.4,
};

//load the collection:
{
var col = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
.map(maskL8sr)
.filterDate('2018-01-01','2018-12-31')
.filterBounds(geometry);
}
print(col, 'coleccion');

//median
{
var image = col.median();
print(image, 'image');
Map.addLayer(image, vizParams2);
}

// NDVI:
{
var ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
var ndviParams = {min: -1, max: 1, palette: ['blue', 'white', 'green']};
print(ndvi,'ndvi');
Map.addLayer(ndvi, ndviParams, 'ndvi');
}

//

//select thermal band 10(with brightness tempereature), no BT calculation 
var thermal= image.select('B10').multiply(0.1);
var b10Params = {min: 2878000, max: 3046000, palette: ['blue', 'white', 'green']};
Map.addLayer(thermal, b10Params, 'thermal');
 
 
// find the min and max of NDVI
{
var min = ee.Number(ndvi.reduceRegion({
   reducer: ee.Reducer.min(),
   geometry: geometry,
   scale: 30,
   maxPixels: 1e9
   }).values().get(0));
print(min, 'min');
var max = ee.Number(ndvi.reduceRegion({
    reducer: ee.Reducer.max(),
   geometry: geometry,
   scale: 30,
   maxPixels: 1e9
   }).values().get(0));
print(max, 'max')
}

//fractional vegetation
{
var fv = ndvi.subtract(min).divide(max.subtract(min)).rename('FV'); 
print(fv, 'fv');
Map.addLayer(fv);
}

/////////////


  //Emissivity

  var a= ee.Number(0.004);
  var b= ee.Number(0.986);
  var EM=fv.multiply(a).add(b).rename('EMM');
  var imageVisParam2 = {min: 0.98, max: 0.99, palette: ['blue', 'white', 'green']};
  Map.addLayer(EM, imageVisParam2,'EMM');


  //LST c,d,f, p1, p2, p3 are assigned variables to write equaton easily
var LST = thermal.expression(
    '(Tb/(1 + (0.001145* (Tb / 1.438))*log(Ep)))-273.15', {
      'Tb': thermal.select('B10'),
      'Ep': EM.select('EMM')
});
  //LST c,d,f, p1, p2, p3 are assigned variables to write equaton easily
/*  var c= ee.Number(1);
  var d= ee.Number(0.00115);
  var f= ee.Number(1.4388);


var p1= ee.Number(thermal.multiply(d).divide(f));
var p2= ee.Number(Math.log(EM));
var p3= ee.Number(p1.multiply(p2).add(c));


var LST= (thermal.divide(p3)).rename('LST');

var LSTimage = ee.Image(LST);*/
{
var min = ee.Number(LST.reduceRegion({
   reducer: ee.Reducer.min(),
   geometry: geometry,
   scale: 30,
   maxPixels: 1e9
   }).values().get(0));
print(min, 'min');
var max = ee.Number(LST.reduceRegion({
    reducer: ee.Reducer.max(),
   geometry: geometry,
   scale: 30,
   maxPixels: 1e9
   }).values().get(0));
print(max, 'max')
}

Map.addLayer(LST, {min: 15, max: 32, palette: ['white', 'red']},'LST');

  
  







