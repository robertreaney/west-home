import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

from src.constants import BOUNDING_BOX

def dms_to_decimal(dms):
    try:
        # Remove directional letters and split the DMS string into components
        dms = dms.strip().upper()  # Ensure consistent formatting
        parts = dms.replace('W', '').replace('E', '').replace('N', '').replace('S', '').split('-')
        
        # Ensure the DMS string has exactly 3 components (degrees, minutes, seconds)
        if len(parts) != 3:
            raise ValueError(f"Invalid DMS format: {dms}")
        
        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        
        # Convert to decimal degrees
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        
        # Handle negative values for west and south coordinates
        if 'W' in dms or 'S' in dms:
            decimal = -decimal
        
        return decimal
    except Exception as e:
        print(f"Error converting DMS to decimal: {e}")
        return None  # Return None for invalid DMS strings

# Example DMS strings
dms_values = [
    "176-38-32.9277W",
    "37-46-44.9277N",
    "122-25-9.9277W",
    "INVALID-DMS"
]

# Convert DMS to decimal degrees
for dms in dms_values:
    print(f"DMS: {dms} -> Decimal: {dms_to_decimal(dms)}")

# Load airport data
airports = pd.read_csv('data/usairports.csv')  # Replace with your actual file path

# public only
airports = airports[airports.use == 'PU']

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