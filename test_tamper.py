from core.core_api import *
from TestCase.test_common import *
from bson import ObjectId
import logging
import requests
import time
import cchardet,chardet
import sys

class TestTamper:

    def __init__(self,list_id):
        # print(list_id)
        watch_tamper(list_id)

class MonogoObjId:

    def __init__(self):
        self.collection_clean = "crawler_urls"
        self.collection_tamper = "res_tamper"
        self.monogo = ConnectMonGoQA()
        self.list_tamper_1 = []
        self.list_tamper_2 = []
        self.list_url=[]
        self.list_url_tamper=[]


    def get_len_url(self):

        leng = self.monogo.db.get_collection(self.collection_clean).find().count()

    def get_id(self):

        for list_url in self.monogo.query_mongo(self.collection_clean, type="url"):
            res = self.monogo.db.get_collection(self.collection_clean).find({"url": list_url})
            count = res.count()
            if count == 1:
                self.list_tamper_1.append(ObjectId(res[0]["_id"]))
            else:
                self.list_url.append(list_url)
                self.list_tamper_2.append(ObjectId(res[0]["_id"]))

        return self.list_tamper_1,self.list_tamper_2

    def get_tamper(self,collection):
        for list_url in self.monogo.query_mongo(collection, type="url"):
            res = self.monogo.db.get_collection(collection).find({"url": list_url})
            count = self.monogo.db.get_collection(collection).find({"url": list_url}).count()
            self.list_url_tamper.append(list_url)

        return  set(self.list_url_tamper)

class ExecuteMonogo:

    def __init__(self,collection):
        self.collection = collection
        self.monogo = ConnectMonGoQA()
        self.list_url = []
        self.list_url1 = []
        self.list_url2 = []
        self.list_url3 = []
        self.dict_id_url={}


    def id_url_dict(self,url_list):
        monogo_response = self.monogo.db.get_collection(self.collection)
        for url in url_list:
            id = monogo_response.find({'url':url}).sort('begin_time', pymongo.DESCENDING).distinct("_id")[0]
            self.dict_id_url[id] = url
        return self.dict_id_url

    def duplicate_url_crawel(self):
        monogo_response = self.monogo.db.get_collection(self.collection)


    def url_database(self):
        url_list=[]
        monogo_response = self.monogo.db.get_collection(self.collection)
        for i in monogo_response.distinct("url"):
            url_list.append(i)
        return url_list

    def save_mon(self,list):
        monogo_response = self.monogo.db.get_collection(self.collection)

        for i in range(len(list)):
            num = monogo_response.find({'url': list[i]}).count()
            logging.info("{}:{}".format(i,list[i]))
            if num > 1:
                data = monogo_response.find({'url': list[i]}).sort('begin_time', -1)
                self.list_url1.append(data[0].get("resp_content"))
                self.list_url2.append(data[1].get("resp_content"))
                self.list_url3.append(data[2].get("resp_content"))
                self.list_url.append(list[i])

            with open(''.join(('logs/list_url1_', str(i), '.html')), 'wb')as f:
                f.write(self.list_url1[i])

            with open(''.join(('logs/list_url2_', str(i), '.html')), 'wb')as f:
                f.write(self.list_url2[i])

            with open(''.join(('logs/list_url3_', str(i), '.html')), 'wb')as f:
                f.write(self.list_url3[i])
            print(list[i])

def invoke_htmldiff(file_loads,file_mens, file_compare,code):
    hd = difflib.HtmlDiff()

    loads = ''

    with open(file_loads, 'r',encoding=code)as loads:
        loads = loads.readlines()

    mens = ''

    with open(file_mens, 'r',encoding=code) as mens:
        mens = mens.readlines()

    with open(file_compare, 'a+') as f:
        f.write(hd.make_file(loads, mens))
        print("Result gennerated !")



class Send:

    def __init__(self):
        self.header={"User-Agent":"Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;"}


    def content(self,collection):

        db = ConnectMonGoQA()
        self.url = 'https://www.lljr.com/about/lxwm'
        self.resp = requests.get(self.url, headers=self.header).content
        dict_res={}
        dict_res['url'] = self.url
        dict_res['respond'] = self.resp
        dict_res['time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        db.insert_data(collection,dict_res)


if __name__ == "__main__":
    collection_tmp = 'crawler_urls_tmp'
    collection_clean = "crawler_urls"
    collection_tamper = "res_tamper"
    collection_line = "tamper_lines"
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))

    #get the monogo_id from crawel db which url is more than 1 record
    monogo_data = MonogoObjId()
    list_tamper_1,list_tamper_2=monogo_data.get_id()
    logging.info('{} {}'.format(list_tamper_2,len(list_tamper_2)))

    # #execute the taper api,and return the url in tamper db
    TestTamper(list_tamper_2)
    list_tamper_url=monogo_data.get_tamper(collection_tamper)

    # #create the dict for objectid and url
    execute_db = ExecuteMonogo(collection_clean)
    dict_id_url = execute_db.id_url_dict(list_tamper_url)
    # print(dict_id_url)


    # #遍历在tamper模板库里的url
    # tamper_line_url=ExecuteMonogo(collection_line)
    # print(tamper_line_url.url_database())

    list_url_id=[] #'https://www.lljr.com/about/lxwm'
    for obj, url in execute_db.id_url_dict(list_tamper_url).items():
        list_url_id.append(url)
    print(len(list_url_id))

    execute_db.save_mon(list_url_id)

    # execute_db.compare_mon(len(list_url_id))

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    # send=Send()
    # send.content(collection_clean)
    # list_obj=[ObjectId("5b1502a8e1382370e71e00f8"),]
    # TestTamper(list_obj)
