from core.core_api import *
import requests
from TestCase.test_crawel import *
from TestCase.test_common import *


class TestYara:

    def __init__(self):
        self.rule = rule_init()

    def test_detect(self, url, response):
        dict_data = start_detect(self.rule, response)
        return url, dict_data

    def save_yara_data(self,url,result, file_name):
        with open(file_name,'a') as f:
            if type(result.get("status")) != str:
                f.write("{} : {}\n".format(url, result.get("status")))
            elif result.get("status") == "None":
                logging.info("{} : {}".format(url, result.get("status")))
            else:
                print(url, result.get("status"))

    def test_detct_js(self,response):
        dict_data = start_detect(self.rule,response)
        print(dict_data.get("status"))

if __name__ == "__main__":

    # setting_path = "/opt/trunk/engine/conf/change_env.py"
    # setting_command = "QA"
    # collection_tmp = 'crawler_urls_tmp'
    collection_clean = "crawler_urls"
    # url_crawl_one = "https://www.tongfudun.com"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', }
    file_name = "logs/erroneous.txt"

    #init the db and yara function.
    connMon_tmp = ConnectMonGoQA()
    testYara = TestYara()

    #save the result for erroneous
    count=0
    for list_url in connMon_tmp.query_mongo(collection_clean, "url"):
        count += 1
        print(list_url,count)
        res = connMon_tmp.query_response(collection_clean, filter_dict={"url": list_url})
        result = testYara.test_detect(list_url, res)
        testYara.save_yara_data(result[0], result[1],file_name)

    #coinhive
    list_hive=[
        "https://coinhive.com/lib/coinhive.min.js",
        "https://authedmine.com/lib/authedmine.min.js",
        "https://authedmine.com/lib/simple-ui.min.js",
        "https://coin-hive.com/lib/coinhive.min.js",
        "http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquerey.min.js",
        "https://do69ifsly4.me/v.js",
        "https://coin-hive.com/lib/captcha.min.js"]

    # testYara = TestYara()
    # for url in list_hive:
    #     print(url)
    #     try:
    #         res=requests.get(url,headers=header,timeout=5)
    #         con=res.content
    #         testYara.test_detct_js(con)
    #     except Exception as e:
    #         print(url)
    
    # Test casino
    # list_casino = ["葡京","澳门赌","博彩","彩票","百家乐","盘口","金宝博","外围赌球","12BET","365BET"]
    # url='http://172.246.93.188/'
    # res=requests.get(url,headers=header)
    # print(res.content)

    # testYara = TestYara()
    # testYara.test_detct_js(res.content)


    # # # list_1=["尼玛","砖家","艹","草泥马","特么的","滚粗","蛋疼","小婊砸","傻X","跪舔","绿茶婊","心机婊","碧莲","碧池","屄","阴茎","A片","黄片",'有屎以来最最最不要脸的biao子，换一般人早去死了，还好意思在这里博眼球。做为女人张开两腿给别的男人艹，愧你还好意思活着！！！！真为你感到悲哀！！！！即使王宝强转移财产，也是很正常的，难道还送给在外苟且的狗男女啊？？？你不先出轨，他会转移财产？？？你真的可以去死了，一万次都嫌少！！！']
    # url = 'http://comment5.news.sina.com.cn/comment/skin/default.html?channel=yl&newsid=comos-fyzeyqc1080357&group=0'
    # res = requests.get(url, headers=header)
    # # print(res.content)
    # # testYara = TestYara()
    # testYara.test_detct_js(res.content)