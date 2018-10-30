# Data files and format
The script will produce in this `output` folder the following semicolon seperated files:
1. `top_10_occupations.txt`: Top 10 occupations for certified visa applications with 3 columns:
    1. __`TOP_OCCUPATIONS`__: The occupation name associated with an application's Standard Occupational Classification (SOC) code. 
    2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. 
    3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation, rounded off to 1 decimal place
2. `top_10_states.txt`: Top 10 states for certified visa applications with 3 columns:
    1. __`TOP_STATES`__: State where the work will take place.
    2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for work in that state. 
    3. __`PERCENTAGE`__: % of applications that have been certified in that state compared to total number of certified applications regardless of state, rounded off to 1 decimal place.