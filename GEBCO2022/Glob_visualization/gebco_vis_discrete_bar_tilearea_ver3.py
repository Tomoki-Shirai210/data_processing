import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from psutil import virtual_memory
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

plt.rcParams['font.family'] = 'Times New Roman'

def print_available_memory():
    mem = virtual_memory()
    available_gb = mem.available / 1024 / 1024 / 1024
    total_gb = mem.total / 1024 / 1024 / 1024
    print('Available memory: {:.2f} GB / {:.2f} GB ({:.2f} %)'.format(
        available_gb, total_gb, available_gb / total_gb * 100))

print_available_memory()

with netCDF4.Dataset('./GEBCO_2022.nc', 'r') as dataset:
    lon = dataset.variables['lon'][:]
    lat = dataset.variables['lat'][:]
    elevation = dataset.variables['elevation'][:]

step = 5
lon = lon[::step]
lat = lat[::step]
elevation = elevation[::step, ::step]

fig, ax = plt.subplots(figsize=(12, 12))

min_elevation, max_elevation = -11000, 10000
num_levels = (max_elevation - min_elevation) // 1000 + 1

levels = np.arange(min_elevation, max_elevation + 1000, 1000)
custom_cmap = plt.get_cmap('viridis', len(levels) - 1)
norm = mcolors.BoundaryNorm(levels, ncolors=len(levels) - 1)

im = ax.imshow(np.flipud(elevation), extent=(lon[0], lon[-1], lat[-1], lat[0]), cmap=custom_cmap, norm=norm, label='elevation')

red_mask = np.logical_and(elevation >= -10, elevation < 0)

rectangles=[]

for i in range(red_mask.shape[0] - 1):
    for j in range(red_mask.shape[1] - 1):
        if red_mask[i, j]:
            rect = Rectangle((lon[j], lat[-1 - i]), lon[j + 1] - lon[j], lat[-1 - i] - lat[-2 - i], edgecolor='none', facecolor='red')
            rectangles.append(rect)

pc = PatchCollection(rectangles, match_original=True)
ax.add_collection(pc)

ax.set_xlabel('longitude', fontsize=20)
ax.set_ylabel('latitude', fontsize=20)
ax.tick_params(labelsize=16)
ax.set_title('GEBCO_2022 ({}% resolution of original)'.format(
    round(100/step, 1)), fontsize=24)

cbar = fig.colorbar(im, ax=ax, label='elevation (m)', shrink=0.8, pad=0.05, boundaries=levels, ticks=levels)
cbar.ax.set_ylabel('elevation (m)', fontsize=20)
cbar.ax.tick_params(labelsize=16)
plt.subplots_adjust(bottom=0.15)
plt.tight_layout()

print_available_memory()

plt.savefig('glob_elv_gebco.png', dpi=1200)
#plt.show()

# Calculate the difference between latitudes and longitudes
lat_diff = np.diff(lat)
lon_diff = np.diff(lon)

# Convert latitudes and longitudes to radians
lat_rad = np.deg2rad(lat)
lon_rad = np.deg2rad(lon)

# Calculate the differences between adjacent latitudes and longitudes in radians
lat_diff_rad = np.deg2rad(lat_diff)
lon_diff_rad = np.deg2rad(lon_diff)

# Calculate the tile areas using spherical law of cosines
tile_areas = np.outer(lat_diff_rad, lon_diff_rad) * (6371.0 ** 2) * np.outer(np.cos(lat_rad[:-1]), np.ones_like(lon_diff))

# Calculate the mean and standard deviation of the tile areas
tile_areas_mean = np.mean(tile_areas)
tile_areas_std = np.std(tile_areas)

print(f"Tile area mean: {tile_areas_mean:.6f} km^2")
print(f"Tile area standard deviation: {tile_areas_std:.6f} km^2")

# Count the number of tiles with elevation between -10 and 0
num_tiles = np.sum((elevation >= -10) & (elevation < 0))

print(f"Number of tiles with elevation between -10 and 0: {num_tiles}")


# Plot histogram of elevation values in the range -100 to -10 m
mask = np.logical_and(elevation >= -100, elevation < 0)
elevation_subset = elevation[mask]

plt.figure()
plt.hist(elevation_subset.flatten(), bins=50, color='b', edgecolor='k', alpha=0.7)
plt.xlabel('Elevation (m)', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
plt.title('Histogram of Elevation Values', fontsize=24)
plt.tick_params(labelsize=16)
plt.grid(True)

plt.tight_layout()

plt.savefig('elevation_histogram_subset.png', dpi=1200)
#plt.show()

