# Data Discover and Ingestion Challenge

For this challenge, each team will identify, extract, and convert United States data at the county level to `.parquet` that supports our temple estimation project.

## Data 

Your discovered data must have a row for each county in the US with variables (columns) that your team feels would be of value to our project. You can use the county file provided in the repository as a guide.

## Format and Details

1. Fork this repository.
2. Evaluate the other groups' described data they are building and make sure your team is not duplicating effort.
3. Create a folder with a descriptive name of your data (E.g., `residential_permits`)
4. Create a data digestion script with the same name as your folder in the main section of the repository (E.g., `residential_permits.py`)
5. Write your `.parquet` files into your respective folder with at least five chunked files, and no file is larger than 10 MB.
6. Create a data dictionary in the main section of the repository (E.g., `residential_permits.md` that describes each column in your data set.
7. Work with your team to have one pull request that returns this data to the central repository.

## Discussion

Your data must have the county fips ID column. It should not have the state and county name columns. It should have the same number of rows as the `county_meta` data.

|  fips    | permits_2020 | permits_2010 |
| -------- | ------------ | ------------ |
|  1045    |     45       |    38        |
|  1046    |     81       |    120       |
|  1081    |     123      |    19        |

