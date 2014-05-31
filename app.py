#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web
from setting import *

if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.debug = debug
    web.config.session_parameters['cookie_name'] = 'py_pytalk_sid'
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['timeout'] = pytalk_cookie['save_cookie_seconds'],
    web.config.session_parameters['ignore_change_ip'] = True
    web.config.session_parameters['secret_key'] = pytalk_cookie['secret_key']
    web.config.session_parameters['expired_message'] = 'Session expired'
    session = web.session.Session(app, web.session.DiskStore('data/sessions'), initializer={'login': False})
    def session_hook():
        web.ctx.session = session
    app.add_processor(web.loadhook(session_hook))
    app.run()