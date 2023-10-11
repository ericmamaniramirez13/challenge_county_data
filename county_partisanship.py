# %%
import polars as pl
import pyarrow.parquet as pq
import pandas as pd
import numpy as np

# %%
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://raw.githubusercontent.com/AddisonJPratt/county_data/main/pres_elections_county.csv"
df = pd.read_csv(url)
# %%
df['fips'] = df['fips'].astype('Int64')

# Group by 'state' and 'election_year' and aggregate the sum of democratic and republican raw votes
county_wins = (
    df.groupby(['state', 'election_year'])
    .agg(
        democratic_raw_votes=pd.NamedAgg(column='democratic_raw_votes', aggfunc='sum'),
        republican_raw_votes=pd.NamedAgg(column='republican_raw_votes', aggfunc='sum')
    )
    .reset_index()
)


# Determine the winning party
conditions = [
    (county_wins['democratic_raw_votes'] > county_wins['republican_raw_votes']),
    (county_wins['republican_raw_votes'] > county_wins['democratic_raw_votes'])
]
choices = ['Dem', 'Rep']

county_wins['county_party_win'] = np.select(conditions, choices, default='Tie')

# Merge the county_party_win column back to the original dataframe
df_with_win = pd.merge(
    df, 
    county_wins[['state', 'election_year', 'county_party_win']], 
    on=['state', 'election_year'], 
    how='left'
)
# %%
# Creating a pivot table
df_pres = df_with_win.pivot_table(
    index=['fips', 'county_name', 'state'],
    columns='election_year',
    values='county_party_win',
    aggfunc='first'
)

df_pres.columns.name = None  # Remove the name of the columns level
df_pres = df_pres.reset_index()  # Reset the index to have 'fips', 'county_name', and 'state' as columns


# %%

export_df = pl.from_pandas(df_pres)
lslice = 500
values = list(range(0, export_df.shape[0], lslice))

previous = 0
for i in values:
    print(str(i))
    export_df.slice(i, lslice).write_parquet("county_partisanship/county_partisanship" + str(i) +".parquet")
    


# %%
# read in.
df = pl.read_parquet("county_partisanship/*")
df.shape

# %%
