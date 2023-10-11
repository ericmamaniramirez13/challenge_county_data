# Crime

This folder contains the crime dataset for the temple estimation project.

##### Source: https://www.kaggle.com/datasets/mikejohnsonjr/united-states-crime-rates-by-county/

## Data Dictionary

| Column Name | Description | Importance |
| --- | --- | --- |
| fips | Federal Information Processing ID for counties. Must have the same number of rows as `county_meta` data (3146 total). | Key Column |
| crime_rate_per_100000 | The crime rate per 100,000 people in a county | float |
| MURDER | The total number of murder charges | int64 |
| RAPE | The total number of rape charges | int64 |
| ROBBERY | The total number of robbery charges  | int64 |
| AGASSLT | The total number of assault charges | int64 |
| BURGLRY | The total number of burglaries | int64 |
| LARCENY | The total number of Larceny charges | int64 |
| MVTHEFT | The total number of motor vehicle thefts | int64 |
| ARSON | The total number of Arson charges | int64 |
| population | The population of the county | int64 |

* No state, county name columns. The `county_meta` dataset already has them.
* There is a miscelaneous row with -1 fips. We added to make it the same number of row as `county_meta` (3146).
