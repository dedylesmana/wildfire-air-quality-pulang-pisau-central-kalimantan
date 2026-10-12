import os
import geopandas as gpd
import matplotlib.pyplot as plt

# ============================================================
# STUDY AREA MAP
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

os.makedirs(
    FIGURE_DIR,
    exist_ok=True
)

# ============================================================
# LOAD PULANG PISAU AOI
# ============================================================

aoi_path = os.path.join(
    DATA_DIR,
    "Pulang_Pisau_AOI.geojson"
)

aoi = gpd.read_file(aoi_path)

# ============================================================
# CREATE STUDY AREA FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(10, 9)
)

# Plot AOI
aoi.plot(
    ax=ax,
    facecolor="none",
    edgecolor="black",
    linewidth=2.5
)

# ============================================================
# MAP TITLE
# ============================================================

ax.set_title(
    "Study Area",
    fontsize=22,
    fontweight="bold",
    pad=20
)

ax.text(
    0.5,
    1.01,
    "Pulang Pisau Regency, Central Kalimantan, Indonesia",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=13
)

# ============================================================
# AXIS LABELS
# ============================================================

ax.set_xlabel(
    "Longitude",
    fontsize=12,
    labelpad=8
)

ax.set_ylabel(
    "Latitude",
    fontsize=12,
    labelpad=8
)

# ============================================================
# GRID
# ============================================================

ax.grid(
    True,
    linestyle="--",
    linewidth=0.6,
    alpha=0.4
)

ax.tick_params(
    axis="both",
    labelsize=10
)

# ============================================================
# KEEP GEOGRAPHIC PROPORTION
# ============================================================

ax.set_aspect("equal")

# ============================================================
# CLEAN FRAME
# ============================================================

for spine in ax.spines.values():
    spine.set_linewidth(1.2)

# ============================================================
# SAVE OUTPUT
# ============================================================

output_path = os.path.join(
    FIGURE_DIR,
    "Pulang_Pisau_Study_Area_Map.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()

# ============================================================
# COMPLETION MESSAGE
# ============================================================

print()
print("================================================")
print("STUDY AREA MAP CREATED SUCCESSFULLY")
print("================================================")
print("Output file:")
print(output_path)
print("================================================")