#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import time
from action.base import base
from setting import *

class login(base):
    def __init__(self):
        base.__init__(self)

    def POST(self, _ = ''):
        post = web.input()
        name = self.htmlspecialchar(post['name'])
        passwd = self.md5(post['pass'])
        res = self.db.query("SELECT * FROM `user` WHERE `user` = $u", vars = {
            'u': name
        })
        try:
            user = res[0]
            if passwd != user['pass']:
                return self.showJson({
                    'num': 1,
                    'msg': u'账号或密码错误'
                })
            else:
                lasttime = int(time.time())
                self.db.query("UPDATE `user` SET `lasttime` = $t WHERE `uid` = $u", vars = {
                    'u': user['uid'],
                    't': lasttime
                })
                web.ctx.session.login = True
                web.ctx.session.lasttime = lasttime
                web.ctx.session.uname = user['user']
                web.ctx.session.formhash = self.randStr()
                return self.showJson({
                    'num': 0,
                    'msg': u'登录成功'
                })
        except Exception, e:
            # print Exception,":",e
            try:
                res = list(self.db.query("SELECT COUNT(*) AS `cnt` FROM `user` WHERE `ip` = $ip", vars = {
                    'ip': web.ctx.ip
                }))
                if len(res) > 0 and int(res[0]['cnt']) > 10:
                    return self.showJson({
                        'num': 4,
                        'msg': u'同IP注册会员数过多'
                    })
                lasttime = int(time.time())
                res = self.db.query("INSERT INTO `user`(`user`, `pass`, `ip`, `lasttime`) VALUES($u, $p, $ip, $t)", vars = {
                    'u': name,
                    'p': passwd,
                    'ip': web.ctx.ip,
                    't': lasttime
                })
            except Exception, e:
                # print Exception,":",e
                return self.showJson({
                    'num': 2,
                    'msg': u'用户名已被占用'
                })
            if res :
                web.ctx.session.login = True
                web.ctx.session.uname = name
                web.ctx.session.lasttime = lasttime
                web.ctx.session.formhash = self.randStr()
                return self.showJson({
                    'num': 0,
                    'msg': u'注册成功'
                })
            else:
                return self.showJson({
                    'num': 3,
                    'msg': u'未知错误'
                })

    def GET(self, act = '/'):
        if act == '/quit':
            web.ctx.session.login = False
            web.ctx.session.uname = ''
            web.ctx.session.uid = 0
            web.ctx.session.formhash = ''
        return self.display('login')