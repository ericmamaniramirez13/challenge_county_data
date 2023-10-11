# %%
import polars as pl
# %%
# ENERGY DATA
# Energy data was found [here](https://data.openei.org/files/149/2016cityandcountyenergyprofiles.xlsb) and shaped manually in Excel before exporting to the dataset below.
nrg = pl.read_parquet("https://github.com/JustinMorley/apt103_county_data/raw/source-branch/cost_of_living_and_transportation/source/energy.parquet")
nrg.head()
# %%
# COST OF LIVING
# https://raw.githubusercontent.com/williamrichards001/Data-science/main/cost%20of%20living%20again.csv
# The above CSV was just converted to the Parquet below with no additional changes.
living_cost = pl.read_parquet("https://github.com/JustinMorley/apt103_county_data/raw/source-branch/cost_of_living_and_transportation/source/cost-of-living.parquet")
living_cost.head()
# %% 
# Join Datasets on FIPS
nrg = nrg.rename({"FIPS":"fips"})
dat = nrg.join(living_cost, on=["fips"], how="left")
dat.shape
# %% 
# Write Dataset to Parquet
lslice = 700
values = list(range(0, dat.shape[0], lslice))

previous = 0
for i in values:
    print(str(i))
    dat.slice(i, lslice).write_parquet("./cost_of_living_and_transportation_" + str(i) +".parquet")