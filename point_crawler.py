import constants
import json
import requests
import pickle
import time
import re,sys
import string
from ip_modifier import change_ip
from comment_crawler import comment_crawler


CRAWL_SUCCESS = 0
IP_BANNED = -1
OTHER_EXCEPTION = 1


class point_crawler:
    restaurants = {}
    latitude = 39.3
    longitude = 116.3


    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
    

    def get_latlon(self):
        return str(self.latitude) + "," + str(self
        .longitude)
    

    def get_result_json(self, page):
        success = True
        msg = CRAWL_SUCCESS
        url = constants.meituan_near_restaurant
        cookie_str = "ci=1;rvct=1;latlng=" + str(self.latitude) + "," + str(self.longitude) + ";"
        if constants.uuid != None:
            cookie_str += "uuid="+constants.uuid+";"
        if constants.client_id != None:
            cookie_str += "client-id="+constants.client_id+";"
        headers = {
            "User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
            "Cookie" : cookie_str,
            "Referer" : "https://meishi.meituan.com/i/",
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "x-requested-with" : "XMLHttpRequest"
        }
        data = json.dumps({
            "limit" : 50,
            "offset" : page * 50,
            "sort" : "distance"
        })
        try:
            r = requests.post(url, headers = headers, data = data)
            r_headers = r.headers
            set_cookie = r_headers['Set-Cookie']
            cookies = set_cookie.split(';')
            for cookie in cookies:
                if cookie.startswith("uuid"):
                    constants.uuid = cookie.split('=')[1]
                if cookie.startswith("client-id"):
                    constants.client_id = cookie.split('=')[1]
            print("receive: ", r.text)
            print("receive headers: ", str(r.headers))
            return_msg = json.loads(r.text)
            if type(return_msg) != dict:
                raise Exception("+++++return message is not a dict+++++")
            msg_dict = dict(return_msg)
            if 'status' not in msg_dict.keys() or msg_dict['status'] != 0 or 'data' not in msg_dict.keys():
                raise Exception("+++++the message format is failed+++++")
            data_dict = msg_dict['data']
            if type(data_dict) != dict:
                raise Exception("+++++return data is not a dict+++++")
            if 'poiList' not in  dict(data_dict).keys():
                raise Exception("+++++the message format is failed+++++")
            poiList_dict = dict(data_dict)['poiList']
            if type(poiList_dict) != dict:
                raise Exception("+++++return poi list json is not a dict+++++")
            if 'poiInfos' not in dict(poiList_dict).keys():
                raise Exception("+++++the message format is failed+++++")
            if type(poiList_dict['poiInfos']) != list:
                raise Exception("+++++return poi infos is not a list+++++")
            poi_infos = list(poiList_dict['poiInfos'])
            for raw_info in poi_infos:
                try:
                    info = {}
                    if 'poiid' not in raw_info.keys():
                        continue
                    poiid = raw_info['poiid']
                    info['poiid'] = poiid
                    info['avgPrice'] = raw_info['avgPrice'] if 'avgPrice' in raw_info.keys() else None
                    info['avgScore'] = raw_info['avgScore'] if 'avgScore' in raw_info.keys() else None
                    info['cateName'] = raw_info['cateName'] if 'cateName' in raw_info.keys() else None
                    info['channel'] = raw_info['channel'] if 'channel' in raw_info.keys() else None
                    info['showType'] = raw_info['showType'] if 'showType' in raw_info.keys() else None
                    info['frontImg'] = raw_info['frontImg'] if 'frontImg' in raw_info.keys() else None
                    info['lat'] = raw_info['lat'] if 'lat' in raw_info.keys() else None
                    info['lng'] = raw_info['lng'] if 'lng' in raw_info.keys() else None
                    info['name'] = raw_info['name'] if 'name' in raw_info.keys() else None
                    info['poiImgExtra'] = raw_info['poiImgExtra'] if 'poiImgExtra' in raw_info.keys() else None
                    info['areaName'] = raw_info['areaName'] if 'areaName' in raw_info.keys() else None
                    info['extraServiceTags'] = raw_info['extraServiceTags'] if 'extraServiceTags' in raw_info.keys() else []
                    info['rotationTags'] = raw_info['rotationTags'] if 'rotationTags' in raw_info.keys() else []
                    info['smartTags'] = raw_info['smartTags'] if 'smartTags' in raw_info.keys() else []
                    info['openHours'] = raw_info['openHours'] if 'openHours' in raw_info.keys() else {}
                    info['preferentialInfo'] = raw_info['preferentialInfo'] if 'preferentialInfo' in raw_info.keys() else {}
                    cmt_crawler = comment_crawler(poiid)
                    comments = cmt_crawler.crawl_poi_comment()
                    info['comments'] = comments
                    self.restaurants[poiid] = info
                except Exception as e1:
                    print("!!!!!one unparsable result!!!!!")
                    print(str(e1))
                    continue
        except Exception as e:
            success = False
            msg = OTHER_EXCEPTION
            print("=====exception occurs when crawling points=====")
            print("=====the exception reason=====")
            print(e)
            print("=====exception message=====")
            print(r.text)
            jsn = json.loads(r.text)
            if type(jsn) == dict:
                dict_jsn = dict(jsn)
                if 'code' in dict_jsn.keys() and dict_jsn['code']==406:
                    msg = IP_BANNED
                

    
    def crawl_point(self):
        rf = open('ids.pkl', 'rb+')
        ids = list(pickle.load(rf))
        rf.close()
        with open('ids.pkl', 'wb') as wf, open('data/'+ self.get_latlon() + '.pkl', 'wb') as data_f:
            for p in range(20):
                while True:
                    print("crawling point: ", self.get_latlon(),"; page: ",str(p))
                    success, msg = get_result_json(p)
                    if success:
                        break
                    elif msg == IP_BANNED:
                        change_ip()
                        time.sleep(7)
                    else:
                        time.sleep(7)
                time.sleep(5)
            for id, info in self.restaurants.items():
                if id in ids:
                    self.restaurants.pop(id)
                    continue
                else:
                    ids.append(id)
            pickle.dump(ids, wf)
            pickle.dump(self.restaurants, data_f)
            
                    

