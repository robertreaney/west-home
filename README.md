# House Hunter

This repo creates intelligent views of the USA to find a dream home for West & Kristi.

# Requirements

## Software

This repo uses these tools:

- [just](https://github.com/casey/just)
- [uv](https://github.com/astral-sh/uv)

## Data

These datasets need to be downloaded manually

- `data/usaairports.csv` - https://openintro.org/data/index.php?data=usairports
- `data/noaa/*` - run these bash commands from project root to get the data
    - `aws s3 sync s3://noaa-normals-pds/normals-annualseasonal/2006-2020/ data/noaa`
    - `aws s3 sync s3://noaa-normals-pds/normals-annualseasonal/access/ data/noaa/root_access`
- `data/census_shape/*` - https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
    - i used the smallest choice in `states` and then extracted everything to this folder

# Setup

- install tools above
- setup pyton env

`uv venv --python3.10`

- install packages

`uv sync`

# Run Stuff
Will better document this later, but go look at the `justfile` for stuff you can type. I gtg to bed so this is all janky right now :)

`just` <- runs end to end