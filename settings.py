#!/usr/bin/env python
# -*- coding: utf-8 -*-

MYSQL = {
    'study': {
        'master': {
            'host': '127.0.0.1',
            'user': 'root',
            'passwd': 'mysql',
            'port': 3306,
            'db': 'study'
        },
        # 'slave': {
        #     'host': '127.0.0.1',
        #     'user': 'ktvsky',
        #     'passwd': '098f6bcd4621d373cade4e832627b4f6',
        #     'port': 3308,
        #     'db': 'gzh'
        # }
    },
    # 'myktv': {
    #     'master': {
    #         'host': '127.0.0.1',
    #         'user': 'ktvsky',
    #         'passwd': '098f6bcd4621d373cade4e832627b4f6',
    #         'port': 3306,
    #         'db': 'myktv'
    #     },
    #     'slave': {
    #         'host': '127.0.0.1',
    #         'user': 'ktvsky',
    #         'passwd': '098f6bcd4621d373cade4e832627b4f6',
    #         'port': 3308,
    #         'db': 'myktv'
    #     }
    # }
}

REDIS = {
    'rs0': {'host': '127.0.0.1', 'port': 6379, 'db': 0},
    'rs1': {'host': '127.0.0.1', 'port': 6379, 'db': 1},
}

A_HOUR = 3600
HOUR6 = 6 * A_HOUR
HOUR3 = 3 * A_HOUR
A_DAY = 24 * A_HOUR

# try:
#     from tornado.options import options
#     import logging
#     if options.debug:
#         exec(compile(open('settings_debug.py').read(), 'settings_debug.py', 'exec'))
# except Exception as e:
#     logging.error(e)
