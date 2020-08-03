#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import os
import sys
import uuid

import tornado.ioloop
import tornado.web
from tornado.options import options, define

import service.index.web
import service.auth.web
from lib import uimodules, uimethods

STATIC_PATH = os.path.join(sys.path[0], 'static')
TEMPLATE_PATH = os.path.join(sys.path[0], 'template')

options.parse_command_line()

define('port', default=8888, help='run on this port', type=int)
define('debug', default=True, help='enable debug mode')

settings = {
    'login_url': '/login',
    'static_path': STATIC_PATH,  # 静态文件路径
    'template_path': TEMPLATE_PATH,
    'autoreload': True,
    'xsrf_cookies': False,
    'compress_response': True,
    'debug': options.debug,
    'ui_modules': uimodules,
    'ui_methods': uimethods,
    'cookie_secret': base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'tyl').bytes),
    'pycket': {  # 固定写法packet，用于保存用户登录信息
        'engine': 'redis',
        'storage': {
            'host': 'localhost',
            'port': 6379,
            'db_sessions': 5,
            'db_notifications': 11,
            'max_connections': 2 ** 33,
        },
        'cookie': {
            'expires_days': 38,
            'max_age': 100
        }
    }
}


RuleList = [
    (r'/', service.index.web.IndexHandler),
    (r'/login', service.auth.web.LoginHandler),
]

if __name__ == "__main__":
    application = tornado.web.Application(RuleList, **settings)
    application.listen(options.port)
    print(f"Running on port {options.port}")
    tornado.ioloop.IOLoop.instance().start()