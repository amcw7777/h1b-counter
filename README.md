# H1B statistic analyzer

A program to analyze H1B row data from past years, specifically calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications.

Problem, Approach and Run instructions sections

## Run instructions
Make sure there are 1)`./output` directory and `./input/h1b_input.csv` in current directory. 
`sh run.sh`

## Problem
Design a program to analyze [raw immigration data](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf) to calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications. 
The program requires:
1. The code should be modular and reusable for future without needing to change the code;
2. The code can deal with special case like missing data or typos;
3. Only allowed to use the default data structures that come with that programming language.

### Input
The input data is a semicolon separated (";") format. The first row is field names. The description of the field names can be find [here](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_FY17_Record_Layout.pdf). **The fields name are different in different years.**

### Output
The program must create 2 output files:
* `top_10_occupations.txt`: Top 10 occupations for certified visa applications
* `top_10_states.txt`: Top 10 states for certified visa applications
Requirements:
1. Each line holds one record and each field on each line is separated by a semicolon (;).
2. The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__ (__`TOP_STATES`__).
3. There can be fewer than 10 lines in each file.
4. Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and 1.04% should be rounded to 1.0%. Also, 1% should be represented by 1.0%

### Challenges
1. Even the data is separated by semicolon, not all the semicolons are delimiter. (For example, `aaa;"bbb;ccc";;ddd` should be read as `'aaa', 'bbb;ccc', '', 'ddd'`;
2. Different field names in different years;
3. Missing data or typo: it is the hardest part in the problem. The work states information are all good. But there are missing or typos in occupation name and SOC code data.

## Approach

### Data information

### Data clean

### Inferring occupation 

### Data analysis

### Trade-offs
