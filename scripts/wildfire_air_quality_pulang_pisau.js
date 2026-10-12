// ============================================================
// WILDFIRE AND AIR QUALITY MONITORING
// Pulang Pisau Regency, Central Kalimantan, Indonesia
// ============================================================

// Administrative boundary : BPS / administrative shapefile
// Active-fire data        : NASA FIRMS
// Atmospheric data        : Copernicus Sentinel-5P
// Platform                : Google Earth Engine

// Note:
// FIRMS rasters are used to examine the spatial distribution
// of active-fire detection activity. The results are not interpreted
// as counts of unique wildfire events on the ground.
// ============================================================

// ============================================================
// 1. STUDY AREA
// ============================================================
var admin = ee.FeatureCollection(
  'projects/ee-dedyhikari0809/assets/Kalimantan_Tengah_ADMIN_BPS'
);

var roi = admin.filter(
  ee.Filter.eq('Kabupaten', 'Pulang Pisau')
);

print('Pulang Pisau ROI:', roi);
print('Number of ROI features:', roi.size());

Map.centerObject(roi, 9);

// Administrative boundary
var roiStyle = roi.style({
  color: 'red',
  fillColor: '00000000',
  width: 2
});

Map.addLayer(
  roiStyle,
  {},
  'Pulang Pisau Regency Boundary'
);

// ============================================================
// 2. NASA FIRMS FIRE-DETECTION ACTIVITY
// July-September 2026
// ============================================================
var firms = ee.ImageCollection('FIRMS')
  .filterBounds(roi);

print(
  'Total FIRMS images intersecting ROI:',
  firms.size()
);

// ------------------------------------------------------------
// Monthly collections
// Earth Engine end dates are exclusive.
// ------------------------------------------------------------
var firmsJuly = firms.filterDate(
  '2026-07-01',
  '2026-08-01'
);

var firmsAugust = firms.filterDate(
  '2026-08-01',
  '2026-09-01'
);

var firmsSeptember = firms.filterDate(
  '2026-09-01',
  '2026-10-01'
);

print(
  'FIRMS images - July 2026:',
  firmsJuly.size()
);

print(
  'FIRMS images - August 2026:',
  firmsAugust.size()
);

print(
  'FIRMS images - September 2026:',
  firmsSeptember.size()
);

// ============================================================
// 2.1 MONTHLY FIRE-DETECTION ACTIVITY
// ============================================================
function calculateFIRMSActivity(collection) {

  var activityImage = collection
    .select('T21')
    .count();

  return activityImage
    .reduceRegion({
      reducer: ee.Reducer.sum(),
      geometry: roi.geometry(),
      scale: 1000,
      maxPixels: 1e9,
      bestEffort: true
    })
    .get('T21');
}

print(
  'FIRMS detection activity - July 2026:',
  calculateFIRMSActivity(firmsJuly)
);

print(
  'FIRMS detection activity - August 2026:',
  calculateFIRMSActivity(firmsAugust)
);

print(
  'FIRMS detection activity - September 2026:',
  calculateFIRMSActivity(firmsSeptember)
);

// ============================================================
// 2.2 MONTHLY FIRMS RASTERS
// ============================================================
var firmsActivityJuly = firmsJuly
  .select('T21')
  .count()
  .clip(roi);

var firmsActivityAugust = firmsAugust
  .select('T21')
  .count()
  .clip(roi);

var firmsActivitySeptember = firmsSeptember
  .select('T21')
  .count()
  .clip(roi);

// FIRMS visualization
var firmsVis = {
  min: 0,
  max: 3,
  palette: [
    'yellow',
    'orange',
    'red'
  ]
};

Map.addLayer(
  firmsActivityJuly,
  firmsVis,
  'NASA FIRMS - July 2026',
  false
);

Map.addLayer(
  firmsActivityAugust,
  firmsVis,
  'NASA FIRMS - August 2026',
  false
);

Map.addLayer(
  firmsActivitySeptember,
  firmsVis,
  'NASA FIRMS - September 2026',
  false
);

// ============================================================
// 3. COPERNICUS SENTINEL-5P
// Atmospheric parameters - September 2026
// ============================================================
var startDate = '2026-09-01';
var endDate   = '2026-10-01';

// ============================================================
// 3.1 HCHO
// ============================================================
var hcho = ee.ImageCollection(
  'COPERNICUS/S5P/OFFL/L3_HCHO'
)
  .filterBounds(roi)
  .filterDate(startDate, endDate)
  .select(
    'tropospheric_HCHO_column_number_density'
  );

print(
  'Sentinel-5P HCHO images:',
  hcho.size()
);

var hchoMean = hcho
  .mean()
  .clip(roi);

var hchoVis = {
  min: 0,
  max: 0.0003,
  palette: [
    'blue',
    'cyan',
    'green',
    'yellow',
    'orange',
    'red'
  ]
};

Map.addLayer(
  hchoMean,
  hchoVis,
  'Sentinel-5P HCHO - September 2026',
  false
);

// ============================================================
// 3.2 NO2
// ============================================================
var no2 = ee.ImageCollection(
  'COPERNICUS/S5P/OFFL/L3_NO2'
)
  .filterBounds(roi)
  .filterDate(startDate, endDate)
  .select(
    'tropospheric_NO2_column_number_density'
  );

print(
  'Sentinel-5P NO2 images:',
  no2.size()
);

var no2Mean = no2
  .mean()
  .clip(roi);

var no2Vis = {
  min: 0,
  max: 0.0002,
  palette: [
    'blue',
    'cyan',
    'green',
    'yellow',
    'orange',
    'red'
  ]
};

Map.addLayer(
  no2Mean,
  no2Vis,
  'Sentinel-5P NO2 - September 2026',
  false
);

// ============================================================
// 3.3 UV AEROSOL INDEX
// ============================================================
var aerosol = ee.ImageCollection(
  'COPERNICUS/S5P/OFFL/L3_AER_AI'
)
  .filterBounds(roi)
  .filterDate(startDate, endDate)
  .select(
    'absorbing_aerosol_index'
  );

print(
  'Sentinel-5P Aerosol Index images:',
  aerosol.size()
);

var aerosolMean = aerosol
  .mean()
  .clip(roi);

var aerosolVis = {
  min: -1,
  max: 3,
  palette: [
    'blue',
    'cyan',
    'green',
    'yellow',
    'orange',
    'red'
  ]
};

Map.addLayer(
  aerosolMean,
  aerosolVis,
  'Sentinel-5P Aerosol Index - September 2026',
  true
);

// ============================================================
// 4. FINAL MAP VIEW
// ============================================================
Map.centerObject(
  roi,
  9
);

print(
  'Wildfire and air-quality analysis successfully prepared.'
);
