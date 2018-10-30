# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run](README.md#run)

# Problem

The challenge is to design a mechanism to analyze H1B(H-1B, H-1B1, E-3) visa application data published by [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). The raw data is pre-processed and converted to semicolon separated text files. This code should use the pre-processed data files to calculate **Top 10 Occupations** and **Top 10 States** for **certified** visa applications and export results to text files. 

The problem can be broken down to smaller tasks:
1. Handle data file
    1. Read in dataset
    2. Parse data and store values of interest
    3. Write result to text file
2. Find top K frequent element
    1. Sort data by multiple attributes
    2. Return top K records

The following requirements should be met:
1. Modular and Reusable
2. Robust
3. Scalable
4. Readable
5. Use default data structures and standard libraries

# Approach

To make the code reusable, I decomposed the project into smaller modules and created a library with functions and class to realize desired functionality.

There are two source code files:
1. **`base.py`**: A library to support the H1B statistics project. It defines a class `ApplicationData` with methods and a function `get_filepath` as described below:

    1. ***Class* `ApplicationData`**: Represent visa application data. 

        From problem description, this code should be able to process data files with file structure similar to that of H1B visa application data. The code should be able to process the raw data file and calculate statistics of metrics given conditions. In order to do these, the `ApplicationData` class has following methods:
        
        1. Handle data file
            1. ***Function* `readInput`**: Read in input data, parse data, and store relevant fields.
                - **Read in dataset**. Python has two default libraries that can read CSV: `I/O` and `csv`. While `I/O` is slightly faster than `csv` according to this [post](https://codereview.stackexchange.com/questions/79449/need-fast-csv-parser-for-python-to-parse-80gb-csv-file), `csv` provides a more robust way to work with CSV data. 
                - **Parse data**. For the sake of efficiency and memory, data is parsed while iterate over `csv.reader` object during the read-in process. `Dictionary` is used to record frequencies of elements. If an entry matches condition, i.e. case status is `CERTIFIED`, then add 1 to elements' corresponding counters stored in the dictionary; if an entry does not match condition, then skip this row and continue the iteration.
            2. ***Function* `writeOutput`**: Write result to output as txt using Python's default `I/O` library. 
            
        2. Find Top K Frequent Element
            1. ***Function* `heapSortLargest`**: Python provides `heapq` module as an implementation of the heap queue algorithm. The time complexity of heap sort is `O(nlogn)`, space complexity is `O(1)`. Finding top K elements is realized through `heapq.nsmallest` function. `heapq.nsmallest` function is used with multiple keys to first sort by frequency and then by name when there is a tie, and return top K elements. 
            2. ***Function* `topK`**: Iterate through records, for each metric, call `heapSortLargest` to get top K elements and call `writeOutput` to export result to desired destination. This function allows user to specify different K values for different metrics. 

    2. *Function* `get_filepath`: Construct and return file path.

        This function is created to construct file path given file type and file name. File type can be `src` for source files, `input` for input files, and `output` for output files. 

2. **`h1b_counting.py`**: Users can specify parameters, create `ApplicationData` objects, and call its function to find top K elements. Specifically, users can specify:
    - `K`: how many top elements to return.
    - `FIELDS`: metrics of interest and corresponding possible field names in raw file. In this challenge, we are interested in two metrics: `occupations` and `states`. `occupations` values are under column name **SOC_NAME** in Year 2015 to 2018, and under column name **LCA_CASE_SOC_NAME** in Year 2014. 'states' values are under column name **WORKSITE_STATE** in Year 2015 to 2018, and under column name **LCA_CASE_WORKLOC1_STATE** in Year 2014.
    - `CONDITIONS`: conditions to count values and corresponding possible field names. In this challenge, there is only one condition to be met: case status is `CERTIFIED`. Case status values are under column name **CASE_STATUS** in Year 2015 to 2018, and under column name **STATUS** in Year 2014.
    - `INPUT_FILE`: input filename.
    - `OUTPUT_FILE`: generic output filename.

# Run
With input file `h1b_input.csv` put in the `input` directory, there are two ways to run the code:

1. Run the `run.sh` script in the `h1b_statistics-master` folder, or
2. Run the `h1b_counting.py` script in the `src` folder.

The script will produce in the `output` folder the following semicolon seperated files:
1. `top_10_occupations.txt`: Top 10 occupations for certified visa applications with 3 columns:
    1. __`TOP_OCCUPATIONS`__: The occupation name associated with an application's Standard Occupational Classification (SOC) code. 
    2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. 
    3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation, rounded off to 1 decimal place
2. `top_10_states.txt`: Top 10 states for certified visa applications with 3 columns:
    1. __`TOP_STATES`__: State where the work will take place.
    2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for work in that state. 
    3. __`PERCENTAGE`__: % of applications that have been certified in that state compared to total number of certified applications regardless of state, rounded off to 1 decimal place.

Code is tested on 6 cases and all passed.
