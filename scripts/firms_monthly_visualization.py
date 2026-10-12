import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import geopandas as gpd
from matplotlib.colors import Normalize


# ============================================================
# NASA FIRMS FIRE-DETECTION ACTIVITY
# PULANG PISAU REGENCY, CENTRAL KALIMANTAN, INDONESIA
# JULY - SEPTEMBER 2026
# ============================================================


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
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
# FILES
# ============================================================

JULY_FILE = os.path.join(
    DATA_DIR,
    "NASA_FIRMS_Hotspot_Juli_2026.tif"
)

AUGUST_FILE = os.path.join(
    DATA_DIR,
    "NASA_FIRMS_Hotspot_Agustus_2026.tif"
)

SEPTEMBER_FILE = os.path.join(
    DATA_DIR,
    "NASA_FIRMS_Hotspot_September_2026.tif"
)

AOI_FILE = os.path.join(
    DATA_DIR,
    "Pulang_Pisau_AOI.geojson"
)


# ============================================================
# CHECK FILES
# ============================================================

for file_path in [
    JULY_FILE,
    AUGUST_FILE,
    SEPTEMBER_FILE,
    AOI_FILE
]:

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File tidak ditemukan:\n{file_path}"
        )


# ============================================================
# READ RASTER
# ============================================================

def read_raster(path):

    with rasterio.open(path) as src:

        data = src.read(1).astype(float)

        bounds = src.bounds

        raster_crs = src.crs

        nodata = src.nodata

    if nodata is not None:

        data[data == nodata] = np.nan

    data[~np.isfinite(data)] = np.nan

    return data, bounds, raster_crs


# ============================================================
# LOAD DATA
# ============================================================

july, july_bounds, raster_crs = read_raster(
    JULY_FILE
)

august, august_bounds, _ = read_raster(
    AUGUST_FILE
)

september, september_bounds, _ = read_raster(
    SEPTEMBER_FILE
)


# ============================================================
# LOAD AOI
# ============================================================

aoi = gpd.read_file(
    AOI_FILE
)


# ============================================================
# MATCH AOI CRS WITH RASTER CRS
# ============================================================

if aoi.crs != raster_crs:

    aoi = aoi.to_crs(
        raster_crs
    )


# ============================================================
# GET RASTER EXTENT
# ============================================================

def get_extent(bounds):

    return [
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ]


# ============================================================
# MASK ZERO VALUES
# ============================================================

july_plot = np.ma.masked_where(
    ~np.isfinite(july) | (july <= 0),
    july
)

august_plot = np.ma.masked_where(
    ~np.isfinite(august) | (august <= 0),
    august
)

september_plot = np.ma.masked_where(
    ~np.isfinite(september) | (september <= 0),
    september
)


# ============================================================
# COMMON COLOR SCALE
# ============================================================

all_values = np.concatenate([
    july_plot.compressed(),
    august_plot.compressed(),
    september_plot.compressed()
])


if len(all_values) > 0:

    vmax = np.percentile(
        all_values,
        98
    )

else:

    vmax = 1


norm = Normalize(
    vmin=0,
    vmax=vmax
)


# ============================================================
# CREATE FIGURE
# ============================================================

fig, axes = plt.subplots(
    1,
    3,
    figsize=(18, 9)
)


# ============================================================
# MAIN TITLE
# ============================================================

fig.text(
    0.5,
    0.955,
    "NASA FIRMS Fire-Detection Activity",
    ha="center",
    va="center",
    fontsize=23,
    fontweight="bold"
)


# ============================================================
# SUBTITLE
# ============================================================

fig.text(
    0.5,
    0.915,
    "Pulang Pisau Regency, Central Kalimantan, Indonesia | July – September 2026",
    ha="center",
    va="center",
    fontsize=14
)


# ============================================================
# DATA FOR EACH MONTH
# ============================================================

monthly_data = [

    (
        axes[0],
        july_plot,
        july_bounds,
        "July 2026"
    ),

    (
        axes[1],
        august_plot,
        august_bounds,
        "August 2026"
    ),

    (
        axes[2],
        september_plot,
        september_bounds,
        "September 2026"
    )

]


# ============================================================
# PLOT MONTHLY MAPS
# ============================================================

for ax, data, bounds, month in monthly_data:

    # --------------------------------------------------------
    # FIRMS raster
    # --------------------------------------------------------

    im = ax.imshow(
        data,
        extent=get_extent(bounds),
        origin="upper",
        cmap="hot",
        norm=norm,
        interpolation="nearest"
    )


    # --------------------------------------------------------
    # AOI BOUNDARY
    # --------------------------------------------------------

    aoi.boundary.plot(
        ax=ax,
        color="black",
        linewidth=1.5
    )


    # --------------------------------------------------------
    # MONTH TITLE
    # --------------------------------------------------------

    ax.set_title(
        month,
        fontsize=17,
        fontweight="bold",
        pad=10
    )


    # --------------------------------------------------------
    # AXIS LABEL
    # --------------------------------------------------------

    ax.set_xlabel(
        "Longitude",
        fontsize=11
    )

    ax.set_ylabel(
        "Latitude",
        fontsize=11
    )


    # --------------------------------------------------------
    # TICKS
    # --------------------------------------------------------

    ax.tick_params(
        axis="both",
        labelsize=9
    )


    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    ax.grid(
        True,
        linestyle="--",
        linewidth=0.5,
        alpha=0.20
    )


    # --------------------------------------------------------
    # GEOGRAPHIC PROPORTION
    # --------------------------------------------------------

    ax.set_aspect(
        "equal"
    )


    # --------------------------------------------------------
    # FRAME
    # --------------------------------------------------------

    for spine in ax.spines.values():

        spine.set_linewidth(
            1.1
        )

# ============================================================
# COLORBAR
# ============================================================

cbar = fig.colorbar(
    im,
    ax=axes,
    orientation="vertical",
    fraction=0.025,
    pad=0.025
)


cbar.set_label(
    "FIRMS Fire-Detection Activity",
    fontsize=11,
    labelpad=10
)


cbar.ax.tick_params(
    labelsize=9
)


# ============================================================
# FINAL LAYOUT
# ============================================================

plt.subplots_adjust(
    left=0.055,
    right=0.91,
    bottom=0.10,
    top=0.82,
    wspace=0.25
)


# ============================================================
# OUTPUT FILE
# ============================================================

output_path = os.path.join(
    FIGURE_DIR,
    "Pulang_Pisau_NASA_FIRMS_Fire_Detection_July_September_2026.png"
)


# ============================================================
# SAVE
# ============================================================

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)


# ============================================================
# SHOW
# ============================================================

plt.show()


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print()
print("============================================================")
print("NASA FIRMS MONTHLY VISUALIZATION COMPLETED SUCCESSFULLY")
print("============================================================")
print("Study Area : Pulang Pisau Regency")
print("Period     : July - September 2026")
print("Output:")
print(output_path)
print("============================================================")