from urllib.parse import urlparse
import socket
import json
# from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import as_completed
# import requests
# URLS = [['http://httpbin.org','1'], ['http://example.com/','2'], ['https://api.github.com/', '3']]
# def load_url(url,code):
#     print(code)
#     return url, requests.get(url).status_code
#
#
# with ThreadPoolExecutor(max_workers=3) as executor:
#     tasks = [executor.submit(load_url, url, code) for (url, code) in URLS]
#     for future in as_completed(tasks):
#         print(future.result())
import glob
x = glob.glob('./pxScan.py')

print(type(x[0]))