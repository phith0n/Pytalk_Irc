#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web, time, random
from action.base import base
from setting import *

class upload(base):
    def __init__(self):
        base.__init__(self)
        if not self.is_login():
            raise web.seeother('/login')

    def __rename(self, ext):
        return "%d_%d%s" % (time.time(), random.randint(0, 65535), ext)

    def POST(self):
        import os, cgi
        cgi.maxlen = upload_max_size
        try:
            data = web.input(upfile = {})
        except:
            return self.showJson({
                'num': 2,
                'msg': '文件最大不超过%sK' % int(upload_max_size / 1024)
            })
        if 'upfile' in data:
            # 处理上传文件
            filename = self.safechar(data['upfile'].filename[0: 256])
            (_, onlyname) = os.path.split(filename)
            (_, ext) = os.path.splitext(filename)
            filename = u'static/%s/%s' % (upload_dir, self.__rename(ext))
            with open(filename, 'wb') as fout:
                fout.write(data['upfile'].file.read())

            # 作为新消息插入数据库
            filename = self.root_site + filename
            if ext in ('.jpg', '.gif', '.png', '.bmp'):
                msg = u'分享了 <a class="fancybox" href="javascript:;" ' \
                      u'title="%s" onclick="return showimg(this);">图片-%s</a>' % (filename, onlyname.decode('utf8'))
            elif ext in ('.rar', '.zip', '.tar', '.gz', '.doc', '.pdf', '.exe', '.wps', '.txt', '.xls'):
                msg = u'<span>分享了文件 <a href="%s" target="_blank">%s</a></span>' % (filename, onlyname.decode('utf8'))
            else:
                return self.showJson({
                    'num': 4,
                    'msg': '非法文件格式'
                })
            uname = web.ctx.session.uname
            try:
                self.db.query("INSERT INTO `msg`(`msg`, `uname`, `time`) VALUES($m, $u, $t)", vars = {
                    'm': msg,
                    'u': uname,
                    't': int(time.time())
                })
                return self.showJson({
                    'num': 0,
                    'msg': "上传成功",
                    'dir': filename
                })
            except:
                return self.showJson({
                    'num': 3,
                    'msg': '发送文件失败'
                })
        else:
            return self.showJson({
                'num': 1,
                'msg': '没有选择要上传的文件'
            })