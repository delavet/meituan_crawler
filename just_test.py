from point_crawler import point_crawler
from pprint import pprint
import constants
import requests


def try_food():
    headers = {
            "User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
            "Referer" : "https://meishi.meituan.com/i/",
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "x-requested-with" : "XMLHttpRequest"
        }
    data = {
        "poiId": 5086409
    }
    url = constants.meituan_sold_list
    print("start request sold list")
    r = requests.post(url, data = data, headers = headers)
    print("request ended")
    print(r.text)
    print(str(r.headers))
    with open("sold_list_record", 'w', encoding='utf-8') as wf:
        wf.write(r.text)
        wf.write('\n')
        wf.write(str(r.headers))


if __name__ == "__main__":
    try_food()
    #p = point_crawler(39.1234, 117.1212)
    #pprint(p.get_result_json(0))
