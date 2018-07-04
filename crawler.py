import requests
from urllib.parse import quote
from settings import *


class crawler(object):
    def __init__(self, MAX_PAGE, PAGE_TRACK, MAX_PROXY, MAX_TRY, MAX_GET, PAGE_LIST, URL_START, PARAMS, PROXY_POOL_API):

        self.MAX_PAGE = MAX_PAGE        #转换为内部变量
        self.PAGE_TRACK                 #跟踪次数
        self.MAX_PROXY = MAX_PROXY      #代理最大次数
        self.MAX_TRY = MAX_TRY          #最大尝试次数
        self.MAX_GET = MAX_GET          #获取次数

        self.PAGE_LIST = PAGE_LIST      #第一次获取失败的 html 的 列表
        self.url_start =  URL_START     #初始链接
        self.PARAMS = PARAMS            #url 构造参数

        self.PROXY_POOL_API = PROXY_POOL_API  


     """
    #代理获取模块

    """
    def proxy_get():
        try:
            r_proxy = requests.get(self.PROXY_POOL_API, timeout = 10)
            return r_proxy.text
        except:
            if self.MAX_PROXY < self.MAX_TRY:
                self.MAX_PROXY += 1
                self.proxy_get()
            else:
                print("超过代理获取重试次数")
        finally:
            self.MAX_PROXY = 1


    def url_yield(self):
        if True:
            for i in range(1, self.MAX_PAGE +1 ):
                self.PAGE_TRACK = i         #页面追踪
                url = "{}{}{}".format(self.URL_START, i, self.PARAMS) 
                yield url
        else:
            self.url_omi()

    def url_omi(self):
        for i in self.PAGE_LIST:
            self.PAGE_TRACK = i 
            url = "{}{}{}".format(self.URL_START, i, self.PARAMS) 
                yield url                                                  #如何构造一个动态的列表，用来存储爬取失败的 url 

    def html_return(self):
        url_list = self.url_yield()   #获取url
        for url in url_list:
            print("执行到了获取模块")
            proxy = self.proxy_get()  #获取代理

            #打印提示信息
            print('URL is', url)
            print('Proxy is ', proxy)

            headers = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Cookie': 'spversion=20130314; __utma=156575163.1163133091.1530233537.1530289428.1530369413.3; __utmz=156575163.1530369413.3.3.utmcsr=stockpage.10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1530444468,1530505958,1530506333,1530516152; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1530516152; historystock=300033%7C*%7C1A0001; v=AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
                'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
                'Host': 'q.10jqka.com.cn',
                'Referer': 'http://q.10jqka.com.cn/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'}

            proxies = {
                "http": 'http://' + proxy,
                "https": 'https://' + proxy,
                }
            try:
                r = requests.get(url, headers = headers, proxies = proxies, timeout = 10) #proxies = proxy
            except:
                if self.MAX_GET < self.MAX_TRY:  
                    print("第",MAX_GET,'次获取重连') 
                    self.MAX_GET += 1
                    html_get(url)
                else:
                    print("获取重连失败")
                    self.PAGE_LIST.append(self.PAGE_TRACK)   #将获取失败的url保存起来，后面再次循环利用
            else:
                if r.status_code == 200:
                    html = r.content

                    
                    #save_to_csv(html)
                    html_parse(html)     #解析信息
                    #return html
                else:
                    print("状态码：", r.status_code)
            finally:
                MAX_GET = MAX_START
                pass
    def items_return(self):
        pass