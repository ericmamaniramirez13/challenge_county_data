# %%
import polars as pl
import urllib.request
from urllib.request import urlopen
import json

# %%
# This is much better than what I was doing. This actually has the right amount of states
counties = pl.read_csv("https://github.com/kjhealy/fips-codes/raw/master/state_and_county_fips_master.csv")\
    .filter(pl.col("state") != "NA").drop('name')

# %%
# Get relevant disaster data
# Data dictionary
# https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2

# Based on the link, and looking at data for hurricane katrina, it seems like the counties
# where these programs were declared determines whether it was actually a serious disaster,
# or if it just kinda passed through there technically. (i.e. apparently katrina technically hit ID)
disasters = pl.read_csv('https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv')\
    .filter(pl.col('ihProgramDeclared').cast(pl.Boolean) | pl.col('iaProgramDeclared').cast(pl.Boolean))\
    .select(
    'incidentType',
    # 'state',
    ( # This combines the state and county codes propery (ssccc, with padding 0's in county)
        pl.col('fipsStateCode').cast(str) + \
        pl.col('fipsCountyCode').cast(str).str.rjust(3, '0')
    ).cast(pl.Int64).alias('fips'),
)

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
labeledCounties = counties.join(wideDisasters, 'fips', how='inner')

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
    # I'm justifying this because after making a grpah, it's not nearly as widespread
    # as i assumed. I think they're only counting wildfires after all
    (pl.col('Fire') > 0).alias('Fire'),
    (pl.col('Flood') > 3).alias('Flood'),
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
# Upon consideration (and several graphs), I'm not sure this is necissary after all.
# I think that just filtering based on the programs above is sufficent.

# %%
# Now write it properly distributed
# filtered.write_parquet('disasters/disasters.parquet', use_pyarrow=True)

# The size each will be
size = len(filtered) // 5
# Split them all up into a list of smaller datasets
split = [filtered[size*i:size*(i+1)] for i in range(4)]
# Becuase we're doing // instead of /, we might have an off-by-one error.
# This fixes that.
split.append(filtered[size*4:])
assert sum(map(len, split)) == len(filtered), "You split the dataset wrong"

# NOW actually write the data
for cnt, data in enumerate(split):
    data.write_parquet(f'disasters/disasters_{cnt}.parquet', use_pyarrow=True)



# %%
# Just some quick code to make a long formatted version
longFiltered = filtered.drop('state', 'state_right').melt('fips', variable_name='disaster')\
    .filter(pl.col('value').cast(pl.Boolean))\
    .drop('value')\
    .with_columns(pl.col('fips').cast(pl.Utf8).str.rjust(5,'0').alias('fips'))


# %%
# The problem here is that a bunch of counties have multiple disasters they have
# to deal with. That sucks for them, but it also sucks for us, because each county
# can only have 1 color. So what I'm doing here is prioritizing them so only the
# most worrisome is shown
# This is kind of a janky way of doing it, but I spend 2 hours trying to figure
# out how to do this, and this is the only way I could figure out.
def prioritize(r):
    if r[1]:
        rtn = 'Hurricane'
    elif r[4]:
        rtn = 'Tornado'
    elif r[6]:
        rtn = 'Earthquake'
    elif r[3]:
        rtn = 'Fire'
    elif r[2]:
        rtn = 'Flood'
    elif r[5]:
        rtn = 'Severe Storm'
    elif r[8]:
        rtn = 'Coastal Storm'
    elif r[7]:
        rtn = 'Typhoon'
    else:
        rtn = None
    return r[0], rtn

prioritized = filtered\
    .drop('state', 'state_right')\
    .map_rows(prioritize)\
    .drop_nulls()\
    .select(
        pl.col('column_0').cast(pl.Utf8).str.rjust(5,'0').alias('fips'),
        pl.col('column_1').alias('disaster')
    )

# %%
prioritizedUnfiltered = labeledCounties\
    .drop('state', 'state_right')\
    .map_rows(prioritize)\
    .drop_nulls()\
    .select(
        pl.col('column_0').cast(pl.Utf8).str.rjust(5,'0').alias('fips'),
        pl.col('column_1').alias('disaster')
    )

# %%
# Get the shapes of all the counties in a geoJSON file
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    countyShapes = json.load(response)

# %%
# A graph of what disaster each county is most worried about
fig = px.choropleth(prioritized,
    geojson=countyShapes, locations='fips',
    color='disaster',
    color_discrete_sequence=px.colors.qualitative.G10,
    color_discrete_map={
            "Tornado": '#550000',
            "Hurricane": '#65d6ff',
            "Earthquake": '#aa6511',
            "Flood": '#0835ff',
            "Severe Storm": '#00c106',
            "Coastal Storm": '#426a8d',
            "Fire": '#e60004',
            "Typhoon": '#a91fc1',
    },
    scope="usa",
    title='A Map of What kind of disaster each county is most worried about'.title(),
)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig.show()

# %%
# A graph of what each county is most worried about, if they're paranoid
fig = px.choropleth(prioritizedUnfiltered,
    geojson=countyShapes, locations='fips',
    color='disaster',
    color_discrete_sequence=px.colors.qualitative.G10,
    color_discrete_map={
            "Tornado": '#550000',
            "Hurricane": '#65d6ff',
            "Earthquake": '#aa6511',
            "Flood": '#0835ff',
            "Severe Storm": '#00c106',
            "Coastal Storm": '#426a8d',
            "Fire": '#e60004',
            "Typhoon": '#a91fc1',
    },
    scope="usa",
    title='A Map of What kind of disaster each county is most worried about, if they\'re paranoid'.title(),
)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig.show()

# %%
# A graph of just where tornadoes are a problem, cause it's kind interesting
justHurricanes = longFiltered.filter(pl.col('disaster') == 'Tornado')
fig = px.choropleth(justHurricanes, geojson=countyShapes, locations='fips',
    color='disaster',
    color_discrete_sequence=px.colors.qualitative.G10,
    scope="usa",
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
