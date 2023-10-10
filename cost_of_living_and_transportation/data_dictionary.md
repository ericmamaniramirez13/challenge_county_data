# Data Dictionary

## Cost of Living Dataset

| Column Name | Description |
|-----|------|
| rent | Average monthly cost of rent |
| food | Average monthly cost of food |
| child_care | Average monthly cost of child_care |
| transportation | Average monthly cost of transportation |
| health_care | Average monthly cost of health_care |
| other | Average monthly cost of other expenses |
| taxes | Average monthly taxes |
| total | Average monthly total cost of living |
| total_annual | Average annual total cost of living |
| state_cost_rank | Rank for each state based on cost of living |

## Transportation Dataset
> Dataset Completed: 12/3/2019
<br><br>
This City and County Energy Profiles data lookup table provides modeled electricity and natural gas consumption and expenditures, on-road vehicle fuel consumption, and vehicle miles traveled for each U.S. city and county. Please note this data is modeled and more precise data may be available from regional, state, or other sources. The modeling approach for electricity and natural gas is described in Sector-Specific Methodologies for Subnational Energy Modeling: https://www.nrel.gov/docs/fy19osti/72748.pdf. For feedback or questions please contact: slope@nrel.gov.

| Column Name | Units | Description | Source (if applicable) |
|-----|------|---|---|
 | county_center_lat | | Latitude component of centroid coordinates or geometric center of the county | U.S. Census 2016 Gazetteer Files |
 | county_center_long | | Longitude component of centroid coordinates or geometric center of the county | [''](https://en.wikipedia.org/wiki/Ditto_mark) |
 | total_population | | County population count | U.S. Census 2012-2016 5-yr American Community Survey |
 | total_employment | | County-only employment count | U.S. Census 2016 County Business Patterns |
 | utility_customers | | Estimated electric utility or natural gas customers | NREL GIS mapping based on Ventyx/ABB Data and 2016 Energy Information Administration Survey Form 861 |
 | electric_consumption | MWH | Estimated total consumption of electricity by residential buildings | Ma, Ookie, Ricardo Oliveira, Evan Rosenlieb, and Megan Day. 2019. Sector-Specific Methodologies for Subnational Energy Modeling. Golden, CO: National Renewable Energy Laboratory. NREL/TP-7A40-72748. https://www.nrel.gov/docs/fy19osti/72748.pdf. |
 | electric_expenditure | '000 $ | Estimated total expenditure of electricity by residential buildings | '' |
 | electric_consumption_capita | MWH | Estimated per capita consumption of electricity by residential buildings | '' |
 | electric_expenditure_capita | '000 $ | Estimated per capita expenditure of electricity by residential buildings | '' |
 | gas_consumption | gallons | Modeled gasoline consumption by on-road vehicles within the county | '' |
 | gas_consumption_capita | gallons | Modeled gasoline consumption per capita by on-road vehicles within the county | '' |
 | diesel_consumption | gallons | Modeled diesel consumption by on-road vehicles within the selected county | '' |
 | diesel_consumption_capita | gallons | Modeled diesel consumption per capita by on-road vehicles within the county | '' |
 | county_vehicle_miles | miles | Estimated total vehicle miles for all on-road travel within the county | See methodology posted at: www.eere.energy.gov/sled under transportation. |
 | county_vehicle_miles_capita | miles | Estimated vehicle miles per capita for all on-road travel within the county | '' |
