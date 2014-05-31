#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web
from action.base import base
from setting import *

class show(base):
    def __init__(self):
        base.__init__(self)

    def GET(self):
        if web.ctx.session.login == True:
            self.assign('name', web.ctx.session.uname)
            self.assign('ipaddr', web.ctx.ip)
            self.assign('formhash', web.ctx.session.formhash)
            return self.display('show')
        else:
            web.seeother('/login/')