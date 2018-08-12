#必要参数设置
MAX_PAGE = 165   #最大页数
PAGE_TRACK = 1   #追踪到了第几页
MAX_GET = 1      #获取最大尝试次数
MAX_PARSE = 1    #解析尝试最大次数
MAX_CSV = 1      #文件保存最大次数
MAX_PROXY =1     #获取代理的最大次数
MAX_START = 1    #MAX_*的初始值
MAX_TRY = 4      #最大尝试次数
FLAG = 0         #用于标识，是否使用 url_omi() 函数

#初始链接
URL_START = "http://q.10jqka.com.cn//index/index/board/all/field/zdf/order/desc/page/"
PARAMS = "/ajax/1/"


#第一次爬取的 html 缺失的页面 的url 列表
#先进先出的列表
PAGE_LIST = [] 

#代理池接口
PROXY_POOL_API = "http://127.0.0.1:5555/random"  

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

#数据库部分
MONGO_URL = ''