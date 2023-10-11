'''
Data digestion script
for the crime dataset
'''
#%%
# Load libraries
import pyspark.sql.functions as F
import requests

# create dir
dbutils.fs.mkdirs("dbfs:/data") 
dbutils.fs.mkdirs("dbfs:/data/crime") 

#%%
# Now we will download the data to our `data` folder
token = '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' 
owner = 'MarcelPratikto'
repo = 'challenge_county_data'
files_safegraph_census = ['crime0.parquet',
                          'crime1.parquet', 'crime2.parquet', 
                          'crime3.parquet', 'crime4.parquet']
paths_safegraph_census = ["crime/" + f for f in files_safegraph_census]
files = files_safegraph_census
paths = paths_safegraph_census

# send requests
for p in paths:
  folder_name = p.split("/")
  folder = folder_name[0]
  name = folder_name[1].replace(".parquet", "")
  r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
    owner=owner, repo=repo, path=p),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
            },
    stream = True
    )
  with open("temp.parquet", 'wb') as f:
    f.write(r.content)
  dbfs_path = "dbfs:/data/" + p
  dbutils.fs.cp("file:/databricks/driver/temp.parquet", dbfs_path)
  dbutils.fs.rm("file:/databricks/driver/temp.parquet")
  print(p)

#%%
spark.read.parquet("dbfs:/FileStore/crime0.parquet").write.mode("overwrite").saveAsTable("safegraph.crime_table")