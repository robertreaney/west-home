import pandas as pd
from pathlib import Path
import geopandas as gpd

# airports = pd.read_csv('data/usairports.csv')
# airports

cols = ['STATION','LATITUDE','LONGITUDE', 'ELEVATION','NAME', 'ANN-SNOW-NORMAL','ANN-SNOW-AVGNDS-GE030TI']
# climate = pd.read_csv(next(Path('data/noaa/root_access').rglob("*.csv")))#, usecols=cols)
# [x for x in climate.columns if 'ann-snow' in x.lower()]

usecols = lambda x: x in cols
climate = pd.concat((pd.read_csv(f, usecols=usecols) for f in Path('data/noaa/root_access').rglob("*.csv")), ignore_index=True)

climate.head()
climate.describe()
# ann-snwd-avgnds-ge005wi 

climate['ANN-SNOW-NORMAL'].isna().sum() / climate.shape[0]  # 35% empty
climate['ANN-SNOW-NORMAL'].describe()
climate.shape

# Filter the climate data for points with ANN-SNOW-NORMAL > 36
df = climate[climate['ANN-SNOW-NORMAL'] > 48]
df = climate[climate['ANN-SNOW-AVGNDS-GE030TI'] >= 17]

# Create a GeoDataFrame for the points
gdf_points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE'])
)

# Save the GeoDataFrame to a GeoJSON file
gdf_points.to_file('data/output/points.geojson', driver='GeoJSON')

print('ETL Done!')