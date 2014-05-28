#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'

# 数据库
database = 'db/pytalk.db3'

# 网址，为空时自动获取
root_site = ""

# url规则，请勿随便修改，详见文档
urls = (
    '/msg/?', 'msg',
    '/login(/quit|/)?', 'login',
    '/log/?', 'log',
    '/file/?', 'upload',
    '.*', 'show'
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