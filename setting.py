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
    '.*', 'show'
)