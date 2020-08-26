# Git_repo_scrapper1
# GitHub Public repository scrapper

Package requirements:-
--> 'requests' package must be installed 

1- 'main. Pay' is main file from where we will make api calls. <br/>
    We have also limited no. of api calls to 34 and put sleep of 3 seconds to not exceed call limit.<br/>
2- Python package 'api_filter' has 'filter. Pay' file. It will pass filter parameters to apply, call string to fetch the required data only.<br/>
3- Python package 'json_filter' has 'filter_json_to_csv. Pay' file which will pass filter parameters to filter json data from api calls made. <br/>
4- Output csv file will be generated in the parent directory as 'output.csv'.<br/>
5- user has to only run 'main.py' file and output file will be created.<br/>
