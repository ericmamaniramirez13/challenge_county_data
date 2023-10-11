# zhvi (Zillow Zestimates data)

## Objective

To identify, extract, and convert United States data at the county level to `.parquet` that supports our temple estimation project.

## Data Background

From the [Zillow Website](https://www.zillow.com/research/methodology-neural-zhvi-32128/)

"The Zillow Home Value Index (ZHVI) is designed to capture the value of a typical property across the nation or the neighborhood, not just the homes that sold, and we do so by drawing information from the full distribution of homes in a given region. 

ZHVI measures monthly changes in property-level Zestimates, capturing both the level and appreciation of home values across a wide variety of geographies and housing types (e.g., all single-family homes in ZIP code 98101). This is how we focus on actual market price changes, and not changes in the kinds of markets or property types that sell from month to month."

This data can be used to see trends over time of general house prices per county.

## Missing Values

There are several months, especially in less populated counties, where a ZHVI score was not recorded. The closer you move towrds the present the more fields there are that have a ZHVI score. We have assigned these missing values as `nan`. There are a few counties that have no data, but are still represented in the data.

## Data Dictionary

* fips - i64 - fips code for the county

* SizeRank - i64 - size ranking to other counties by population (0 is the most populated county)

* Metro - str - Metro area (Major City) that this county is associated with

* *dates* - f64 - the ZHVI score for the county for this month in dollars (recorded at the end of the month so 2000-01-31 is for January, 2000)

## Data Table Snippet
|    |   fips |   SizeRank | Metro                     |   2000-01-31 |   2000-02-29 |   2000-03-31 |   2000-04-30 |
|---:|-------:|-----------:|:--------------------------|-------------:|-------------:|-------------:|-------------:|
|  0 |   1001 |        904 | Montgomery, AL            |       119113 |       119142 |       118947 |       118873 |
|  1 |   1003 |        302 | Daphne-Fairhope-Foley, AL |       133903 |       134113 |       134348 |       134816 |
|  2 |   1005 |       1635 | Eufaula, AL-GA            |          nan |          nan |          nan |          nan |
|  3 |   1007 |       1751 | Birmingham-Hoover, AL     |          nan |          nan |          nan |          nan |
|  4 |   1009 |        894 | Birmingham-Hoover, AL     |          nan |          nan |          nan |          nan |
