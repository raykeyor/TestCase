import os
import time
import logging
import difflib
import re
from selenium import webdriver
import pymongo
from pymongo import MongoClient
from conf.settings import MONGODB
from core.crawler.config import PARAMS
from core.core_api import *
from selenium.webdriver.chrome.options import Options
from bson import ObjectId

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='logs/monogo.log',
                    filemode='a'
                    )


# 在Setting文件中初始化数据库的信息
class SettingEnv:

    def __init__(self, setting_path, setting_command):
        os.system("python {0} {1}".format(setting_path, setting_command))
        logging.info("The database set already .")
        time.sleep(1)

# Create the database instance
class ConnectMonGoQA:
    def __init__(self):
        self.client = MongoClient('mongodb://{0}:{1}@{2}/{3}'.format(MONGODB['user'],
                                           MONGODB['passwd'],
                                           MONGODB['host'],
                                           MONGODB['dbname']))
        self.db = self.client[MONGODB['dbname']]
        print(MONGODB['user'], MONGODB['passwd'], MONGODB['host'], MONGODB['dbname'])

    def query_mongo(self, collection, type=None, filter_dict=None):
        self.coll = self.db.get_collection(collection).find(filter_dict).distinct(type)
        self.coll_count = self.db.get_collection(collection).find(filter_dict).count()
        logging.info("The count for {0} is {1} ".format(collection, self.coll_count))
        return self.coll

    def query_response(self, collection, filter_dict=None):
        self.mongo_response = self.db.get_collection(collection).find(filter_dict).distinct("resp_content")
        return self.mongo_response[0]

    def save_data(self, collection,file_name, file_origin, filter_dict=None, type=None ):

        self.coll = self.db.get_collection(collection).find(filter_dict).distinct(type)
        self.coll_count = self.db.get_collection(collection).find(filter_dict).count()
        logging.info("The count for {0} is {1} ".format(collection, self.coll_count))

        with open(file_name, 'w', encoding="utf-8") as f:
            list_url = []
            for data in self.coll:
                data_split = data.split("?")
                list_url.append(data_split[0])

            for data in sorted(set(list_url)):
                data = re.sub(r":\d+", "", data)
                f.write("".join((data, "\n")))

        with open(file_origin, 'w', encoding="utf-8") as f:
            for data in self.coll:
                f.write("".join((data, "\n")))

    def remove_mongo(self,collection):
        self.db.get_collection(collection).remove()

    #insert into db
    def insert_data(self,collection,doc):
        coll=self.db.get_collection(collection)
        coll.save(doc)

    def remove(self,collection,doc):
        coll = self.db.get_collection(collection)
        coll.remove(doc)

    def __del__(self):
        self.client.close()


class File:

    def __init__(self,file_name,file_type,code_type):
        self.file_name = file_name
        self.file_type = file_type
        self.code_type = code_type

    def readFile(self):
        with open(self.file_name,self.code_type,encoding=self.code_type)as f:
            for data in f:
                pass


if __name__ == '__main__':
    setting_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_setting.py')
    setting_command = "QA"
    collection_tamper = "res_tamper"
    collection_tmp = 'crawler_urls_tmp'
    collection_clean = "crawler_urls"
    collection_tamper_line='tamper_lines'
    collection_qa = 'qa_test'
    # setting data config
    senv = SettingEnv(setting_path, setting_command)


    # clean the monogo collection
    clean_monogo = ConnectMonGoQA()
    data = input("Do you want to remove the data:\n")
    if data =='1':
        clean_monogo.remove_mongo(collection_clean)
        clean_monogo.remove_mongo(collection_tmp)
        clean_monogo.remove_mongo(collection_tamper)
        clean_monogo.remove_mongo(collection_tamper_line)
        clean_monogo.remove_mongo(collection_qa)
        print("THe database was removed already .")
    else:
        print("THe database did not be remove already .")

