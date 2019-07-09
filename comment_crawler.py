import constants
import json
import requests
import pickle
import time
import re,sys
import string


class comment_crawler:
    poi_id = 0


    def __init__(self, poi_id):
        self.poi_id = poi_id

    
    def crawl_poi_comment(self):
        url = constants.meituan_comment
        headers = {
            "User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
            "Referer" : "https://meishi.meituan.com/i/",
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "x-requested-with" : "XMLHttpRequest"
        }
        data = json.dumps({
            "poiId": self.poi_id
        })
        ret = []
        try:
            r = requests.post(url, headers = headers, data = data)
            return_msg = json.loads(r.text)
            status = dict(return_msg)['status']
            if status != 0:
                raise Exception("+++++comment: return status is not 0+++++")
            data_list = list(dict(dict(return_msg)['data'])['list'])
            ret = data_list
        except Exception as e:
            print("=====exception occurs when crawling comments=====")
            print("=====the exception reason=====")
            print(e)
            print("=====exception message=====")
            print(r.text)
        finally:
            return ret
            