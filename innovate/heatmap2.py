import folium
import numpy as np
import pandas as pd
from branca.colormap import linear

# the center point of Kagoshima
center_lat = 31.2518
center_lon = 130.6350

# generate a randome data set
np.random.seed()  # use the same seed just for repetition
points = 1500
latitudes =[]
longitudes = []
values = []
for i in range(points):
    latitudes.append((i-points/2)*0.0001 + center_lat)
    longitudes.append((i-points/2)*0.0001 + center_lon)
    if (abs(latitudes[i] - center_lat) < 0.002 and abs(longitudes[i] - center_lon) < 0.002):
        values.append((np.random.uniform(70, 100)))
    else: 
        values.append((np.random.uniform(0, 70))) # default values are under 70

# print(len(latitudes))

# generate a dataframe
data = pd.DataFrame({
    'lat': latitudes,
    'lon': longitudes,
    'value': values
})

# the size of each grid
grid_size = 0.0005

# generate a grid
lat_bins = np.arange(center_lat - 0.01, center_lat + 0.01, grid_size)
lon_bins = np.arange(center_lon - 0.01, center_lon + 0.01, grid_size)

# generate a color map
colormap = linear.YlOrRd_09.scale(0, 100)
# colormap = linear.viridis.scale(0, 100)

# generate a map
m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

# calculate datapoints within each grid and plot squares
for i in range(len(lat_bins) - 1):
    for j in range(len(lon_bins) - 1):
        # datapoints
        in_bin = data[
            (data['lat'] >= lat_bins[i]) & (data['lat'] < lat_bins[i + 1]) &
            (data['lon'] >= lon_bins[j]) & (data['lon'] < lon_bins[j + 1])
        ]
        
        if not in_bin.empty:
            # calculate the average
            bin_value = in_bin['value'].mean() if not in_bin.empty else 0
            color = colormap(bin_value)
            # color = get_color(bin_value)
            
            # four vertexes
            bounds = [
                [lat_bins[i], lon_bins[j]],
                [lat_bins[i], lon_bins[j + 1]],
                [lat_bins[i + 1], lon_bins[j + 1]],
                [lat_bins[i + 1], lon_bins[j]],
            ]
            
            # add a heatmap
            folium.Polygon(
                bounds,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)

# save the map
m.save('heatmap2.html')
