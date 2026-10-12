import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from matplotlib.colors import Normalize

# ============================================================
# FOREST FIRE AND ATMOSPHERIC POLLUTION VISUALIZATION
# PULANG PISAU REGENCY, CENTRAL KALIMANTAN, INDONESIA
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

# Create output directory if it does not exist
os.makedirs(
    FIGURE_DIR,
    exist_ok=True
)


# ============================================================
# RASTER READING FUNCTION
# ============================================================

def read_raster(filename):
    """
    Read a single-band GeoTIFF raster.
    """

    path = os.path.join(
        DATA_DIR,
        filename
    )

    with rasterio.open(path) as src:

        data = src.read(1).astype(float)

        bounds = src.bounds

        nodata = src.nodata

    # Remove NoData values
    if nodata is not None:

        data[data == nodata] = np.nan

    # Remove invalid values
    data[~np.isfinite(data)] = np.nan

    return data, bounds


# ============================================================
# LOAD RASTER DATA
# ============================================================

firms, firms_bounds = read_raster(
    "NASA_FIRMS_Hotspot_September_2026.tif"
)

hcho, hcho_bounds = read_raster(
    "Sentinel5P_HCHO_September_2026.tif"
)

no2, no2_bounds = read_raster(
    "Sentinel5P_NO2_September_2026.tif"
)

aerosol, aerosol_bounds = read_raster(
    "Sentinel5P_Aerosol_Index_September_2026.tif"
)


# ============================================================
# EXTENT FUNCTION
# ============================================================

def get_extent(bounds):

    return [
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ]


# ============================================================
# NASA FIRMS MASK
# ============================================================

firms_plot = np.ma.masked_where(
    ~np.isfinite(firms) | (firms <= 0),
    firms
)


# ============================================================
# ATMOSPHERIC POLLUTANT MASKS
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
# CREATE FIGURE
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(16, 12)
)


# ============================================================
# MAIN TITLE
# ============================================================

fig.suptitle(
    "Forest Fire and Atmospheric Pollution Monitoring\n"
    "Pulang Pisau Regency, Central Kalimantan, Indonesia\n"
    "September 2026",
    fontsize=17,
    fontweight="bold",
    ha="center",
    va="top",
    y=0.98,
    linespacing=1.35
)

# ============================================================
# 1. NASA FIRMS ACTIVE FIRE HOTSPOTS
# ============================================================

ax = axes[0, 0]

im1 = ax.imshow(
    firms_plot,
    extent=get_extent(firms_bounds),
    origin="upper",
    cmap="hot",
    interpolation="nearest",
    aspect="auto"
)

ax.set_title(
    "NASA FIRMS Active Fire Hotspots",
    fontsize=12,
    fontweight="bold",
    pad=12
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
    fraction=0.045,
    pad=0.025
)

cbar1.set_label(
    "Hotspot Detection",
    fontsize=9
)

cbar1.ax.tick_params(
    labelsize=8
)


# ============================================================
# 2. SENTINEL-5P HCHO
# ============================================================

ax = axes[0, 1]

hcho_values = hcho_plot.compressed()

if len(hcho_values) > 0:

    hcho_vmin = np.percentile(
        hcho_values,
        2
    )

    hcho_vmax = np.percentile(
        hcho_values,
        98
    )

else:

    hcho_vmin = 0

    hcho_vmax = 1


im2 = ax.imshow(
    hcho_plot,
    extent=get_extent(hcho_bounds),
    origin="upper",
    cmap="YlOrRd",
    interpolation="nearest",
    norm=Normalize(
        vmin=hcho_vmin,
        vmax=hcho_vmax
    ),
    aspect="auto"
)

ax.set_title(
    "Sentinel-5P Formaldehyde (HCHO)",
    fontsize=12,
    fontweight="bold",
    pad=12
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
    fraction=0.045,
    pad=0.025
)

cbar2.set_label(
    "Tropospheric HCHO Column Density",
    fontsize=9
)

cbar2.ax.tick_params(
    labelsize=8
)


# ============================================================
# 3. SENTINEL-5P NO2
# ============================================================

ax = axes[1, 0]

no2_values = no2_plot.compressed()

if len(no2_values) > 0:

    no2_vmin = np.percentile(
        no2_values,
        2
    )

    no2_vmax = np.percentile(
        no2_values,
        98
    )

else:

    no2_vmin = 0

    no2_vmax = 1


im3 = ax.imshow(
    no2_plot,
    extent=get_extent(no2_bounds),
    origin="upper",
    cmap="YlOrRd",
    interpolation="nearest",
    norm=Normalize(
        vmin=no2_vmin,
        vmax=no2_vmax
    ),
    aspect="auto"
)

ax.set_title(
    "Sentinel-5P Nitrogen Dioxide (NO₂)",
    fontsize=12,
    fontweight="bold",
    pad=12
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
    fraction=0.045,
    pad=0.025
)

cbar3.set_label(
    "Tropospheric NO₂ Column Density",
    fontsize=9
)

cbar3.ax.tick_params(
    labelsize=8
)


# ============================================================
# 4. SENTINEL-5P ABSORBING AEROSOL INDEX
# ============================================================

ax = axes[1, 1]

aerosol_values = aerosol_plot.compressed()

if len(aerosol_values) > 0:

    aerosol_vmin = np.percentile(
        aerosol_values,
        2
    )

    aerosol_vmax = np.percentile(
        aerosol_values,
        98
    )

else:

    aerosol_vmin = -1

    aerosol_vmax = 1


im4 = ax.imshow(
    aerosol_plot,
    extent=get_extent(aerosol_bounds),
    origin="upper",
    cmap="YlOrRd",
    interpolation="nearest",
    norm=Normalize(
        vmin=aerosol_vmin,
        vmax=aerosol_vmax
    ),
    aspect="auto"
)

ax.set_title(
    "Sentinel-5P Absorbing Aerosol Index",
    fontsize=12,
    fontweight="bold",
    pad=12
)

ax.set_xlabel(
    "Longitude",
    fontsize=10
)

ax.set_ylabel(
    "Latitude",
    fontsize=10
)

cbar4 = fig.colorbar(
    im4,
    ax=ax,
    fraction=0.045,
    pad=0.025
)

cbar4.set_label(
    "Absorbing Aerosol Index",
    fontsize=9
)

cbar4.ax.tick_params(
    labelsize=8
)


# ============================================================
# MAP FORMATTING
# ============================================================

for ax in axes.flat:

    # Grid
    ax.grid(
        True,
        alpha=0.20,
        linewidth=0.5
    )

    # Tick size
    ax.tick_params(
        axis="both",
        labelsize=8
    )

    # Keep tick labels readable
    ax.tick_params(
        axis="x",
        rotation=0
    )

    ax.tick_params(
        axis="y",
        rotation=0
    )


# ============================================================
# ADJUST FIGURE LAYOUT
# ============================================================

plt.subplots_adjust(
    left=0.07,
    right=0.93,
    bottom=0.07,
    top=0.78,
    wspace=0.32,
    hspace=0.30
)

# ============================================================
# SAVE OUTPUT
# ============================================================

output_path = os.path.join(
    FIGURE_DIR,
    "Pulang_Pisau_Forest_Fire_Atmospheric_Pollution_September_2026.png"
)

plt.savefig(
    output_path,
    dpi=300,
    facecolor="white"
)


# ============================================================
# DISPLAY FIGURE
# ============================================================

plt.show()


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print()
print("================================================")
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("================================================")
print("Output file:")
print(output_path)
print("================================================")