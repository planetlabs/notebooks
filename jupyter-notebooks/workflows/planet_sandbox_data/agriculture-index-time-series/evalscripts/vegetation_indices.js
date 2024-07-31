//VERSION=3
//PlanetScope Mutliple Agricultural Indices

function setup() {
  return {
    input: [{
      bands: [
        "nir",
        "rededge",
        "dataMask",
        "green",
        "red",
        "clear"
      ]
    }],
    output: [
      { id: "ndre", bands: 1, sampleType: "FLOAT32" },
      { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
      { id: "rtvicore", bands: 1, sampleType: "FLOAT32" },
      { id: "msavi", bands: 1, sampleType: "FLOAT32" },
      { id: "clear", bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 },
    ]
  }
}

function evaluatePixel(sample) {

  let ndre = index(sample.nir, sample.rededge);

  let ndvi = index(sample.nir, sample.red);

  let msavi = 0.5 * (2.0 * sample.nir + 1 - (((2 * sample.nir + 1) ** 2) - 8 * (sample.nir - sample.red)) ** 0.5)

  let rtvicore = (100 * (sample.nir - sample.rededge) - 10 * (sample.nir - sample.green))

  const clear = sample.dataMask && sample.clear;

  return {
    ndre: [ndre],
    ndvi: [ndvi],
    rtvicore: [rtvicore],
    msavi: [msavi],
    clear: [clear],
    dataMask: [sample.dataMask],
  };
}