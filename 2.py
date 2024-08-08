import geopandas as gpd
from shapely.geometry import Polygon, Point
import numpy as np

# Define your polygon using a list of (longitude, latitude) tuples
coords = [(-60, 80), (-50, 82), (-40, 83), (-30, 80), (-60, 80)]  # Example coordinates
polygon = Polygon(coords)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[polygon])

# Generate a grid of points within the polygon
minx, miny, maxx, maxy = polygon.bounds
x_points = np.linspace(minx, maxx, 10)  # 10 points along longitude
y_points = np.linspace(miny, maxy, 10)  # 10 points along latitude

points = []
for x in x_points:
    for y in y_points:
        point = Point(x, y)
        if polygon.contains(point):
            points.append(point)

points_gdf = gpd.GeoDataFrame(geometry=points)

# Display the points
print(points_gdf)
