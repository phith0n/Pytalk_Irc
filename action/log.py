#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import time
from action.base import base
from setting import *

class log(base):
    def __init__(self):
        base.__init__(self)
        if not self.is_login():
            raise web.seeother('/login')

    def GET(self):
        lasttime = web.ctx.session.lasttime
        nowtime = int(time.time())
        rs = list(self.db.query("SELECT * FROM `msg` WHERE `time` > $lt AND `time` < $nt ORDER BY `time` DESC", vars = {
            'lt': lasttime,
            'nt': nowtime
        }))
        return self.showJson({
            'num': 0,
            'msg': rs
        })