from concurrent.futures import ThreadPoolExecutor
import requests
import re
import hashlib
from concurrent.futures import as_completed
from config import CMSDATA
import json
def getCMS(url, path, rep, name, hash):
    result = ''
    try:
        req = requests.get(url + path)
        if req.status_code == 200:
            if re.search(rep, req.text, re.I) or hashlib.md5(req.content).hexdigest() == hash:
                result.add(str(name))
    except:
        pass

def cmsDiscover(url):#url, path, rep, name, hash
    cmsFileBuf = json.loads(CMSDATA)
    cmsDict = cmsFileBuf.read()
    result = []
    with ThreadPoolExecutor() as exec:
        tasks = [exec.submit(getCMS, url, one['url'], one['re'], one['name'], one['md5'])for one in cmsDict]
        for furture in as_completed(tasks):
            result.append(furture.result())
            #return future
    return result