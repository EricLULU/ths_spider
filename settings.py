#必要参数设置
MAX_PAGE = 165   #最大页数
PAGE_TRACK = 1   #追踪到了第几页
MAX_GET = 1      #获取最大尝试次数
MAX_PARSE = 1    #解析尝试最大次数
MAX_CSV = 1      #文件保存最大次数
MAX_PROXY =1     #获取代理的最大次数
MAX_START = 1    #MAX_*的初始值
MAX_TRY = 4      #最大尝试次数

#初始链接
URL_START = "http://q.10jqka.com.cn//index/index/board/all/field/zdf/order/desc/page/"
PARAMS = "/ajax/1/"


#第一次爬取的 html 缺失的页面 的url 列表
PAGE_LIST = []

#代理池接口
PROXY_POOL_API = "http://127.0.0.1:5555/random"    