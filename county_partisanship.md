## Variable Definitions

### This dataset represents the partisanship of each county during presidential elections spanning the years 1868 through 2020.

- **fips:** The Federal Information Prcessing ([FIPS](https://www.nist.gov/standardsgov/compliance-faqs-federal-information-processing-standards-fips)) ID for each county.
- **1868-2020** The data ranges from the years 1868 to 2020. Every year has the value "Dem" or "Rep".
  This represents what partisanship the county was in that specific year based on which party had more votes.

* Please note - The value means which party each county swinged more towards to, not necessarily everyone in the county voted 'Dem' or 'Rep'

  The values were calculated as follows:

```
'democratic_raw_votes' > 'republican_raw_votes' = 'Dem'
'republican_raw_votes' > 'democratic_raw_votes' = 'Rep'
```

## Missingness

For each year there are some counties that do not have their voting information recorded, therefore I was not able to make a calculation for whether or not they were a more leaning Dem or Rep.

- As the years go on, there are less missing values.
  ex: The year 1868 had **1488** while years progressively have less null values concluding with the year 2020 had **98** missing values.

## Data Snippet

| fips | 1868  | 1872  | 1876  | 1880  | 1884  | 1888  | 1892  | 1896  | 1900  | 1904  |
| ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| i64  | str   | str   | str   | str   | str   | str   | str   | str   | str   | str   |
| 1001 | "Rep" | "Rep" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" |
| 1003 | "Rep" | "Rep" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" |
| 1005 | "Rep" | "Rep" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" |
| 1007 | "Rep" | "Rep" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" |
| 1009 | "Rep" | "Rep" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" | "Dem" |
