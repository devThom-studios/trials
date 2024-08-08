import geopandas as gpd
import matplotlib.pyplot as plt

# Assuming points_gdf is your GeoDataFrame containing the points
# Create a buffer around each point (e.g., 0.1 degrees)
polygons_gdf = points_gdf.copy()
polygons_gdf['geometry'] = points_gdf.buffer(0.1)  # Adjust the buffer size as needed

# Optionally, set a CRS (Coordinate Reference System) if not already set
polygons_gdf = polygons_gdf.set_crs("EPSG:4326")

# View the polygons
print(polygons_gdf)

# Plot the polygons
polygons_gdf.plot(edgecolor='black')
plt.title('Polygons around points')
plt.show()
