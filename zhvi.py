import polars as pl
import pyarrow.parquet as pq
import requests 
from io import StringIO

def download_csv_to_dataframe(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = StringIO(response.text)
        return pl.read_csv(data)
    else:
        print(f"Failed to download data from {url}. Status code: {response.status_code}")
        return None

url_zhvi = "https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
url_fips = "https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_and_county_fips_master.csv"
# url_fips_other = "https://raw.githubusercontent.com/kjhealy/fips-codes/master/county_fips_master.csv"

df_zhvi = download_csv_to_dataframe(url_zhvi)
df_fips = download_csv_to_dataframe(url_fips)
# df_fips_other = download_csv_to_dataframe(url_fips_other)

print(f"Zillow Data: {df_zhvi.shape}")
print(f"FIPS: {df_fips.shape}")

# create a FIPS column in the Zillow Data  
# join on the FIPS df to create the necessary amount of rows

df_zhvi = (
    df_zhvi
    .with_columns([
        df_zhvi['StateCodeFIPS'].cast(pl.datatypes.Utf8).alias('StateCodeFIPS_str'),
        df_zhvi['MunicipalCodeFIPS'].cast(pl.datatypes.Utf8).str.zfill(3).alias('MunicipalCodeFIPS_str')
    ])

    .with_columns((pl.col('StateCodeFIPS_str') + pl.col('MunicipalCodeFIPS_str')).alias('CombinedFIPS'))
)

df_zhvi.select(['StateCodeFIPS', 'MunicipalCodeFIPS', 'CombinedFIPS']).head()

# drop the StateCodeFIPS and MunicipalCodeFIPS - now that they're combined we don't need them
df_zhvi = df_zhvi.drop(['StateCodeFIPS', 'MunicipalCodeFIPS', 'StateCodeFIPS_str', 'MunicipalCodeFIPS_str', 'RegionName', 'RegionType', 'StateName', 'State'])

# convert the combined FIPS to int
df_zhvi = df_zhvi.with_columns(df_zhvi['CombinedFIPS'].cast(pl.datatypes.Int64).alias('CombinedFIPS'))

# move the combined column to the front
df_zhvi = df_zhvi.select(['CombinedFIPS'] + [col for col in df_zhvi.columns if col != 'CombinedFIPS'])

df_zhvi.head()


zhvi = df_fips.join(df_zhvi, left_on="fips", right_on="CombinedFIPS", how="left")
mask = zhvi["name"].str.to_uppercase() != zhvi["name"]
zhvi = zhvi.filter(mask)
zhvi = zhvi.drop(["state", "RegionID", "name"])
zhvi.head()
# zhvi.write_csv("output_zhvi.csv")
print(zhvi.shape)

lslice = 500
values = list(range(0, zhvi.shape[0], lslice))
import os
if not os.path.exists("zhvi_slices"):
    os.makedirs("zhvi_slices")
previous = 0
for i in values:
    print(str(i))
    zhvi.slice(i, lslice).write_parquet("zhvi_slices/zhvi_" + str(i) +".parquet")
# To read them back in:
# df_zhvi = pl.read_parquet("zhvi_slices/*")
# df_zhvi.shape