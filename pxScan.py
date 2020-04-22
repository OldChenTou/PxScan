from multiprocessing import Process, Pool
import multiprocessing
import glob
from lib.masterWeb import masterWeb
import lib.argParse as argParse
import concurrent.futures
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED, as_completed
import time, os
#胖小scan 业务逻辑，扫描主站，获得基本信息，针对字典库的特殊路径进行爬取，字典库暂时只分：默认，jsp，php，aspx。高并发访问采用"异步，多进程"，接受参数：url
TIMEOUT = 10

USER_AGENT = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT, 'Connection': 'Keep-Alive', 'Range': 'bytes=0-102400'}

def openUrl(url):
    res = requests.get(
        url=url,
        allow_redirects=False,
        timeout=TIMEOUT,
        headers=HEADERS,
        verify=False
    )
    return url, res.status_code

# def asyncTask(task):#task为数组
#     with ProcessPoolExecutor() as executor:
#         for f in as_completed(task):


if __name__ == '__main__':
    #初始化部分,取url，解析url
    FileDictDefault = glob.glob('./dict/normal/*.txt')
    arg = argParse()
    baseurl = arg.u
    if arg.d:
        FileDictDefault.append(arg.d)
    masterWeb = masterWeb(baseurl)
    print
    xpd = masterWeb.xPowerBy
    if 'ASP' in xpd:
        x = glob.glob('./dict/asp/asp.txt')
        FileDictDefault.append(x[0])
    if 'JSP' in xpd:
        x = glob.glob('./dict/asp/jsp.txt')
        FileDictDefault.append(x[0])
    if 'PHP' in xpd:
        x = glob.glob('./dict/asp/php.txt')
        FileDictDefault.append(x[0])
    else:pass
    dictCrawl = []
    for file in FileDictDefault:
        with open(file, 'r') as f:
            ff = f.readlines()
            for one in ff:
                dictCrawl.append(one.strip())
    print('[+]特殊路径字典已创建，字典大小为：{}'.format(type(dictCrawl)))
    with ProcessPoolExecutor as exec:
        task = [exec.submit(openUrl, baseurl+uri) for uri in dictCrawl]
        for i in as_completed(task):
            print(i.result())

    pool =Pool(multiprocessing.cpu_count())
    print('scan begin')
    for i in range(10):
        pool.apply_async(func, args=(i,),callback=P)
