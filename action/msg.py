#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web, time, re
from action.base import base
from setting import *

class msg(base):
    def __init__(self):
        base.__init__(self)
        if not self.is_login():
            raise web.seeother('/login')

    def GET(self):
        msg = self.__getmsg()
        return self.showJson({
                'num': 0,
                'msg': msg
            })

    def POST(self):
        data = web.input()
        msg = data['msg'].replace('\n', ' ').strip()
        msg = self.htmlspecialchar(msg)
        msg = msg[0: 128]
        uname = web.ctx.session.uname

        # 检查formhash，防止CSRF
        try:
            assert data['formhash'] == web.ctx.session.formhash
        except:
            return self.showJson({
                'num': -1,
                'msg': 'Permission Deny'
            })

        # 处理超链接
        msg = self.__href(msg)

        #插入数据库
        try:
            self.db.query("INSERT INTO `msg`(`msg`, `uname`, `time`) VALUES($m, $u, $t)", vars = {
                'm': msg,
                'u': uname,
                't': int(time.time())
            })
            msg = self.__getmsg()
            return self.showJson({
                'num': 0,
                'msg': msg
            })
        except:
            return self.showJson({
                'num': 1,
                'msg': '发表错误'
            })

    def __href(self, msg):
        (ret, _) = re.subn(r'(https?://[^"\'\s]*)', '<a href="\\1" target="_blank">\\1</a>', msg)
        return ret

    def __getmsg(self):
        begin = 0
        num = 17
        msg = self.db.query("SELECT * FROM `msg` WHERE `time` > $t ORDER BY `time` DESC LIMIT $b, $n", vars = {
            't': web.ctx.session.lasttime,
            'b': begin,
            'n': num
        })
        lst = []
        for l in msg:
            l['time'] = time.strftime("%H:%M:%S", time.gmtime(l['time'] + time_zone * 3600))
            lst.append(l)
        return lst
