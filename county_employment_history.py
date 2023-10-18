# %%
import polars as pl
import pyarrow.parquet as pq
import pandas as pd
import urllib.request

# %%
url = "https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.csv?v=6139.9"
file_path = "Unemployment.csv"
urllib.request.urlretrieve(url, file_path)

# Read the downloaded Excel file using Polars
us_counties = pl.read_csv(file_path)
# %%

us_counties  = us_counties\
.pivot(
    index = ["FIPS_Code", "State", "Area_Name"],
    values = "Value",
    columns = "Attribute",
    aggregate_function= "first"
)

# %%
us_counties
# %%
condition = (pl.col("Area_Name").str.contains("Municipio") | pl.col("Area_Name").str.contains("County")\
            |pl.col("Area_Name").str.contains("Parish")\
            |pl.col("Area_Name").str.contains("Census")\
            |pl.col("Area_Name").str.contains("Borough"))

# Apply the filter to the DataFrame
us_counties = us_counties.filter(condition)
# %%
columns_to_remove = ["State", "Area_Name", "Rural_Urban_Continuum_Code_2013","Urban_Influence_Code_2013", "Metro_2013", "Med_HH_Income_Percent_of_State_Total_2021" ] 
us_counties = us_counties.select([col for col in us_counties.columns if col not in columns_to_remove])
# %%
us_counties
# %%
lslice = 800
values = list(range(0, us_counties.shape[0], lslice))

previous = 0
for i in values:
    print(str(i))
    us_counties.slice(i, lslice).write_parquet("county_employment_history_meta/meta_" + str(i) +".parquet")
# %%
# read parquet file
df = pl.read_parquet("county_employment_history_meta/*")
# %%
df.shape
# %%
# display first 20 lines
df.head(20)
# %%
