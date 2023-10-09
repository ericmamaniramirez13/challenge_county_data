# %%
import polars as pl
import plotly.express as px
from datetime import datetime, timedelta
import polars.selectors as cs
import urllib.request
import json
import numpy as np

#%%
# Now get all the counties -- this is how I got the counties
# https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt
urllib.request.urlretrieve('https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt', 'disasters/counties.txt')
pass

# %%
# It's in basically a csv, but with | instead of ,
with open('disasters/counties.txt', 'r') as f:
    new = f.read().replace('|', ',')

with open('disasters/counties.csv', 'w') as f:
    f.write(new)

counties = pl.read_csv('disasters/counties.csv')

# %%
# We just want all the viable fips codes, basically
counties = counties.select(
    ( # This combines the state and county codes propery (ssccc, with padding 0's in county)
        pl.col('STATEFP').cast(str) + \
        pl.col('COUNTYFP').cast(str).str.rjust(3, '0')
    ).cast(pl.Int64).alias('fips'),)

# %%
# Get relevant disaster data
# Data dictionary
# https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2
# Data download
# https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv

# Based on the link, and looking at data for hurricane katrina, it seems like the counties
# where these programs were declared determines whether it was actually a serious disaster,
# or if it just kinda passed through there technically. (i.e. apparently katrina technically hit ID)
disasters = pl.read_csv('disasters/DisasterDeclarationsSummaries.csv')\
    .filter(pl.col('ihProgramDeclared').cast(pl.Boolean) | pl.col('iaProgramDeclared').cast(pl.Boolean))\
    .select(
    'incidentType',
    ( # This combines the state and county codes propery (ssccc, with padding 0's in county)
        pl.col('fipsStateCode').cast(str) + \
        pl.col('fipsCountyCode').cast(str).str.rjust(3, '0')
    ).cast(pl.Int64).alias('fips'),
)
disasters.head()

# %%
# Pivot the disaster data the way we want it
wideDisasters = disasters.pivot(
    values='incidentType',
    index='fips',
    columns='incidentType',
    aggregate_function='count',
).fill_null(0)\
    .drop('Biological', 'Other', 'Snowstorm', 'Dam/Levee Break', 'Freezing', 'Toxic Substances',
          'Drought', 'Human Cause', 'Fishing Losses', 'Chemical', 'Terrorist', 'Volcanic Eruption',
          'Severe Ice Storm', 'Mud/Landslide'
        )
    # These don't feel particularly relevant /|\
    # After looking at the data, it looks like for Volcanic Eruption, there's Hawaii (obviously),
    # and a few in Washington, which I realized must be Mt. St. Helen's. I'm removing it because
    # It seems like they know how to deal with them in Hawaii, and Mt. St. Helen's isn't gonna blow
    # again anytime soon

# %%
# Add the disasters to the data
labeledCounties = counties.join(wideDisasters, 'fips')


# %%
# Remove any columns that don't have any in them
drop = []
for c in labeledCounties.columns:
    if labeledCounties[c].dtype == pl.UInt32:
        if not labeledCounties[c].cast(pl.Boolean).any():
            drop.append(c)
labeledCounties = labeledCounties.drop(drop)

# %%
# If you have occational fires/floods/storms in the county, that's not indicative
# of a larger problem. We want to know if it's at significant risk
# This data does go all the way back to 1964 after all
filtered = labeledCounties.with_columns(
    # The thresholds I got from looking at the .describe() stats
    (pl.col('Fire') > 3).alias('Fire'),
    (pl.col('Flood') > 5).alias('Flood'),
    (pl.col('Severe Storm') > 3).alias('Severe Storm'),
    # ANY tonadoes are bad
    (pl.col('Tornado') > 0).alias('Tornado'),
    # By looking at https://www.fema.gov/disaster/how-declared, it looks like
    # The disaster has to be approved as a "major disaster" by the president
    # before it ends up here (if I'm reading this right), which shoud mean
    # the measly California quakes shouldn't be included
    (pl.col('Earthquake') > 0).alias('Earthquake'),
    (pl.col('Hurricane') > 0).alias('Hurricane'),
    (pl.col('Coastal Storm') > 0).alias('Coastal Storm'),
    (pl.col('Typhoon') > 0).alias('Typhoon'),
)
filtered.write_parquet('disasters/disasters_wide.parquet', use_pyarrow=True)
filtered.head()

# %%
# Just some quick code to make a long formatted version
filtered.melt('fips', variable_name='disaster')\
    .filter(pl.col('value').cast(pl.Boolean))\
    .drop('value')\
    .write_parquet('disasters/disasters_long.parquet', use_pyarrow=True)
