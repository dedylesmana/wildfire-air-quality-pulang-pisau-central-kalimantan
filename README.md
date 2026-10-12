# Karhutla Pulang Pisau, Central Kalimantan

## Remote Sensing-Based Forest Fire and Atmospheric Pollution Analysis

This repository contains a geospatial analysis workflow for assessing forest-fire activity and atmospheric pollution in Pulang Pisau Regency, Central Kalimantan, Indonesia.

The project integrates satellite-derived fire detection and atmospheric composition datasets to support spatial analysis and visualization of forest-fire-related environmental conditions.

---

## Study Area

The study focuses on **Pulang Pisau Regency, Central Kalimantan, Indonesia**.

The study area is represented using a GeoJSON boundary and is used as the spatial reference for processing and visualization of the satellite-derived datasets.

---

## Data Sources

The analysis uses the following datasets:

### NASA FIRMS Fire Detection

Monthly fire-detection data are used to examine the spatial and temporal distribution of active fire detections.

- July 2026
- August 2026
- September 2026

### Sentinel-5P Atmospheric Indicators

Sentinel-5P satellite products are used to characterize atmospheric pollution indicators over the study area:

- Tropospheric Formaldehyde (HCHO)
- Tropospheric Nitrogen Dioxide (NO₂)
- Absorbing Aerosol Index (AAI)

---

## Repository Structure

```text
Karhutla_Kabupaten_Pulang_Pisau_Kalteng/
│
├── data/
│   ├── NASA_FIRMS_Hotspot_Juli_2026.tif
│   ├── NASA_FIRMS_Hotspot_Agustus_2026.tif
│   ├── NASA_FIRMS_Hotspot_September_2026.tif
│   ├── Sentinel5P_HCHO_September_2026.tif
│   ├── Sentinel5P_NO2_September_2026.tif
│   ├── Sentinel5P_Aerosol_Index_September_2026.tif
│   └── Pulang_Pisau_AOI.geojson
│
├── figures/
│   ├── Pulang_Pisau_Study_Area_Map.png
│   ├── Pulang_Pisau_Forest_Fire_Atmospheric_Pollution_September_2026.png
│   └── Pulang_Pisau_Sentinel5P_Atmospheric_Pollution_September_2026.png
│
├── scripts/
│   ├── study_area_map.py
│   ├── firms_monthly_visualization.py
│   ├── sentinel5p_visualization.py
│   └── visualisasi_pulang_pisau.py
│
└── README.md