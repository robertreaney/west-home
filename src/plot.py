from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd

from src.constants import BOUNDING_BOX

def snowfall(gdf_points):
    # Load a GeoDataFrame with the USA map (you can use a shapefile or GeoJSON file)
    usa_map = gpd.read_file('data/census_shape/cb_2018_us_state_500k.shp')
    # usa_map = usa_map.set_crs(epsg=4326, allow_override=True)  # Set CRS to WGS84

    # usa_map = usa_map[usa_map['name'] == 'United States']

    # gdf_points = gpd.read_file('data/output/points.geojson')
    # gdf_points = gdf_points.set_crs(epsg=4326, allow_override=True)  # Set CRS to WGS84

    gdf_points.columns
    # gdf_points = gdf_points[~gdf_points['ANN-SNOW-AVGNDS-GE030TI'].isna()]
    gdf_points = gdf_points[~gdf_points['IS_VALID'].isna()]

    Path('plot.png').unlink(missing_ok=True) # idk why my machine is making me do this

    # Plot the map and overlay the points
    fig, ax = plt.subplots(figsize=(12, 8))
    usa_map.plot(ax=ax, color='lightgray', edgecolor='black')  # Plot the USA map
    gdf_points.plot(ax=ax, color=gdf_points['IS_VALID'].map({1.0: 'green', 0.: 'red'}), markersize=5, alpha=0.7)  # Overlay the points

    ax.set_xlim(BOUNDING_BOX['min_lon'], BOUNDING_BOX['max_lon'])
    ax.set_ylim(BOUNDING_BOX['min_lat'], BOUNDING_BOX['max_lat'])

    ax.set_box_aspect((BOUNDING_BOX['max_lat'] - BOUNDING_BOX['min_lat']) / (BOUNDING_BOX['max_lon'] - BOUNDING_BOX['min_lon']))

    # Add labels and grid
    plt.title('Latitude and Longitude Points on USA Map')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig('snowfall.png', dpi=300, bbox_inches='tight')

    plt.close('all')

    print('Plot saved as plot.png')