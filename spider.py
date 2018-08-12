import requests
from urllib.parse import quote
from settings import *
from bs4 import BeautifulSoup
import sys
import time
import random
import csv


class crawl(object):

    def __init__(self):
        self.MAX_PAGE = MAX_PAGE
        self.PAGE_TRACK = PAGE_TRACK    #跟踪次数
        self.FLAG = FLAG                #设置标志位
        self.PAGE_LIST = PAGE_LIST      #第一次获取失败的 html 的 列表
        self.URL_START =  URL_START     #初始链接
        self.PARAMS = PARAMS            #url 构造参数
        self.PROXY_POOL_API = "http://127.0.0.1:5555/random" 
        self.proxy_save = None   #用于存储代理
        self.proxy_con  = 0      #用于控制代理什么时候更换 
        self.fieldnames = ['代码','名称','现价','涨跌幅']
        self.file = open("ths.csv",'a', newline='')   #打开文件
        self.writer = csv.DictWriter(self.file, fieldnames = self.fieldnames)
        self.writer.writeheader()



    
    def proxy_get(self, num_retries=2):
        """
        #代理获取模块

        """
        try:
            r_proxy = requests.get(self.PROXY_POOL_API, timeout = 5)
            proxy = r_proxy.text    #指定代理
            print("代理是", proxy)
            proxies = {
                "http": 'http://' + proxy,
                "https": 'https://' + proxy,
                }
            return proxies
        except:
            if num_retries > 0:
                print("代理获取失败，重新获取")
                self.proxy_get(num_retries-1)

   
    def url_yield(self):
        """
        :func 用于生成url
        :yield items
        """
        for i in range(1, self.MAX_PAGE + 1 ):
            self.PAGE_TRACK = i         #页面追踪
            self.FLAG += 1              #每次加1
            print('FLAG 是：', self.FLAG)
            url = "{}{}{}".format(self.URL_START, i, self.PARAMS) 
            yield url

    def url_omi(self):
        print("开始补漏")
        length_pl = len(self.PAGE_LIST) 
        if length_pl != 0:          #判断是否为空
            for i in range(length_pl):
                self.PAGE_TRACK = self.PAGE_LIST.pop(0)                  #构造一个动态列表, 弹出第一个元素
                url = "{}{}{}".format(self.URL_START, self.PAGE_TRACK, self.PARAMS) 
                yield url
    


    def downloader(self, url, num_retries=3):
        if self.proxy_con == 0:
            proxies = self.proxy_get()  #获取代理
        else:
            proxies = self.proxy_save   #继续使用代理
        self.proxy_save = proxies       #更换代理值
        headers_list = [{
                    'Accept': 'text/html, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    'Cookie':'log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469,1533998895,1533998953; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998953; user=MDrAz9H9akQ6Ok5vbmU6NTAwOjQ2OTU0MjIzNDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQyMjM0OjE1MzM5OTkwNzU6OjoxNTMzOTk5MDYwOjg2NDAwOjA6MTZmOGFjOTgwMGNhMjFjZjRkMWZlMjk0NDQ4M2FhNDFkOmRlZmF1bHRfMjox; userid=459542234; u_name=%C0%CF%D1%FDjD; escapename=%25u8001%25u5996jD; ticket=7c92fb758f81dfa4399d0983f7ee5e53; v=Ajz6VIblS6HlDX_9PqmhBV0QDdH4NeBfYtn0Ixa9SCcK4daNPkWw77LpxLZl',
                    'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
                    'Host': 'q.10jqka.com.cn',
                    'Referer': 'http://q.10jqka.com.cn/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                    },{'Accept': 'text/html, */*; q=0.01', 
                    'Accept-Encoding': 'gzip, deflate, sdch', 
                    'Accept-Language': 'zh-CN,zh;q=0.8', 
                    'Connection': 'keep-alive', 
                    'Cookie': 'user=MDq62tH9NUU6Ok5vbmU6NTAwOjQ2OTU0MjA4MDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQyMDgwOjE1MzM5OTg4OTc6OjoxNTMzOTk4ODgwOjg2NDAwOjA6MTEwOTNhMzBkNTAxMWFlOTg0OWM1MzVjODA2NjQyMThmOmRlZmF1bHRfMjox; userid=459542080; u_name=%BA%DA%D1%FD5E; escapename=%25u9ed1%25u59965E; ticket=658289e5730da881ef99b521b65da6af; log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469,1533998895,1533998953; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998953; v=AibgksC3Qd-feBV7t0kbK7PCd5e-B2rBPEueJRDPEskkk8xLeJe60Qzb7jDj', 'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 
                    'Host': 'q.10jqka.com.cn', 
                    'Referer': 'http://q.10jqka.com.cn/', 
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
                    },
                    {'Accept': 'text/html, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive', 'Cookie': 'user=MDq62sm9wM%2FR%2FVk6Ok5vbmU6NTAwOjQ2OTU0MTY4MTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQxNjgxOjE1MzM5OTg0NjI6OjoxNTMzOTk4NDYwOjg2NDAwOjA6MTAwNjE5YWExNjc2NDQ2MGE3ZGYxYjgxNDZlNzY3ODIwOmRlZmF1bHRfMjox; userid=459541681; u_name=%BA%DA%C9%BD%C0%CF%D1%FDY; escapename=%25u9ed1%25u5c71%25u8001%25u5996Y; ticket=4def626a5a60cc1d998231d7730d2947; log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998496; v=AvYwAjBHsS9PCEXLZexL20PSRyfuFzpQjFtutWDf4ll0o5zbyKeKYVzrvsAz', 'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 'Host': 'q.10jqka.com.cn', 'Referer': 'http://q.10jqka.com.cn/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'},
                    {'Accept': 'text/html, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive', 'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361; user=MDq62sm9SnpsOjpOb25lOjUwMDo0Njk1NDE0MTM6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjo6OjQ1OTU0MTQxMzoxNTMzOTk4MjA5Ojo6MTUzMzk5ODE2MDo4NjQwMDowOjFlYTE2YTBjYTU4MGNmYmJlZWJmZWExODQ3ODRjOTAxNDpkZWZhdWx0XzI6MQ%3D%3D; userid=459541413; u_name=%BA%DA%C9%BDJzl; escapename=%25u9ed1%25u5c71Jzl; ticket=b909a4542156f3781a86b8aaefce3007; v=ApheKMKxdxX9FluRdtjNUdGcac08gfwLXuXQj9KJ5FOGbTKxepHMm671oBoh', 'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 'Host': 'q.10jqka.com.cn', 'Referer': 'http://q.10jqka.com.cn/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'},

                    ]

        try:
            time.sleep(random.random()*5)   #设置延时
            headers = random.choice(headers_list)
            r = requests.get(url, headers = headers, proxies=proxies, timeout=4)
        except:
            if num_retries > 0:
                print("重新下载")
                self.proxy_con = 0  #更换代理
                self.downloader(url,num_retries-1)
            else:
                if not self.PAGE_TRACK in self.PAGE_LIST:    #首先应该判断 该页是否存在列表中，如果不存在， 则将其加入其中
                        self.PAGE_LIST.append(self.PAGE_TRACK)   #将获取失败的url保存起来，后面再次循环利用，将元素添加在末尾，
        else:            
            return r.text


    def items_return(self):
        sys.setrecursionlimit(5000)
        count = 0
        while True:
            if self.FLAG < self.MAX_PAGE:
                url_list = self.url_yield()   #获取url
            else:
                url_list = self.url_omi()
                if len(PAGE_LIST) ==0:
                    break
            print("执行到了获取模块")

            for url in url_list:
                html = self.downloader(url)
                #打印提示信息
                print('URL is:', url)
                items = {}   #建立一个空字典，用于信息存储
                try:                      
                    soup = BeautifulSoup(html, 'lxml')
                    for tr in soup.find('tbody').find_all('tr'):
                        td_list = tr.find_all('td')
                        items['代码'] = td_list[1].string
                        items['名称'] = td_list[2].string
                        items['现价'] = td_list[3].string
                        items['涨跌幅'] = td_list[4].string
                        self.writer.writerow(items)
                        print(items)
                        print("保存成功")
                        #如果保存成功，则继续使用代理
                        self.proxy_con = 1
                        #print("解析成功")
                        #yield items          #将结果返回
                except:
                    print("解析失败")
                    #解析失败，则将代理换掉
                    self.proxy_con = 0   
                    #print(html)
                    if not self.PAGE_TRACK in self.PAGE_LIST:
                        self.PAGE_LIST.append(self.PAGE_TRACK)
                    else:
                        count += 1

            if count == 2:
                break


if __name__ == '__main__':
    app = crawl()
    app.items_return()   #打印最后的结果