let minVal = 0.0;
let maxVal = 0.4;

let viz = new HighlightCompressVisualizer(minVal, maxVal);

function evaluatePixel(samples) {
    let val = [samples[0].B04, samples[0].B03, samples[0].B02];
    return viz.processList(val);
}

function setup(ds) {
    setInputComponents([ds.B02, ds.B03, ds.B04]);
    setOutputComponentCount(3);
}
