# Flurry API
## Analytics scripts
### This repo contains a python script that accesses CHPL app usage data via the Flurry API via their website https://y.flurry.com and associated API console. The script makes a query and converts the results to CSV so they can be used to create a dataset in the Open Data Portal.

### Input
Analytics Reporting API V4 service object
https://www.googleapis.com/auth/analytics.readonly

### Output
 https://www.chapelhillopendata.org/explore/dataset/flurry/. 
 
 ### Frequency
 
 These scripts are run daily and the dataset is updated shortly after.

#### dailybibsearches.py
creates dailybibliosearch.csv

#### dailysearchtoch.py
creates dailytownsearch.csv

#### dailysessionstoch.py
creates dailytownsessions.csv

#### monthlybibsearches.py
creates monthlybibliosearch.csv

#### monthlysearchtoch.py
creates monthlytownsearch.csv

#### monthlysessionstoch.py
creates monthlytownsessions.csv

#### dailysearches.py 
creates dailysearch.csv

#### dailysessions.py
creates dailysessions.csv

#### flurry.py
flurry.csv

#### monthlysearches.py
creates monthlysearch.csv

#### monthlysessions.py
creates monthlysessions.csv
