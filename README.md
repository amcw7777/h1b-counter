# H1B statistic analyzer
This project is developed with Python.
The purpose is to analyze H1B raw data from past years, calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications.

# Table of Contents
1. [Problem](README.md#problem)
    1. [Input]( README.md#input )
    2. [Output]( README.md#output )
    3. [Challenge]( README.md#challenge )
2. [Approach]( README.md#approach )
    1. [Data information]( README.md#data-information )
    2. [Data prerpocessing]( README.md#data-preprocessing )
    3. [Data analysis]( README.md#data-analysis )
    4. [Performance and trade-offs]( README.md#performance-and-trade-offs )
3. [Run instructions]( README.md#run-instructions)


# Problem
Design a program to analyze [raw immigration data](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf) to calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications. 
The program requires:
1. The code should be modular and reusable for future without needing to change the code;
2. The code can deal with special case like missing data or typos;
3. Only allowed to use the default data structures that come with that programming language.

## Input
The input data is a semicolon separated (";") format. The first row is field names. The description of the field names can be find [here](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_FY17_Record_Layout.pdf). **The fields name are different in different years.**

## Output
The program must create 2 output files:
* `top_10_occupations.txt`: Top 10 occupations for certified visa applications
* `top_10_states.txt`: Top 10 states for certified visa applications

Requirements:
1. Each line holds one record and each field on each line is separated by a semicolon (;).
2. The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__ (__`TOP_STATES`__).
3. There can be fewer than 10 lines in each file.
4. Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and 1.04% should be rounded to 1.0%. Also, 1% should be represented by 1.0%

## Challenges
1. Even the data is separated by semicolon, not all the semicolons are delimiter. (For example, `aaa;"bbb;ccc";;ddd` should be read as `'aaa', 'bbb;ccc', '', 'ddd'`;
2. Different field names in different years;
3. Missing data or typo: it is the hardest part in the problem. The work states information are all good. But there are missing or typos in occupation name and SOC code data.

# Approach
`preprocess.py`: process raw data, find correct fields, clean data. Write records with `'CERTIFIED'` status into processed data:
1. `STATE`: 'xx' format. Inferred from zip code if not valid;
2. `SOC_CODE`: 'xx-xxxx.xx' format.
3. `SOC_NAME`: clean as a string

`data_analyze.py`: analyze processed data:
1. Infer occupation name from `SOC_CODE` and `SOC_NAME`;
2. Use `state_counter` and `occupation_counter` hash tables to record frequency of states and occupations;
3. Sort based on counts and print out top 10 states and occupations.

## Data information
I summarized the field names which are need for this problem for different years.

| Year | Status      | State                   | Occupation name   | SOC code          |
|:----:|-------------|-------------------------|-------------------|-------------------|
| 2014 | STATUS      | LCA_CASE_WORKLOC1_STATE | LCA_CASE_SOC_NAME | LCA_CASE_SOC_CODE |
| 2015 | CASE_STATUS | WORKSITE_STATE          | SOC_NAME          | SOC_CODE          |
| 2016 | CASE_STATUS | WORKSITE_STATE          | SOC_NAME          | SOC_CODE          |

So I am using following criteria to select the correct fields
```
Status: 'STATUS' in name
State: 'WORK' in name and 'STATE' in name
Occupation name: 'SOC' in name and 'NAME' in name
SOC code: 'SOC' in name and 'CODE' in name
```
Since in 2014 data, there is another field name `LCA_CASE_WORKLOC2_STATE`, I only take the first time. 
The semicolon delimiter challenge can be solve using [a function](https://github.com/amcw7777/h1b-counter/blob/master/src/h1b_tools.py#L60-L81). Or using [regular expression](https://github.com/amcw7777/h1b-counter/blob/master/src/preprocess.py#L44).

## Data preprocessing 
### STATUS
Valid values include “Certified”, “Certified-Withdrawn”, “Denied”, and “Withdrawn". In the given data, most information are valid. In the 2014 data, one case with status as 'REJECTED' and another one as 'INVALIDATED'. These are the only two special cases for the three years data. In this problem, only cases with "Certified" status are counted. So the special cases will not affect the result.

### STATE
Two letters short for one of the states. In some cases, the name of the states are incorrect and the name cannot be found in a state dictionary. For these cases, [a function](https://github.com/amcw7777/h1b-counter/blob/master/src/preprocess.py#L112-L127) uses Zip code to correct the states. And check all the special cases manually. ** If the state name is accidentally input as another state, my program does not work. **

### 'VOTING' to correct OCCUPATION
The occupation name in raw data is not very clean. 
1. Missing occupation name;
2. Different format: the occupation name ending with '*' (means modified in SOC2000) or '"'. Or 'R&D' and 'R & D' and 'R and D' which present same name;
3. Typos: like 'ANALYST' -> 'ANALYSTS'; 'COMPUTER' -> 'COMPTUER';
4. Missing part of information: like 'COMPUTER OCCUPATIONS, ALL' -> 'COMPUTER OCCUPATIONS, ALL OTHER'

We can use SOC code to help correct occupation name, but SOC code also have problem:
1. Missing SOC code;
2. Different format: xx/xxxx.xx or xx-xxxx-xx or xxxxxxxx;
3. Typos: missing number of incorrect SOC code;
4. Same SOC code but different occupation name.

To solve format problem, I used two function [`clean_soc_code`](https://github.com/amcw7777/h1b-counter/blob/master/src/h1b_tools.py#L18-L39) to transfer all SOC code as format 'XX-XXXX.XX'. If the SOC code is 6 digit or ends with '.99', the function replace the end with '.00'. 

The [`clean_soc_name`](https://github.com/amcw7777/h1b-counter/blob/master/src/h1b_tools.py#L41-L59) function fix the occupation as all capital letter and remove extra space and quotas. 

The correct occupation name is the soc_name with **highest frequency** of one soc_code.
For example, in the table below, the correct name corresponding to '13-1161.00' should be 'MARKET RESEARCH ANALYSTS AND MARKETING SPECIALISTS'. Others are missing information or typos.

| SOC code   |  Occupation name                                   | Counting |
|------------|----------------------------------------------------|----------|
| 13-1161.00 | MARKET RESEARCH ANALYSTS AND MARKETING SPECIALISTS | 6978     |
|            | MARKET RESEARCH ANALYSTS AND MARKETING             | 167      |
|            | MARKET RESEARCH ANALYST AND MARKETING SPECIALISTS  | 2        |
|            | MARKET RESEACH ANALYSTS AND MARKETING SPECIALISTS  | 1        | 


## Data analysis
The preprocessor reads raw data and writes two output files: `processed_xxx.csv` and `soc_map_xxx.csv`. The processed data is skimmed from raw data with fields as 'state', 'soc_code' and 'soc_name'. Only certified records are written into processed data. 

The analysis code (H1BCounter) reads the processed data and SOC_map. In analysis code, the occupation name is inferred based on 'soc_code', 'soc_name' and the SOC_map. And two hash tables record the counting of each state/occupation. Then sort the two tables with counting decreasing and name alphabet. The first 10 or all (if the number of key is less than 10) records are written into `./output/top_10_occupations.txt` and `./output/top_10_states.txt`

## Performance and trade-offs

### Disk complexity
The program pre-processes data and save the processed data to disk. The processed data cost about 1/10 space of the raw data. The soc_map file is much small than the processed data. 
The advantages are:
1. Save time and memory: to infer the occupation name, using the processed data can help speed up x10. 
2. For further distributed analysis: both the soc_code_map and preprocessed data can be extended in distributed system safely.

### Memory complexity
The input file is read and processed line-by-line. So the largest memory consuming is the hash tables. There are about ~1k occupations, the memory cost is ~100k. And this memory cost will not increase dramatically with the statistic of input.

### Time complexity
In preprocessor, the most time consuming part is to split a line with semicolon. So the total time is O(n), n denotes the number of letters in the input file. Other operations are based on hash table with O(1) time. 

In analysis code, the time to loop all events is O(m), here m denotes the number of letters, which is about 1/10 of n. 

And sorting time is O(klogk), k is the number of states/occupation. Since k ~ 1000, no need to use heap (with O(klog10) time complexity).

# Run instructions
Make sure there are 1)`./output` directory and `./input/h1b_input.csv` in current directory. 

`sh run.sh`

# Acknowledgement
Thanks to the Insight fellowship team, this small project gave me a meaningful and happy weekend.
