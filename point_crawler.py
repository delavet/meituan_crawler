import constants
import json
import requests
import pickle
import time
import re,sys
import string


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
        url = constants.meituan_near_restaurant
        headers = {
            "User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
            "Cookie" : "ci=1;rvct=1;latlng=" + str(self.latitude) + "," + str(self.longitude) + ";;uuid=e7cc30da-c5ce-457b-8be7-ac327f9bd7d0; client-id=b5674afa-a719-45a4-9109-ffe79b719e68",
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
                    self.restaurants[poiid] = info
                except Exception as e1:
                    print("!!!!!one unparsable result!!!!!")
                    continue
        except Exception as e:
            print("=====the exception reason=====")
            print(e)
            print("=====exception message=====")
            print(r.text)

    
    def crawl_point(self):
        rf = open('ids.pkl', 'rb')
        ids = list(pickle.load(rf))
        rf.close()
        with open('ids.pkl', 'wb') as wf, open('data/'+ self.get_latlon() + '.pkl') as data_f:
            for p in range(20):
                get_result_json(p)
                time.sleep(5)
            for id, info in self.restaurants.items():
                if id in ids:
                    self.restaurants.pop(id)
                    continue
                else:
                    ids.append(id)
            pickle.dump(ids, wf)
            pickle.dump(self.restaurants, data_f)
            
                    

