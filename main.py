import requests
import os
import csv
from api_filter import filter
from json_filter import filter_json_to_csv

logged_user = os.environ['USER']
file_path = os.environ['PWD']
print(f'Logged User:-{logged_user}')
print(f'Current Path:-{file_path}')

page_content = []
page_num: int = 1
file_name = "new_output.csv"
header=[filter_json_to_csv.name,filter_json_to_csv.description,
                                                    filter_json_to_csv.html_url,
                                                    filter_json_to_csv.watchers_count,
                                                    filter_json_to_csv.stargazers_count,
                                                    filter_json_to_csv.forks_count]

def api_pages():
    global page_num
    try:
        api_page_obj = requests.get(
            f'https://api.github.com/search/repositories?page={page_num}&q=+{filter.filter_2}:>=200+language:{filter.filter_language}&order=desc').json()
        for data in api_page_obj['items']:
            page_content.append(data)
        page_num += 1
        # time.sleep(5)   #optional
        api_pages()

    except KeyError as k:
        print('Limit Exceeded ',k,api_page_obj)
    except:
        print('ERROR OCCURRED')


def header_check():
    with open(file_name,'a+') as file:
        file.seek(0)
        r_csv = csv.reader(file)
        r_csv = list(r_csv)
        if file.tell()==0:  # To check if file is empty or old , IF empty then add HEADERS
            d_csv = csv.DictWriter(file,fieldnames=header)
            d_csv.writeheader()
            print('Header Adder')
        elif header==r_csv[0]:  # if file is not empty , compare 1st row of file with header and if same DO NOTHING
            print('same header')
        else:  # if file is not empty and header do not match , truncate file and add HEADERS
            file.seek(0)
            file.truncate()
            d_csv = csv.DictWriter(file,fieldnames=[filter_json_to_csv.name,filter_json_to_csv.description,
                                                    filter_json_to_csv.html_url,
                                                    filter_json_to_csv.watchers_count,
                                                    filter_json_to_csv.stargazers_count,
                                                    filter_json_to_csv.forks_count])
            d_csv.writeheader()
            print('file truncated and header added')


def json_to_csv():
    header_check()
    with open(file_name,"a+") as file:
        csv_file = csv.writer(file)
        new_element = [x for x in page_content if x[filter_json_to_csv.stargazers_count] >= 2000]

        for item in new_element:
            csv_file.writerow([item[filter_json_to_csv.name],
                               item[filter_json_to_csv.description],
                               item[filter_json_to_csv.html_url],
                               item[filter_json_to_csv.watchers_count],
                               item[filter_json_to_csv.stargazers_count],
                               item[filter_json_to_csv.forks_count]])
    print(f'Check {file_name} file')

print('start')
api_pages()
json_to_csv()
print('END')
