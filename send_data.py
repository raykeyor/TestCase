import requests
import time
import logging
from pymongo import MongoClient
import pymongo
from conf.settings import MONGODB
import re,os
import difflib
from bson import ObjectId
from pprint import pprint
import re



class Send:

    def __init__(self,url):
        self.header={"User-Agent":"Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;"}
        self.url = url

    def content(self):
        if "http" not in self.url:
            self.url = ''.join(("https://", self.url))
        try:
            requests.get(self.url, headers=self.header,verify=False)

        except:
            if "https" in self.url:
                self.url.replace("https","http")
            else:
                self.url.replace("http", "https")
        finally:
            self.resp=requests.get(self.url, headers=self.header,verify=False).content
            dict_res={}
            dict_res['url'] = self.url
            dict_res["resp_content"] = self.resp  # bytes(self.resp,encoding="utf-8")
            dict_res['time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            db = ConnectMonGoQA()
            db.insert_data("crawler_urls",dict_res)


# Create the database instance
class ConnectMonGoQA:
    def __init__(self):
        self.client = MongoClient('mongodb://{0}:{1}@{2}/{3}'.format(MONGODB['user'],
                                           MONGODB['passwd'],
                                           MONGODB['host'],
                                           MONGODB['dbname']))
        self.db = self.client[MONGODB['dbname']]

    def remove_mongo(self,collection):
        self.db.get_collection(collection).remove()

    #insert into db
    def insert_data(self,collection,doc):
        # collection=self.db.qa_test
        coll=self.db.get_collection(collection)
        coll.save(doc)

    #query
    def query(self,url):

        self.coll = self.db.get_collection("crawler_urls").find({"url":url}).sort('begin_time', pymongo.DESCENDING)
        self.coll_count = self.db.get_collection("crawler_urls").find({"url":url}).count()
        for i in range(self.coll_count):
            path = os.path.join("Data","new", (str(i)+".html"))
            with open(path,"wb") as f:
                res = self.db.get_collection("crawler_urls").find({"url":url})[i]["resp_content"]
                f.write(res)

    def __del__(self):
        self.client.close()




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


if __name__ == "__main__":
    url="https://www.dayspay.com.cn/daysaps/"
    input_data= input("Input the num:")
    if input_data =="1":
        send = Send(url)
        send.content()
    elif input_data =="2":
        con = ConnectMonGoQA()
        con.query(url)
    else:
        pass
