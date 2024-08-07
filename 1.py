import numpy as np
import xarray as xr

# Step 1: Define the dimensions
time_dim = 540  # Number of time steps
i_dim = 120     # i dimension size
j_dim = 360     # j dimension size

# Step 2: Assume you have your actual data
# Replace the following example data with your actual arrays
time = np.arange(time_dim)  # Replace with your actual time array
lon = np.random.uniform(low=-180, high=180, size=(i_dim, j_dim))  # Replace with your actual lon(i,j) array
lat = np.random.uniform(low=-90, high=90, size=(i_dim, j_dim))    # Replace with your actual lat(i,j) array
thick = np.random.random(size=(time_dim, i_dim, j_dim))           # Replace with your actual thick(time, i, j) array

# Step 3: Create the initial xarray Dataset with lon and lat as variables
ds = xr.Dataset(
    {
        'thick': (['time', 'i', 'j'], thick),
        'lon': (['i', 'j'], lon),
        'lat': (['i', 'j'], lat)
    },
    coords={
        'time': time
    }
)

# Step 4: Flatten the lon and lat arrays for the interpolation step
lon_flat = ds['lon'].values.flatten()
lat_flat = ds['lat'].values.flatten()

# Create a 2D mesh grid for the target lat/lon grid
lon_new = np.linspace(lon_flat.min(), lon_flat.max(), j_dim)
lat_new = np.linspace(lat_flat.min(), lat_flat.max(), i_dim)
lon_grid, lat_grid = np.meshgrid(lon_new, lat_new)

# Step 5: Interpolate thick to the regular lat/lon grid
thick_interp = xr.apply_ufunc(
    np.vectorize(np.interp),
    lat_grid, lon_grid, lat_flat, lon_flat,
    ds['thick'].values.reshape((time_dim, -1)),
    vectorize=True,
    input_core_dims=[['lat', 'lon'], ['lat', 'lon'], ['lat', 'lon'], ['lat', 'lon'], ['time', 'space']],
    output_core_dims=[['time', 'lat', 'lon']]
)

# Reshape the interpolated data back into the new lat/lon dimensions
thick_interp = thick_interp.reshape((time_dim, i_dim, j_dim))

# Step 6: Update the Dataset with the new dimensions
ds_final = xr.Dataset(
    {
        'thick': (['time', 'lat', 'lon'], thick_interp)
    },
    coords={
        'time': time,
        'lat': lat_new,
        'lon': lon_new
    }
)

# Step 7: Verify the structure
print(ds_final)
