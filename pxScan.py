from multiprocessing import Process, Pool
import multiprocessing
import glob
from time import ctime
import time
from lib.masterWeb import masterWeb
import lib.parseArgs as parseArgs
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
    print('胖小扫描器v1.0')
    print('[+]本工具扫描主站基础信息和部分特殊路径')
    FileDictDefault = glob.glob('./dict/normal/test.txt')
    arg = parseArgs.parseArgs()
    baseurl = arg.url
    if arg.dict:
        FileDictDefault.append(arg.d)
    if arg.tech:
        xpd = arg.tech.upper()
    masterWeb = masterWeb(baseurl)
    masterWeb.load()
    print('[+]扫描主站: %s'%baseurl)
    if not xpd :
        xpd = masterWeb.xPowerBy
    else:pass
    print('[+]主站部分信息：')
    print('[+]\t状态码[{}]\t\n\tIP地址[{}]\t\n\tTitle [{}]\t\n\tCMS [{}]\t\n\txPowerBy[{}]'.format(masterWeb.status_code, masterWeb.ip, masterWeb.title, masterWeb.cms, xpd))
    print('[+]针对特殊路径开始扫描')
    if 'ASP' in xpd:
        print('[+]ASP 特殊路径加入字典')
        x = glob.glob('./dict/asp/asp.txt')
        FileDictDefault.append(x[0])
    if 'JSP' in xpd:
        print('[+]JSP 特殊路径加入字典')
        x = glob.glob('./dict/jsp/jsp.txt')
        FileDictDefault.append(x[0])
    if 'PHP' in xpd:
        print('[+]PHP 特殊路径加入字典')
        x = glob.glob('./dict/php/phptest.txt')
        FileDictDefault.append(x[0])
    else:pass
    dictCrawl = []
    for file in FileDictDefault:
        with open(file, 'rb') as f:
            ff = f.readlines()
            for one in ff:
                one = one.decode('utf-8', 'ignore')
                dictCrawl.append(one.strip())
    print('[+]特殊路径字典已创建，字典大小为：{}'.format(len(dictCrawl)))
    startTime = time.time()
    print('[+]开始扫描特殊路径 \t %s'% ctime())
    try:
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as exec:
            task = [exec.submit(openUrl, baseurl+uri) for uri in dictCrawl]
            for i in as_completed(task):
                if i.result()[1] == 200 or i.result()[1] == 206:
                    print('[+]' + i.result()[0] + '\t' + str(i.result()[1]))
        endTime = time.time()
        print('[+]用时：{}'.format(endTime-startTime))
    except KeyboardInterrupt as e:
        print('[-]扫描中断！')
        endTime = time.time()
        print('[+]用时：{}'.format(endTime - startTime))
