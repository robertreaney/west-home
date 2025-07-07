import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import structlog as sl

from src.constants import BOUNDING_BOX
from src.utils import dms_to_decimal

logger = sl.get_logger(__name__)

# Load airport data
airports = pd.read_csv('data/usairports.csv')  # Replace with your actual file path

# public only
airports = airports[airports.use == 'PU']

airports.columns
airports.head()

# # checkout some airports we know for cert types
# airports[airports.location_id.str.contains('RDU')].to_dict(orient='records')
# airports[airports.location_id.str.contains('CLT')].to_dict(orient='records')
# airports[airports.location_id.str.contains('ORF')].to_dict(orient='records')

# airports[airports.state=='VA'].location_id.unique()

# from rdu. gives 23 airports
a = airports[airports.cert_type_date.str.contains('I D S', na=False)]

# fromc lt. gives 28
# b = airports[airports.cert_type_date.str.contains('I E S', na=False)]
b = airports[airports.cert_type_date.str.contains('I', na=False)]

airports = pd.concat([a, b], ignore_index=True)

airports['arp_longitude'] = airports['arp_longitude'].apply(dms_to_decimal)
airports['arp_latitude'] = airports['arp_latitude'].apply(dms_to_decimal)

gdf_airports = gpd.GeoDataFrame(
    airports,
    geometry=gpd.points_from_xy(airports['arp_longitude'], airports['arp_latitude'])
)


# Set CRS for the airports (assuming WGS84)
gdf_airports = gdf_airports.set_crs(epsg=4326, allow_override=True)

# Reproject to a CRS that uses meters (e.g., EPSG:3395)
gdf_airports = gdf_airports.to_crs(epsg=3395)

# Create buffer zones (100 miles = 160934 meters)
gdf_airports['buffer'] = gdf_airports.geometry.buffer(160934)

# Convert back to WGS84 for plotting
gdf_airports = gdf_airports.to_crs(epsg=4326)

# Load USA map
usa_map = gpd.read_file('data/census_shape/cb_2018_us_state_500k.shp')

# Check the CRS of the USA map GeoDataFrame
print("USA Map CRS:", usa_map.crs)

usa_map = usa_map.set_crs(epsg=4326, allow_override=True)

# Plot the map and overlay the buffers
fig, ax = plt.subplots(figsize=(16, 10))
usa_map.plot(ax=ax, color='lightgray', edgecolor='black')  # Plot the USA map
gdf_airports.plot(ax=ax, color='red', markersize=5, alpha=0.7)  # Plot airport points
gpd.GeoDataFrame(geometry=gdf_airports['buffer']).plot(ax=ax, color='blue', alpha=0.3)  # Plot buffer zones


ax.set_xlim(BOUNDING_BOX['min_lon'], BOUNDING_BOX['max_lon'])
ax.set_ylim(BOUNDING_BOX['min_lat'], BOUNDING_BOX['max_lat'])

ax.set_box_aspect((BOUNDING_BOX['max_lat'] - BOUNDING_BOX['min_lat']) / (BOUNDING_BOX['max_lon'] - BOUNDING_BOX['min_lon']))

# Add labels and grid
plt.title('Areas Within 100 Miles of Airports')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

# Save the figure
plt.savefig('plot_airports.png', dpi=300, bbox_inches='tight')

plt.close('all')

print('Plot saved as plot_airports.png')