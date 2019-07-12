import constants
import json
import requests
import pickle
import time
import re,sys
import string
from ip_modifier import change_ip


CRAWL_SUCCESS = 0
IP_BANNED = -1
OTHER_EXCEPTION = 1


class comment_crawler:
    poi_id = 0
    disable_cnt = 0


    def __init__(self, poi_id):
        self.poi_id = poi_id

    
    def real_crawl_poi_comment(self):
        success = True
        msg = CRAWL_SUCCESS
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
            success = False
            msg = IP_BANNED
            jsn = json.loads(r.text)
            if type(jsn) == dict:
                dict_jsn = dict(jsn)
                if 'code' in dict_jsn.keys() and dict_jsn['code']==406:
                    msg = IP_BANNED
        finally:
            return success, msg, ret

    
    def crawl_poi_comment(self):
        ret = []
        disable_cnt = 0
        while True:
            success_label, msg, ret = self.real_crawl_poi_comment()
            if success_label:
                break
            elif msg == IP_BANNED:
                disable_cnt += 1
                change_ip()
                time.sleep(7)
            else:
                disable_cnt += 1
                time.sleep(7)
            print("=====comment crawl: retry count %d=====" % disable_cnt) 
            if disable_cnt > 10:
                break      
        return ret
            