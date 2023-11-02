# %%
import polars as pl
import urllib.request
from urllib.request import urlopen
import json
import plotly.express as px
import plotly
import os

# %%
# This is much better than what I was doing. This actually has the right amount of states
counties = pl.read_csv("https://github.com/kjhealy/fips-codes/raw/master/state_and_county_fips_master.csv")\
    .filter(pl.col("state") != "NA").drop('name')

# %%
# Just so I don't have to keep downloading it as I tweak things
if os.path.exists('~/Documents/Class/DS460/DisasterDeclarationsSummaries.csv'):
    _disasters = pl.read_csv('~/Documents/Class/DS460/DisasterDeclarationsSummaries.csv')
else:
    _disasters = pl.read_csv('https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv')

# %%
# Get relevant disaster data
# Data dictionary
# https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2

# Based on the link, and looking at data for hurricane katrina, it seems like the counties
# where these programs were declared determines whether it was actually a serious disaster,
# or if it just kinda passed through there technically. (i.e. apparently katrina technically hit ID)
disasters = _disasters\
    .filter(pl.col('ihProgramDeclared').cast(pl.Boolean) | pl.col('iaProgramDeclared').cast(pl.Boolean))\
    .select(
        'incidentType',
        # I WOULD do .round(-1), but SOMEONE doesn't support integer rounding
        pl.col('incidentBeginDate').str.to_datetime().dt.year()\
            .cut(list(range(1950, 2040, 10)),
                labels=list(map(lambda i: f"{i}s", range(1940, 2040, 10))))\
            .alias('decade'),
        # 'state',
        ( # This combines the state and county codes propery (ssccc, with padding 0's in county)
            pl.col('fipsStateCode').cast(str) + \
            pl.col('fipsCountyCode').cast(str).str.rjust(3, '0')
        ).cast(pl.Int64).alias('fips'),
    )\
    .filter(pl.col('decade') != "1950s") # The only things in the 50's are some floods. Not hugely relevant.

# %%
# Pivot the disaster data the way we want it
disastersWeCareAbout = [
    'Hurricane',
    'Flood',
    'Tornado',
    'Severe Storm',
    'Fire',
    'Earthquake',
    'Winter Storm',
    # 'Typhoon', Looks like there's been like, 1 typhoon. Not real concerning.
    'Coastal Storm',
]
# Note: These are seperated because we use just longWideDisasters later for graphing
longWideDisasters = disasters.pivot(
        values='incidentType',
        index=('fips', 'decade'),
        columns='incidentType',
        aggregate_function='count',
    ).select('fips', 'decade', *disastersWeCareAbout)\
    .fill_null(0)

wideDisasters = longWideDisasters.pivot(
        values=disastersWeCareAbout,
        index='fips',
        columns='decade',
    ).fill_null(0)

    # .drop('Biological', 'Other', 'Snowstorm', 'Dam/Levee Break', 'Freezing', 'Toxic Substances',
    #       'Drought', 'Human Cause', 'Fishing Losses', 'Chemical', 'Terrorist', 'Volcanic Eruption',
    #       'Severe Ice Storm', 'Mud/Landslide'
    #     )\

    # These don't feel particularly relevant /|\
    # After looking at the data, it looks like for Volcanic Eruption, there's Hawaii (obviously),
    # and a few in Washington, which I realized must be Mt. St. Helen's. I'm removing it because
    # It seems like they know how to deal with them in Hawaii, and Mt. St. Helen's isn't gonna blow
    # again anytime soon


# %%
# Add the disasters to the data
labeledCounties = counties.join(wideDisasters, 'fips', how='inner').drop('state')

# %%
# Remove any columns that don't have any in them -- not actually useful anymore
# drop = []
# for c in labeledCounties.columns:
#     if labeledCounties[c].dtype == pl.UInt32:
#         if not labeledCounties[c].cast(pl.Boolean).any():
#             drop.append(c)
# labeledCounties = labeledCounties.drop(drop)


# %%
# We don't actually care about doing this anymore. It's not relevant, especially after
# splitting up into decades
if False:
    # If you have occational fires/floods/storms in the county, that's not indicative
    # of a larger problem. We want to know if it's at significant risk
    # This data does go all the way back to 1964 after all
    filtered = labeledCounties.with_columns(
        # The thresholds I got from looking at the .describe() stats
        # I'm justifying this because after making a grpah, it's not nearly as widespread
        # as i assumed. I think they're only counting wildfires after all
        (pl.col('Fire') > 0).alias('Fire'),
        (pl.col('Flood') > 2).alias('Flood'),
        (pl.col('Severe Storm') > 0).alias('Severe Storm'),
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
# labeledCounties.write_parquet('disasters/disasters.parquet', use_pyarrow=True)

# The size each will be
size = len(labeledCounties) // 5
# Split them all up into a list of smaller datasets
split = [labeledCounties[size*i:size*(i+1)] for i in range(4)]
# Becuase we're doing // instead of /, we might have an off-by-one error.
# This fixes that.
split.append(labeledCounties[size*4:])
assert sum(map(len, split)) == len(labeledCounties), "You split the dataset wrong"

# NOW actually write the data
for cnt, data in enumerate(split):
    data.write_parquet(f'disasters/disasters_{cnt}.parquet', use_pyarrow=True)

# %%
# Just some quick code to make a long formatted version
longVersion = labeledCounties.drop('state', 'state_right').melt('fips', variable_name='disaster')\
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
# def generateDecadeGraphData(decade):
    # decadeData = longWideDisasters.filter(pl.col('decade') == decade)
_priority = [
    'Hurricane',
    'Tornado',
    'Earthquake',
    'Fire',
    'Flood',
    'Severe Storm',
    'Coastal Storm',
]
# NO idea why this is necissary. All of the sudden it started giving me a runtime error
cols = longWideDisasters.columns
def prioritize(r):
    for p in _priority:
        if r[cols.index(p)]:
            return r[0], r[1], p
    return r[0], r[1], None

prioritized = longWideDisasters\
    .map_rows(prioritize)\
    .drop_nulls()\
    .select(
        pl.col('column_0').cast(pl.Utf8).str.rjust(5,'0').alias('fips'),
        pl.col('column_1').alias('decade'),
        pl.col('column_2').alias('disaster')
    )

# graphData = [generateDecadeGraphData(decade) for decade in list(longWideDisasters['decade'].unique())]


# %%
# Get the shapes of all the counties in a geoJSON file
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    countyShapes = json.load(response)

# %%
# A graph of what disaster each county is most worried about
fig = px.choropleth(prioritized,
    geojson=countyShapes, locations='fips',
    color='disaster', facet_col='decade', facet_col_wrap=4,
    # color_discrete_sequence=px.colors.qualitative.G10,
    color_discrete_map={
            "Tornado": '#550000',
            "Hurricane": '#65d6ff',
            "Earthquake": '#aa6511',
            "Flood": '#0835ff',
            "Severe Storm": '#00c106',
            "Coastal Storm": '#426a8d',
            "Fire": '#e60004',
            # "Typhoon": '#a91fc1',
    },
    scope="usa",
    title=f'What Counties had Which Disasters in What Decade',
)
fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    # autosize=False,
    # width=2000,
    # height=1500,
    legend_tracegroupgap=0,
    legend_traceorder='grouped',
)
pass

# %%
# img = plotly.io.to_html(fig)
img = plotly.io.to_image(fig, format='png')


# %%
with open('images/disastersOverDecades.png', 'wb') as f:
    f.write(img)

# %%
# A graph of just where tornadoes are a problem, cause it's kind interesting
justHurricanes = longVersion.filter(pl.col('disaster') == 'Tornado')
fig = px.choropleth(justHurricanes, geojson=countyShapes, locations='fips',
    color='disaster',
    color_discrete_sequence=px.colors.qualitative.G10,
    scope="usa",
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
