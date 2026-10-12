import os
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
from matplotlib.colors import Normalize
from matplotlib.ticker import ScalarFormatter


# ============================================================
# SENTINEL-5P ATMOSPHERIC POLLUTION VISUALIZATION
# PULANG PISAU REGENCY, CENTRAL KALIMANTAN, INDONESIA
# SEPTEMBER 2026
# ============================================================


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

FIGURE_DIR = os.path.join(
    BASE_DIR,
    "figures"
)

os.makedirs(
    FIGURE_DIR,
    exist_ok=True
)


# ============================================================
# INPUT FILES
# ============================================================

HCHO_FILE = "Sentinel5P_HCHO_September_2026.tif"

NO2_FILE = "Sentinel5P_NO2_September_2026.tif"

AEROSOL_FILE = "Sentinel5P_Aerosol_Index_September_2026.tif"

AOI_FILE = "Pulang_Pisau_AOI.geojson"


# ============================================================
# READ RASTER
# ============================================================

def read_raster(filename):

    path = os.path.join(
        DATA_DIR,
        filename
    )

    with rasterio.open(path) as src:

        data = src.read(1).astype(float)

        bounds = src.bounds

        nodata = src.nodata

        crs = src.crs

    if nodata is not None:

        data[data == nodata] = np.nan

    data[~np.isfinite(data)] = np.nan

    return data, bounds, crs


# ============================================================
# LOAD RASTERS
# ============================================================

hcho, hcho_bounds, hcho_crs = read_raster(
    HCHO_FILE
)

no2, no2_bounds, no2_crs = read_raster(
    NO2_FILE
)

aerosol, aerosol_bounds, aerosol_crs = read_raster(
    AEROSOL_FILE
)


# ============================================================
# LOAD AOI
# ============================================================

aoi_path = os.path.join(
    DATA_DIR,
    AOI_FILE
)

aoi = gpd.read_file(
    aoi_path
)

if aoi.crs != hcho_crs:

    aoi = aoi.to_crs(
        hcho_crs
    )


# ============================================================
# EXTENT
# ============================================================

def get_extent(bounds):

    return [
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ]


# ============================================================
# MASK INVALID VALUES
# ============================================================

hcho_plot = np.ma.masked_invalid(
    hcho
)

no2_plot = np.ma.masked_invalid(
    no2
)

aerosol_plot = np.ma.masked_invalid(
    aerosol
)


# ============================================================
# COLOR LIMITS
# ============================================================

def get_percentile_limits(data):

    values = data[
        np.isfinite(data)
    ]

    if len(values) == 0:

        return 0, 1

    vmin = np.percentile(
        values,
        2
    )

    vmax = np.percentile(
        values,
        98
    )

    if vmin == vmax:

        vmax = vmin + 1

    return vmin, vmax


hcho_vmin, hcho_vmax = get_percentile_limits(
    hcho
)

no2_vmin, no2_vmax = get_percentile_limits(
    no2
)

aerosol_vmin, aerosol_vmax = get_percentile_limits(
    aerosol
)


# ============================================================
# FIGURE
# ============================================================

fig, axes = plt.subplots(
    1,
    3,
    figsize=(18, 7.5)
)


# ============================================================
# MAIN TITLE
# ============================================================

fig.suptitle(
    "Sentinel-5P Atmospheric Pollution Indicators",
    fontsize=19,
    fontweight="bold",
    y=0.965
)

fig.text(
    0.5,
    0.905,
    "Pulang Pisau Regency, Central Kalimantan, Indonesia | September 2026",
    ha="center",
    va="center",
    fontsize=11
)

# ============================================================
# COLOR MAP
# ============================================================

map_cmap = "YlOrRd"


# ============================================================
# PANEL 1
# HCHO
# ============================================================

ax = axes[0]

im1 = ax.imshow(
    hcho_plot,
    extent=get_extent(
        hcho_bounds
    ),
    origin="upper",
    cmap=map_cmap,
    interpolation="nearest",
    norm=Normalize(
        vmin=hcho_vmin,
        vmax=hcho_vmax
    )
)

aoi.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.2
)

ax.set_title(
    "HCHO",
    fontsize=13,
    fontweight="bold",
    pad=8
)

ax.set_xlabel(
    "Longitude",
    fontsize=10
)

ax.set_ylabel(
    "Latitude",
    fontsize=10
)

cbar1 = fig.colorbar(
    im1,
    ax=ax,
    fraction=0.040,
    pad=0.025
)

cbar1.set_label(
    "Tropospheric HCHO Column Density",
    fontsize=8
)

cbar1.ax.tick_params(
    labelsize=8
)

formatter1 = ScalarFormatter(
    useMathText=True
)

formatter1.set_powerlimits(
    (-3, 3)
)

cbar1.ax.yaxis.set_major_formatter(
    formatter1
)


# ============================================================
# PANEL 2
# NO2
# ============================================================

ax = axes[1]

im2 = ax.imshow(
    no2_plot,
    extent=get_extent(
        no2_bounds
    ),
    origin="upper",
    cmap=map_cmap,
    interpolation="nearest",
    norm=Normalize(
        vmin=no2_vmin,
        vmax=no2_vmax
    )
)

aoi.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.2
)

ax.set_title(
    "NO₂",
    fontsize=13,
    fontweight="bold",
    pad=8
)

ax.set_xlabel(
    "Longitude",
    fontsize=10
)

ax.set_ylabel(
    "Latitude",
    fontsize=10
)

cbar2 = fig.colorbar(
    im2,
    ax=ax,
    fraction=0.040,
    pad=0.025
)

cbar2.set_label(
    "Tropospheric NO₂ Column Density",
    fontsize=8
)

cbar2.ax.tick_params(
    labelsize=8
)

formatter2 = ScalarFormatter(
    useMathText=True
)

formatter2.set_powerlimits(
    (-3, 3)
)

cbar2.ax.yaxis.set_major_formatter(
    formatter2
)


# ============================================================
# PANEL 3
# ABSORBING AEROSOL INDEX
# ============================================================

ax = axes[2]

im3 = ax.imshow(
    aerosol_plot,
    extent=get_extent(
        aerosol_bounds
    ),
    origin="upper",
    cmap=map_cmap,
    interpolation="nearest",
    norm=Normalize(
        vmin=aerosol_vmin,
        vmax=aerosol_vmax
    )
)

aoi.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.2
)

ax.set_title(
    "Absorbing Aerosol Index",
    fontsize=13,
    fontweight="bold",
    pad=8
)

ax.set_xlabel(
    "Longitude",
    fontsize=10
)

ax.set_ylabel(
    "Latitude",
    fontsize=10
)

cbar3 = fig.colorbar(
    im3,
    ax=ax,
    fraction=0.040,
    pad=0.025
)

cbar3.set_label(
    "Absorbing Aerosol Index",
    fontsize=8
)

cbar3.ax.tick_params(
    labelsize=8
)


# ============================================================
# MAP FORMATTING
# ============================================================

for ax in axes:

    ax.grid(
        True,
        alpha=0.20,
        linewidth=0.5,
        linestyle="--"
    )

    ax.tick_params(
        axis="both",
        labelsize=8
    )

    ax.set_aspect(
        "equal"
    )

    for spine in ax.spines.values():

        spine.set_linewidth(
            1.0
        )


# ============================================================
# LAYOUT
# ============================================================

plt.subplots_adjust(
    left=0.055,
    right=0.945,
    bottom=0.10,
    top=0.80,
    wspace=0.32
)


# ============================================================
# SAVE FIGURE
# ============================================================

output_path = os.path.join(
    FIGURE_DIR,
    "Pulang_Pisau_Sentinel5P_Atmospheric_Pollution_September_2026.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)


# ============================================================
# DISPLAY
# ============================================================

plt.show()


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print()
print("============================================================")
print("SENTINEL-5P VISUALIZATION COMPLETED SUCCESSFULLY")
print("============================================================")
print("Output file:")
print(output_path)
print("============================================================")