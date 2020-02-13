var band="B10";
var option = 0;
var minC = -30;
var maxC = 30;
var NDVIs=0.2;
var NDVIv=0.8;
var waterE=0.991;
var soilE=0.966;
var vegetationE=0.973;
var C=0.009;
var bCent= (band=="B10") ? 0.000010895 : 0.000012005;
var rho=0.01438;
if (option==2) {
	minC = 0;
	maxC = 25;
}
let viz = ColorGradientVisualizer.createRedTemperature(minC, maxC);
function setup (dss) {
	setInputComponents([dss.B03,dss.B04,dss.B05,dss.B10,dss.B11]);
	setOutputComponentCount(3);// 1
}
function LSEcalc(NDVI,Pv) {
	var LSE;
	if (NDVI < 0) {
		LSE=waterE;
	} else if (NDVI < NDVIs) {
		LSE=soilE;
	} else if (NDVI > NDVIv) {
		LSE=vegetationE;
	} else {
		LSE=vegetationE*Pv+soilE*(1-Pv)+C;
	}
	return LSE;
}
function evaluatePixel(samples) {
	var LSTmax=-999;
	var LSTavg=0;
	var LSTstd=0;
	var reduceNavg=0;
	var N=samples.length;
	var LSTarray = [];
	for (var i=0;i<N;i++) {
		var Bi= (band=="B10") ? samples[i].B10 : samples[i].B11;
		var B03i = samples[i].B03;
		var B04i = samples[i].B04;
		var B05i = samples[i].B05;
		if ((Bi>173 && Bi<65000) && (B03i>0 && B04i>0 && B05i>0)) {
			var b10BTi=Bi-273.15;
			var NDVIi=(B05i-B04i)/(B05i+B04i);
			var PVi=Math.pow(((NDVIi-NDVIs)/(NDVIv-NDVIs)), 2);
			var LSEi=LSEcalc(NDVIi,PVi);
			var LSTi=(b10BTi/(1+(((bCent*b10BTi)/rho)*Math.log(LSEi))));
			LSTavg=LSTavg+LSTi;
			if (LSTi>LSTmax) {LSTmax=LSTi;}
			LSTarray.push(LSTi);
		} else {
			++reduceNavg;
		}
	}
	N=N-reduceNavg;
	LSTavg=LSTavg/N;
	for (var i=0;i<LSTarray.length;i++) {
		LSTstd=LSTstd+(Math.pow(LSTarray[i]-LSTavg, 2));
	}
	LSTstd=(Math.pow(LSTstd/(LSTarray.length-1), 0.5));
	let outLST= (option==0)
		? LSTavg
		: (option==1)
			? LSTmax
			: LSTstd;
        return [(outLST - minC) / (maxC - minC), 0, 0];
	return viz.process(outLST);
}
