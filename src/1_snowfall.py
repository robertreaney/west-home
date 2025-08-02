import pandas as pd
from pathlib import Path
import geopandas as gpd
import numpy as np

from src.constants import STATES
from src.plot import snowfall

#### 1) GET LAT/LON WITH DESIREABLE WEATHER
print('calculating snowfall filter..')

# weather cols we need
cols = ['STATION','LATITUDE','LONGITUDE', 'ELEVATION','NAME', 'ANN-SNOW-NORMAL','ANN-SNOW-AVGNDS-GE030TI']

# load noaa weather data
usecols = lambda x: x in cols
climate = pd.concat((pd.read_csv(f, usecols=usecols) for f in Path('data/noaa/root_access').rglob("*.csv")), ignore_index=True)

climate['STATE'] = climate.NAME.str.split(" ").str[-2]

# filter out only desired states
climate = climate[climate.STATE.isin(STATES)]

# climate.head()
# climate.describe()
# ann-snwd-avgnds-ge005wi 

# climate['ANN-SNOW-NORMAL'].isna().sum() / climate.shape[0]  # 35% empty
# climate['ANN-SNOW-NORMAL'].describe()
# climate.shape

# HERE ARE SOME FILTERS WE HAVE TESTED? data isn't well documented but you can change these and view the plot it creates

# # Filter the climate data for points with ANN-SNOW-NORMAL > 36
# df = climate[climate['ANN-SNOW-NORMAL'] > 48]
# df = climate[climate['ANN-SNOW-AVGNDS-GE030TI'] >= 17]
# df

# climate['IS_VALID'] = (climate['ANN-SNOW-AVGNDS-GE030TI'] >= 15)
climate['IS_VALID'] = np.where(
    climate['ANN-SNOW-AVGNDS-GE030TI'].isna(),
    np.nan,
    climate['ANN-SNOW-AVGNDS-GE030TI'] >= 10
)

df = climate.copy()

# Create a GeoDataFrame for the points
gdf_points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']),
)

# Save the GeoDataFrame to a GeoJSON file
gdf_points.to_file('data/output/snowfall.geojson', driver='GeoJSON')

snowfall(gdf_points)

print('Done!')