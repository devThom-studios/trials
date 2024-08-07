import numpy as np
import xarray as xr

# Step 1: Define the dimensions
time_dim = 540  # Number of time steps
i_dim = 120     # i dimension size
j_dim = 360     # j dimension size

# Step 2: Generate example data arrays (Replace these with your actual data)
time = np.arange(time_dim)  # Replace with your actual time array
lon = np.random.uniform(low=-180, high=180, size=(i_dim, j_dim))  # Replace with your actual lon(i,j) array
lat = np.random.uniform(low=-90, high=90, size=(i_dim, j_dim))    # Replace with your actual lat(i,j) array
thick = np.random.random(size=(time_dim, i_dim, j_dim))           # Replace with your actual thick(time, i, j) array

# Step 3: Create the initial xarray Dataset
ds = xr.Dataset(
    {
        'thick': (['time', 'i', 'j'], thick)
    },
    coords={
        'time': time,
        'lon': (['i', 'j'], lon),
        'lat': (['i', 'j'], lat)
    }
)

# Step 4: Create a regular grid for lat and lon
lat_new = np.linspace(lat.min(), lat.max(), i_dim)
lon_new = np.linspace(lon.min(), lon.max(), j_dim)

# Step 5: Interpolate the data onto this regular grid
thick_interp = ds['thick'].interp(lat=lat_new, lon=lon_new, method="linear")

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
