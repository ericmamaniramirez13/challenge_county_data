# %%
# https://www.usreligioncensus.org/node/1639
import requests
import tempfile
import polars as pl
import pandas as pd

url = "https://www.usreligioncensus.org/sites/default/files/2023-06/2020_USRC_Group_Detail.xlsx"
response = requests.get(url)

with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
    temp_file.write(response.content)
    temp_file_path = temp_file.name


# %%
# blank line and totals on the last two lines
rel = pl.from_pandas(pd.read_excel(temp_file_path, sheet_name = "2020 Group by County")).slice(0, -2)
# %%
people = rel.select("FIPS", "State Name", "County Name", "Group Code", "Group Name", "Adherents")
congregations = rel.select("FIPS", "State Name", "County Name", "Group Code", "Group Name", "Adherents")
# %%
keep_churches = people.group_by("Group Name").count().sort("count", descending=True).slice(0, 12).select("Group Name").to_series().to_list()

top13 = people.filter(pl.col("Group Name").is_in(keep_churches))\
    .with_columns(
        pl.col("FIPS").str.slice(0, 2).alias("STATEFP"),
        pl.col("FIPS").str.slice(2).alias("COUNTYFP"))\
    .pivot(values="Adherents",
           index = ["FIPS","STATEFP", "COUNTYFP", "State Name", "County Name"],
           columns="Group Name",
           aggregate_function="first")\
    .fill_null(0)

# %%
lslice = 500
values = list(range(0, top13.shape[0], lslice))

previous = 0
for i in values:
    print(str(i))
    top13.slice(i, lslice).write_parquet("religion_census/religion_" + str(i) +".parquet")
    
# %%
