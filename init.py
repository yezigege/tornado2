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

STATIC_PATH = os.path.join(sys.path[0], 'static')
TEMPLATE_PATH = os.path.join(sys.path[0], 'template')

options.parse_command_line()

define('port', default=8888, help='run on this port', type=int)
define('debug', default=True, help='enable debug mode')

settings = {
    'xsrf_cookies': False,
    'compress_response': True,
    'debug': options.debug,
    'cookie_secret': base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'tyl').bytes),
}


RuleList = [
    (r'/', service.index.web.IndexHandler),
]

if __name__ == "__main__":
    application = tornado.web.Application(RuleList, **settings)
    application.listen(options.port)
    print(f"Running on port {options.port}")
    tornado.ioloop.IOLoop.instance().start()