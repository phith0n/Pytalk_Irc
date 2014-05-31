#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web

# 数据库
database = 'db/pytalk.db3'
db = web.database(dbn = 'sqlite', db = database)

# 网址，为空时自动获取
root_site = ""

# url规则，请勿随便修改，详见文档
urls = (
    '/msg/?', 'action.msg.msg',
    '/login(/quit|/)?', 'action.login.login',
    '/log/?', 'action.log.log',
    '/file/?', 'action.upload.upload',
    '.*', 'action.show.show'
)

# 时区
time_zone = 8

# cookie设置
pytalk_cookie = {
    'save_cookie_seconds': 86400,
    'secret_key': 'kOlai1jnXPMj9k1i6xT'
}

# 上传文件夹
upload_dir = 'upfile'

# 上传文件最大尺寸
upload_max_size = 1 * 1024 * 1024

# debug模式
debug = False