#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web, json, time
from hashlib import md5

# 数据库
database = 'db/irc.db3'
db = web.database(dbn='sqlite', db='db/oicq.db3')
# 路径
root_site = 'http://localhost:81/'

urls = (
    '/msg/?', 'msg',
    '/login(/quit|/)?', 'login',
    '/log/?', 'log',
    '.*', 'show'
)

class base:
    def __init__(self):
        self.tplData = {}
        self.globalsTplFuncs = {}
        self.initCommonTplFunc()
        self.assign('root', root_site)
        self.assign('static', root_site + 'static')

    def initCommonTplFunc(self):
        subStr=lambda strings,offset,length : self.subText(strings,offset,length)
        self.assignTplFunc({'subStr':subStr})

    def assignTplFunc(self,funcs):
        self.globalsTplFuncs = dict(self.globalsTplFuncs,**funcs)

    def is_login(self):
        return hasattr(web.ctx.session, 'login') and web.ctx.session.login == True

    def md5(self, str):
        m = md5()
        m.update(str)
        return m.hexdigest()

    def htmlspecialchars(self, txt):
        return txt.replace("<", "&lt;").replace(">", "&gt;")\
            .replace("&", "&amp;").replace('"', "&quot;")\
            .replace("'", "&#39;")

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

    def display(self,tplName):
        self.tplData['render'] = web.template.render('templates',globals=self.globalsTplFuncs)
        return getattr(self.tplData['render'], tplName)(self.tplData)

class log(base):
    def __init__(self):
        base.__init__(self)
        if not self.is_login():
            raise web.seeother('../login')

    def GET(self):
        lasttime = web.ctx.session.lasttime
        nowtime = int(time.time())
        rs = db.query("SELECT * FROM `msg` WHERE `time` > $lt AND `time` < $nt ORDER BY `time` DESC", vars = {
            'lt': lasttime,
            'nt': nowtime
        })
        return self.showJson({
            'num': 0,
            'msg': [l for l in rs]
        })

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
        uname = web.ctx.session.uname
        try:
            db.query("INSERT INTO `msg`(`msg`, `uname`, `time`) VALUES($m, $u, $t)", vars = {
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

    def __getmsg(self):
        begin = 0
        num = 17
        msg = db.query("SELECT * FROM `msg` WHERE `time` > $t ORDER BY `time` DESC LIMIT $b, $n", vars = {
            't': web.ctx.session.lasttime,
            'b': begin,
            'n': num
        })
        lst = []
        for l in msg:
            l['time'] = time.strftime("%H:%M:%S", time.gmtime(l['time'] + 28800))
            lst.append(l)
        return lst


class login(base):
    def __init__(self):
        base.__init__(self)

    def POST(self, _ = ''):
        post = web.input()
        name = post['name']
        passwd = self.md5(post['pass'])
        res = db.query("SELECT * FROM `user` WHERE `user` = $u AND 1=1", vars = {
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
                db.query("UPDATE `user` SET `lasttime` = $t WHERE `uid` = $u", vars = {
                    'u': user['uid'],
                    't': lasttime
                })
                web.ctx.session.login = True
                web.ctx.session.lasttime = lasttime
                web.ctx.session.uname = user['user']
                return self.showJson({
                    'num': 0,
                    'msg': u'登录成功'
                })
        except Exception, e:
            # print Exception,":",e
            try:
                res = list(db.query("SELECT COUNT(*) AS `cnt` FROM `user` WHERE `ip` = $ip", vars = {
                    'ip': web.ctx.ip
                }))
                if len(res) > 0 and int(res[0]['cnt']) > 10:
                    return self.showJson({
                        'num': 4,
                        'msg': u'同IP注册会员数过多'
                    })
                lasttime = int(time.time())
                res = db.query("INSERT INTO `user`(`user`, `pass`, `ip`, `lasttime`) VALUES($u, $p, $ip, $t)", vars = {
                    'u': name,
                    'p': passwd,
                    'ip': web.ctx.ip,
                    't': lasttime
                })
            except Exception, e:
                print Exception,":",e
                return self.showJson({
                    'num': 2,
                    'msg': u'用户名已被占用'
                })
            if res :
                web.ctx.session.login = True
                web.ctx.session.uname = name
                web.ctx.session.lasttime = lasttime
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
        return self.display('login')

class show(base):
    def __init__(self):
        base.__init__(self)

    def GET(self):
        if web.ctx.session.login == True:
            self.assign('name', web.ctx.session.uname)
            self.assign('ipaddr', web.ctx.ip)
            return self.display('show')
        else:
            web.seeother('/login/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.session_parameters['cookie_name'] = 'py_pytalk_sid'
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['timeout'] = 86400,
    web.config.session_parameters['ignore_expiry'] = True
    web.config.session_parameters['ignore_change_ip'] = True
    web.config.session_parameters['secret_key'] = 'kO9ai2jNXxMjSk1i6xT'
    web.config.session_parameters['expired_message'] = 'Session expired'
    session = web.session.Session(app, web.session.DiskStore('data/sessions'), initializer={'login': False})
    def session_hook():
        web.ctx.session = session
    app.add_processor(web.loadhook(session_hook))
    app.run()