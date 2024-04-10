// Setup function defining the input/output settings

var allowedDates = []//["2023-08-01", "2023-08-06", "2023-08-09", "2023-08-16", "2023-08-19"];  // added from python

function setup() {
    return {
        input: ["red", "nir", "dataMask"],
        output: [{
            id: "default",
            bands: 4
        }
    ],
        mosaicking: "ORBIT"  // Mosaicking method
};
}

// Preprocess the scenes to filter based on allowed dates
function preProcessScenes(collections) {
    collections.scenes.orbits = collections.scenes.orbits.filter(function (orbit) {
        var orbitDateFrom = orbit.dateFrom.split("T")[0];
        return allowedDates.includes(orbitDateFrom);
    });
    return collections;
}

// Function to calculate NDVI
function calculateNDVI(nir, red) {
    return (nir - red) / (nir + red);
}

// Function to get the median value from an array
function getMedian(values) {
    values.sort((a, b) => a - b);
    const middle = Math.floor(values.length / 2);
    return values.length % 2 !== 0 ? values[middle] : (values[middle - 1] + values[middle]) / 2.0;
}

// Evaluate each pixel across all samples
function evaluatePixel(samples) {
    let ndviValues = [];

    for (let i = 0; i < samples.length; i++) {
        let sample = samples[i];
        if (sample.dataMask === 1) { 
            let ndvi = calculateNDVI(sample.nir, sample.red);
            ndviValues.push(ndvi);
        }
    }

    // Calculate the median NDVI
    let medianNDVI = getMedian(ndviValues);


    return colorBlend(medianNDVI,
        [0.0, 0.5, 1.0],
        [
            [1, 0, 0, samples[0].dataMask],
            [1, 1, 0, samples[0].dataMask],
            [0.1, 0.31, 0, samples[0].dataMask],
        ]);

}
