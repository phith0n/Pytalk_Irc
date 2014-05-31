#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import random, json, string
from setting import *
from hashlib import md5

class base:
    def __init__(self):
        self.db = ""
        self.tplData = {}
        self.globalsTplFuncs = {}
        self.initCommonTplFunc()
        self.db = db
        if "" == root_site:
            self.root_site = "%s://%s/" % (web.ctx.protocol, web.ctx.host)
        else:
            self.root_site = root_site
        self.assign('root', self.root_site)
        self.assign('static', self.root_site + 'static')

    def initCommonTplFunc(self):
        subStr = lambda strings,offset,length : self.subText(strings,offset,length)
        self.assignTplFunc({'subStr':subStr})

    def assignTplFunc(self,funcs):
        self.globalsTplFuncs = dict(self.globalsTplFuncs,**funcs)

    def is_login(self):
        return hasattr(web.ctx.session, 'login') and web.ctx.session.login == True

    def md5(self, str):
        m = md5()
        m.update(str)
        return m.hexdigest()

    def safechar(self, txt):
        return txt.replace("<", "").replace(">", "")\
            .replace("&", "").replace('"', "")\
            .replace("'", "")

    def htmlspecialchar(self, txt):
        return txt.replace("<", "&lt;").replace(">", "&gt;")\
            .replace('"', "&quot;").replace("'", "&#039;")

    def randStr(self, len = 8):
        return ''.join(random.sample(string.ascii_letters + string.digits, len))

    def subText(self,strings,offset,length):
        return self.strip_tags(strings)[offset:length]

    def strip_tags(self,html):
        from HTMLParser import HTMLParser
        html = html.strip()
        html = html.strip("\n")
        result = []
        parse = HTMLParser()
        parse.handle_data = result.append
        parse.feed(html)
        parse.close()
        return "".join(result)

    def showJson(self, data):
        j = json.dumps(data)
        return j

    def assign(self,key,value = ''):
        if type(key) == dict:
            self.tplData = dict(self.tplData,**key)
        else:
            self.tplData[key] = value

    def display(self, tplName):
        self.tplData['render'] = web.template.render('templates', globals = self.globalsTplFuncs)
        return getattr(self.tplData['render'], tplName)(self.tplData)