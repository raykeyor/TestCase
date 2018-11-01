# import requests
# import difflib
#
# header=header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1', }
# res = requests.get("https://mp.weixin.qq.com:443/s/GWFex1L_MJr7Cwm_aveAkQ",headers=header)
#
# with open("cont.txt",'wb') as f:
#     f.write(res.content)
#
# res1 = requests.get("https://mp.weixin.qq.com:443/s/GWFex1L_MJr7Cwm_aveAkQ",headers=header)
# with open("cont1.txt",'wb') as f:
#     f.write(res.content)
#
# hd=difflib.HtmlDiff()
# loads=''
#
# with open('cont.txt','r')as loads:
#     loads=loads.readlines()
#
# mens=''
#
# with open('cont1.txt','r') as mens:
#     mens=mens.readlines()
#
#
# with open('compare.html','a+') as f:
#     f.write(hd.make_file(loads,mens))
#     print("Result gennerated !")
#     f.close()

# import cchardet
# print(cchardet.detect("""
# <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "//www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
# """))

import os
import sys,cchardet

def rmfile(filename):
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)

    list_file=[]
    for dir, file_path, file in os.walk(path):
        for i in file:
            list_file.append(os.path.join(dir,i))

    for i in list_file:
        os.remove(i)
if __name__ == "__main__":
    rmfile('logs')
    rmfile('compares')
    rmfile('Data/new')
    import time
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))) #1528183510


