## Variable Definitions

### This dataset represents unemployment and median household income for the US from 2000 to 2022

- **FIPS_Code:** The Federal Information Prcessing ([FIPS](https://www.nist.gov/standardsgov/compliance-faqs-federal-information-processing-standards-fips)) ID for each county.

- **2000-2022** The data ranges from the years 2000 to 2022. Every year has these columns below with specifics to which year it was

* Civilian_labor_force - Civilian labor force annual average
* Employed - Number employed annual average
* Unemployed - Number unemployed annual average
* Unemployment_rate - Unemployment rate

## Missingness

The only missing values in this dataset are for Puerto Rico of which those missing values will not affect us because we are dealing only with The United States.


## Data Snippet

| FIPS_Code |  Civilian_labor_force_2000 | Employed_2000  | Unemployed_2000  | Unemployment_rate_2000  | Civilian_labor_force_2001  | Employed_2001  | Unemployed_2001  |  Unemployment_rate_2001 |
| ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| i64  | str   | str   | str   | str   | str   | str   | str   | str   | 
| 1001 | "21,861" | "20,971" | "890" | "004.1" | "22,081" | "21,166" | "915" | "004.1" |
| 1003| "69,979" | "67,370" | "2,609" | "003.7" | "69,569" | "66,545" |	"3,024" |"004.3" |
| 1003| "11,449" | "10,812" | "637"	| "005.6" |	"11,324" | "10,468" | "856" | "007.6" |
| 1005| "8,623" | "8,160" | "463" |	"005.4" | "9,134" |	"8,513" | "621" | "006.8" |
| 1007| "25,266" | "24,375"	| "891"	| "003.5" | "25,450" | "24,521" | "929"	| "003.7" |	
| 1009| "3,997" |"3,656" | "341" | "008.5" | "3,937" | "3,543" | "394" | "010.0" |
| 1011| "9,221" | "8,496" | "725" | "007.9" | "9,060" | "8,372" | "688" | "007.6" |

ß