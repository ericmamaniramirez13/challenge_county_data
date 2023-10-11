# %%
import polars as pl
import pyarrow.parquet as pq
# %%
county = pl.read_csv("https://github.com/kjhealy/fips-codes/raw/master/state_and_county_fips_master.csv")\
    .filter(pl.col("state") != "NA").drop("state")
other = pl.read_csv("https://github.com/kjhealy/fips-codes/raw/master/county_fips_master.csv",
        use_pyarrow=True)\
    .select("fips", "state_name", "region", "division", "state", "crosswalk", "region_name", "division_name")
# %%

dat = other.join(county, on=["fips"], how="left").select("fips", "name", "state_name", "region_name", "division_name", "state", "region", "division")
# %%
# dat.shape
# (3146, 8) shape

lslice = 500
values = list(range(0, dat.shape[0], lslice))

previous = 0
for i in values:
    print(str(i))
    dat.slice(i, lslice).write_parquet("county_meta/meta_" + str(i) +".parquet")
    


# %%
# read in.
df = pl.read_parquet("county_meta/*")
df.shape
# df
# fips	name	state_name	region_name	division_name	state	region	division
# i64	str	str	str	str	i64	i64	i64
# 1001	"Autauga County…	"Alabama"	"South"	"East South Cen…	1	3	6
# 1003	"Baldwin County…	"Alabama"	"South"	"East South Cen…	1	3	6
# 1005	"Barbour County…	"Alabama"	"South"	"East South Cen…	1	3	6
# 1007	"Bibb County"	"Alabama"	"South"	"East South Cen…	1	3	6