//VERSION=3

function setup() {
    return {
      input: [
        {
          bands: [
            "red",
            "nir",
            "dataMask",
            "clear"
          ]
        }
      ],
      output: [
        {
          id: "ndvi",
          bands: 2
        },
        {
          id: "dataMask",
          bands: 1
        }
      ]
    }
  }
  
  
  
  function evaluatePixel(samples) {
    
      let ndvi = (samples.nir-samples.red)/(samples.nir+samples.red);
  
      const indexVal = samples.dataMask === 1 ? ndvi : NaN;
    
      let id_default = colorBlend(ndvi,  [0.0, 0.5, 1.0],
        [
          [1,0,0, samples.dataMask * samples.clear], 
          [1,1,0,samples.dataMask * samples.clear], 
          [0.1,0.31,0,samples.dataMask * samples.clear], 
        ])
  
        return {
          ndvi: [ndvi, samples.clear * samples.dataMask],
          dataMask: [samples.dataMask],
        };
  }