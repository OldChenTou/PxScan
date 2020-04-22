import requests
import re
import socket
import json

from lib.cmsDiscover import cmsDiscover
class masterWeb(object):
    def __init__(self, url, parser, proxy={}, timeout=10, load=True):
        self.proxy = proxy
        self.timeout = timeout
        self.url = url
        self.parser = parser
        self.scheme = parser.scheme #https
        self.netloc = parser.netloc #www.baidu.com
        self.path = parser.path   #www.baidu.com
        self.domain = ''
        if re.search('a-z',self.netloc, re.I):
            self.domain = self.netloc.split(':')[0]
        self.ip = self.gethostbyname(self.netloc.split(':')[0])
        try:
            self.port = self.netloc.split(':')[1]
        except:
            self.port = 443 if self.scheme.upper() == 'HTTPS' else 80
        self.status_code= 0
        self._content   = set() #struts2 dedecms ...
        self.headers    = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '}

        self.server     = '|' #Server: nginx/1.8.0 #Apache Tomcat/7.0.59
        self.xPowerBy = '|' #X-Powered-By: PHP/5.6.31'
        self.title      = ''
        self.cms     = ''
        if load:
            try:
                self.pag404 = self.getpag404()
                self.load()
            except:
                pass

    def getpag404(self):
        try:
            url = self.url + "/7xs12rna9sdj1nsdaux.%s"%self.host
            return requests.get(
                url,
                allow_redirects=True,
                headers=self.headers,
                proxies=self.proxy,
                timeout=self.timeout,
                verify=False)
        except:
            pass
#load部分获取title xpower， cms 获取分两个部分 300 200 先不允许重定向（此处很细，值得学习）。
    def load(self):
        res = requests.get(
                self.url,
                allow_redirects=False,
                headers=self.headers,
                #proxies=self.proxy,
                timeout=self.timeout,
                verify=False)
        self.headers = res.headers
        self.server = res.headers.get('Server',self.server)
        xPowerBy1 = res.headers.get('X-Powered-By','')
        xPowerBy2 = self.findXPowerBby(res)
        self.xPowerBy = xPowerBy2+'|'+self.xPowerBy if xPowerBy2 else xPowerBy1
        res = requests.get(
                self.url,
                #proxies=self.proxy,
                #timeout=self.timeout,
                verify=False)
        self.status_code = res.status_code
        self.title = ''.join(
                    re.findall(r"<title>([\s\S]*?)</title>",
                    res.text.encode(res.encoding).decode('utf-8'),
                    re.I))
        self.server = res.headers.get('Server',self.server)
        xPowerBy3 = res.headers.get('X-Powered-By',self.xPowerBy)
        xPowerBy4 = self.findXPowerBby(res)
        self.xPowerBy = xPowerBy4 + '|' + self.xPowerBy if xPowerBy4 else xPowerBy3+'|'+self.xPowerBy

        if 'JSP' in self.xPowerBy:
            server = self.findJavaServer(self.scheme, self.netloc)
            self.server = server + '|' + self.server if server else res.headers.get('Server')

        self.cms = '|'.join(cmsDiscover(self.url))

    def findXPowerBby(res):
        xPowerBy = ' '
        headers = str(res.headers)
        content = res.text
        if 'ASP.NET' in headers or 'ASPSESSIONID' in headers:
            xPowerBy += '|ASP'
        if 'PHPSESSIONID' in headers:
            xPowerBy += '|PHP'
        if 'JSESSIONID' in headers:
            xPowerBy += '|JSP'
        if re.search(r'name="__VIEWSTATE" id="__VIEWSTATE"',content):
            xPowerBy += '|ASP'
        if re.search(r'''href[\s]*=[\s]*['"][./a-z0-9]*\.jsp[x'"]''',content,re.I):
            xPowerBy += 'JSP'
        if re.search(r'''href[\s]*=[\s]*['"][./a-z0-9]*\.action['"]''',content,re.I):
            xPowerBy += 'JSP'
        if re.search(r'''href[\s]*=[\s]*['"][./a-z0-9]*\.do['"]''',content,re.I):
            xPowerBy += 'JSP'
        if re.search(r'''href[\s]*=[\s]*['"][./a-z0-9]*\.asp[x'"]''',content,re.I):
           xPowerBy += 'ASP'
        if re.search(r'''href[\s]*=[\s]*['"][./a-z0-9]*\.php[\?'"]''',content,re.I):
           xPowerBy += 'PHP'
        return xPowerBy

    def gethostbyname(hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return hostname

    def findJavaServer(self, scheme,netloc):
        server = ' '
        try:
            res = self.pag404
            tomcat = ''.join(re.findall("<h3>(.*?)</h3>",res.text))
            weblogic = ''.join(re.findall("<H4>(.*?)404 Not Found</H4>",res.text))
            if res.status_code == 404:
                if 'Tomcat' in res.text:
                    server = tomcat
                if 'Hypertext' in res.text:
                    server = 'Weblogic '+weblogic
        except:pass
        return server

    # def content(self):
    #     for s in self.server.split('|') + self.xpoweredby.split('|'):
    #         if s:self._content.add(s.strip())
    #     if self.cmsver:
    #         self._content.add(self.cmsver.strip())
    #     return '|'.join(self._content).lower()
    #
    # @content.setter
    # def content(self,value):
    #     self._content.add(value)



