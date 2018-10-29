# H1B statistic analyzer

A program to analyze H1B row data from past years, specifically calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications.

# Table of Contents
1. [Problem](README.md#problem)
    1. [Input]( README.md#input )
    2. [Output]( README.md#output )
    3. [Challenge]( README.md#challenge )
2. [Approach]( README.md#approach )
    1. [Data information]( README.md#data-information )
    2. [Data prerpocessing]( README.md#data-preprocessing )
    3. [Data analysis]( README.md#data-analysis )
    4. [Complexity and trade-offs]( README.md#complexity-and-trade-offs )
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

## Data information
I summarized the field names which are need for this problem for different years.

| Year | Status      | State                   | Zip code             | Occupation name   | SOC code          |
|:----:|-------------|-------------------------|----------------------|-------------------|-------------------|
| 2014 | STATUS      | LCA_CASE_WORKLOC1_STATE | PW_1                 | LCA_CASE_SOC_NAME | LCA_CASE_SOC_CODE |
| 2015 | CASE_STATUS | WORKSITE_STATE          | WORKSITE_POSTAL_CODE | SOC_NAME          | SOC_CODE          |
| 2016 | CASE_STATUS | WORKSITE_STATE          | WORKSITE_POSTAL_CODE | SOC_NAME          | SOC_CODE          |

So I am using following criteria to select the correct fields
```
Status: 'STATUS' in name
State: 'WORK' in name and 'STATE' in name
Zip code: the next element of State
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

### Inferring OCCUPATION
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

To solve format problem, I used two function `clean_soc_code` to transfer all SOC code as format 'XX-XXXX.XX'. If the SOC code is 6 digit or ends with '.99', the function replace the end with '.00'. The `clean_soc_name` function fix the occupation as all capital letter and remove extra space and quotas. For the typos, I need two dictionaries:
```
occupation_dict: a dictionary stores **valid** occupation name
soc_code_map: a hashmap, key is the correct SOC code with format XX-XXXX.XX and value is the correct occupation name
```
With the help of these two dictionaries, the occupation name can be found with following steps:
1. If occupation_name in `occupation_dict`, means it is a valid name;
2. Else, means it is a new name or wrong name. If the SOC code in `soc_code_map`, use the value in the hash map;
3. Else, means it might be a new name with new SOC code. Or both the name and SOC code are wrong. In this case, just return the name. 

To get these two dictionaries, there are two methods in my program:
1. Using file from [website](https://www.onetcenter.org/taxonomy/2010/list.html).
  * Pro: The SOC code and occupation name can be always valid. 
  * Con: Need to update the file for different year.
2. Using the input data, for each SOC code, choose the occupation name with most counting as the value. For example, in the table below, the correct name corresponding to '13-1161.00' should be 'MARKET RESEARCH ANALYSTS AND MARKETING SPECIALISTS'. Others are missing information or typos.
  * Pro: No need extra input; the dictionaries can be self updated;
  * Con: Not accurate with low input statistic 

| SOC code   |  Occupation name                                   | Counting |
|------------|----------------------------------------------------|----------|
| 13-1161.00 | MARKET RESEARCH ANALYSTS AND MARKETING SPECIALISTS | 6978     |
|            | MARKET RESEARCH ANALYSTS AND MARKETING             | 167      |
|            | MARKET RESEARCH ANALYST AND MARKETING SPECIALISTS  | 2        |
|            | MARKET RESEACH ANALYSTS AND MARKETING SPECIALISTS  | 1        | 

In the program, the 'input data' method is used in data preprocessing. The ['website file' method](https://github.com/amcw7777/h1b-counter/blob/master/src/occupation_checker.py) is use to check the performance.

## Data analysis
The preprocessor reads raw data and writes two output files: `processed_xxx.csv` and `soc_map_xxx.csv`. The processed data is skimmed from raw data with fields as 'state', 'soc_code' and 'soc_name'. Only certified records are written into processed data. 
The analysis code (H1BCounter) reads the processed data and SOC_map. In analysis code, the occupation name is inferred based on 'soc_code', 'soc_name' and the SOC_map. And two hash tables record the counting of each state/occupation. Then sort the two tables with counting decreasing and name alphabet. The first 10 or all (if the number of key is less than 10) records are written into `./output/top_10_occupations.txt` and `./output/top_10_states.txt`

## Complexity and trade-offs

### Disk complexity
The program preprocesses data and save the processed data to disk. The processed data cost about 1/10 space of the raw data. The soc_map file is much small than the processed data. We can certainly process the data to infer the occupation in preprocessor, and only save the hash table as state-counting and occupation-counting. My opinion is:
1. Save a processed data helps running analysis faster. Once we have new interested in data or to infer new features. It can be fast tuned;
2. If the raw data is very large, to process data can help analyzing in distributed system. For example, if the raw data are divided, the SOC_code map will be bias and may make mistake.

### Memory complexity
The input file is read and processed line-by-line. So the largest memory consuming is the hash tables. There are about ~1k occupations, so the memory cost is fordable. And this memory cost will not increase dramatically with the statistic of input.

### Time complexity
In preprocessor, the most time consuming part is to split a line with semicolon. So the total time is O(n), n denotes the number of letters in the input file. To find a state based on Zip code needs loop Zip code ranges for states. But the records with incorrect state is rare. Other operations are based on hash table with O(1) time. 
In analysis code, the time to loop all events is O(m), here m denotes the number of lines. So it is much faster. And sorting cost O(klogk), k is the number of states/occupation. The sorting time is ignorable.

# Run instructions
Make sure there are 1)`./output` directory and `./input/h1b_input.csv` in current directory. 
`sh run.sh`
