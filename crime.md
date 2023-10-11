# Crime

This folder contains the crime dataset for the temple estimation project.

##### Source: https://www.kaggle.com/datasets/mikejohnsonjr/united-states-crime-rates-by-county/

## Data Dictionary

| Column Name | Description | Importance |
| --- | --- | --- |
| fips | Federal Information Processing ID for counties. Must have the same number of rows as `county_meta` data (3146 total). | Key Column |
| crime_rate_per_100000 | description goes here | optional |
| EDITION | description goes here | optional |
| PART | description goes here | optional |
| IDNO | description goes here | optional |
| CPOPARST | description goes here | optional |
| CPOPCRIM | description goes here | optional |
| AG_ARRST | description goes here | optional |
| AG_OFF | description goes here | optional |
| COVIND | description goes here | optional |
| INDEX | description goes here | optional |
| MODINDX | description goes here | optional |
| MURDER | description goes here | optional |
| RAPE | description goes here | optional |
| ROBBERY | description goes here | optional |
| AGASSLT | description goes here | optional |
| BURGLRY | description goes here | optional |
| LARCENY | description goes here | optional |
| MVTHEFT | description goes here | optional |
| ARSON | description goes here | optional |
| population | description goes here | optional |

* No state, county name columns. The `county_meta` dataset already has them.
* There is a miscelaneous row with -1 fips. We added to make it the same number of row as `county_meta` (3146).