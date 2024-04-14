# %%
from urllib.request import urlopen
import json
import plotly.express as px
import polars as pl
import pyarrow.parquet as pq
# %%
data = pl.read_csv("education_vs_per_capita_personal_income.csv")
    #.filter(pl.col("state") != "NA").drop("state")
# %%
print(data.null_count())
#No null values

print(data.columns)
# %%
data = data.rename({"county_FIPS" : "fips", "per_capita_personal_income_2019": "pcp_income_2019", "per_capita_personal_income_2020": "pcp_income_2020", "per_capita_personal_income_2021": "pcp_income_2021", "associate_degree_numbers_2016_2020": "as_degree_2016_2020", "bachelor_degree_numbers_2016_2020": "bs_degree_2016-2020", "associate_degree_percentage_2016_2020": "as_degree_percent_2016_2020", "bachelor_degree_percentage_2015_2019": "bs_degree_percent_2015_2019"})
print(data.columns)
# %%
data.select(['fips', 'state', 'county', 'pcp_income_2019', 'pcp_income_2020', 'pcp_income_2021', 'as_degree_2016_2020', 'bs_degree_2016-2020', 'as_degree_percent_2016_2020', 'bs_degree_percent_2015_2019'])
data
# %%
print(len(data))

data.shape
# %%
lslice = 700
values = list(range(0, data.shape[0], lslice))

previous = 0
for i in values:
    print(str(i))
    data.slice(i, lslice).write_parquet("education_vs_income/education_vs_income" + str(i) +".parquet")

df = pl.read_parquet("education_vs_income/education_vs_income0.parquet")
df.shape
# %%
print(data["bs_degree_percent_2015_2019"].max(), data["bs_degree_percent_2015_2019"].min())
# %%
data = data.filter(pl.col("pcp_income_2021") < 300_000)

data_agg = (
    data.lazy()
    .group_by("state")
    .agg(
        pl.col("county").count(),
        pl.col("pcp_income_2021").mean(),
        pl.col("bs_degree_percent_2015_2019").mean(),
    )
    .sort("bs_degree_percent_2015_2019", descending=True)
    #.limit(7)
)
data_agg=data_agg.collect()
print(data_agg)

# %%
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    countyShapes = json.load(response)
fig = px.choropleth(data, geojson=countyShapes, locations='fips',
    color='bs_degree_percent_2015_2019',
    range_color=(0, 76),
    color_discrete_sequence=px.colors.qualitative.G10,
    scope="usa",
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
fig.write_image("images/education_vs_income_1.png")
# %%
#More education = more income per county

fig = px.scatter(data, x="bs_degree_percent_2015_2019", y="pcp_income_2021", color="bs_degree_percent_2015_2019")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
fig.write_image("images/education_vs_income_2.png")
# %%
#More education = more income per state
fig = px.scatter(data_agg,
                 x="bs_degree_percent_2015_2019",
                 y="pcp_income_2021",
                )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

