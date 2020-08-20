import requests
import csv
from api_filter import filter
from json_filter import filter_json_to_csv
import time

api_request_obj = requests.get(
    f'https://api.github.com/search/repositories?q=+{filter.filter_parameters.filter_2}:>=200+language:{filter.filter_parameters.filter_language}').json()
total_repo_count = api_request_obj['total_count']
print(f'There are total {total_repo_count} repo matching our criteria')
page_count = (total_repo_count // 30)  # max 30 search results can be fetched in single call
if page_count > 34 :  #checking no.of api calls is not exceeding 1000 and in case it exceeds calls are limited to 34 calls.
    page_count = 34
    print(f'Limiting api calls to{page_count}')
page_content = []


def api_pages() :
    for page_num in range(1 , page_count+1) :  # will go through every page matching our filter criteria
        api_page_obj = requests.get(
            f'https://api.github.com/search/repositories?page={page_num}&q=+{filter.filter_parameters.filter_2}:>=200+language:{filter.filter_parameters.filter_language}&order=desc').json()
        time.sleep(3)#to not exceed max. permissible limit
        for each_page in range(0,30) :  # At at a time we can fetch only 30 repository , so appending each page to page_content list
            try :
                page_content.append(api_page_obj['items'][each_page])
            except :
                print(api_page_obj)
        print(f'{page_num} api calls made')


file_name = "output.csv"

def json_to_csv() :
    with open(file_name , "w") as file :
        csv_file = csv.writer(file)
        csv_file.writerow([filter_json_to_csv.json_parameters.name , filter_json_to_csv.json_parameters.description ,
                           filter_json_to_csv.json_parameters.html_url ,
                           filter_json_to_csv.json_parameters.watchers_count ,
                           filter_json_to_csv.json_parameters.stargazers_count ,
                           filter_json_to_csv.json_parameters.forks_count])

        for item in page_content :
            if item[filter_json_to_csv.json_parameters.stargazers_count] > 2000 :
                csv_file.writerow([item[filter_json_to_csv.json_parameters.name] ,
                                   item[filter_json_to_csv.json_parameters.description] ,
                                   item[filter_json_to_csv.json_parameters.html_url] ,
                                   item[filter_json_to_csv.json_parameters.watchers_count] ,
                                   item[filter_json_to_csv.json_parameters.stargazers_count] ,
                                   item[filter_json_to_csv.json_parameters.forks_count]])


api_call = api_pages()
csv_file = json_to_csv()
