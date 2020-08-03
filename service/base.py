#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import json
from tornado import web
from tornado.web import HTTPError
from client import mysql, redis
from pycket.session import SessionMixin


class APIError(HTTPError):
    def __init__(self, data):
        super(APIError, self).__init__(status_code=200, reason=json.dumps(data))


class BaseHandler(web.RequestHandler, SessionMixin):

    def send_str(self, json_str):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')

        self.set_status(200)
        self.write(json_str)
        self.finish()

    def send_json(self, data=None, errcode=200, errmsg=''):
        if data is None:
            data = {}
        res = {
            'errcode': errcode,
            'errmsg': errmsg or '请求成功'
        }
        res.update(data)
        self.send_str(json.dumps(res))

    def options(self):
        """预处理过滤"""
        self.send_json()

    def write_error(self, status_code, **kwargs):
        err_object = kwargs['exc_info'][1]
        if isinstance(err_object, APIError):  # 自定义异常
            return self.send_str(err_object.reason)
        super(BaseHandler, self).write_error(status_code, **kwargs)

    def initialize(self):
        mysql.study.close()

    def on_finish(self):
        mysql.study.close()

    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')  # 获取加密的cookie
        # print(current_user)
        # if current_user:
        #     return current_user
        # return None
        # session是一种会话状态，跟数据库的session可能不一样
        return self.session.get('user_info', None)

    def get_real_ip(self):
        req_headers = self.request.headers
        real_ip = ''
        try:
            if 'X-Forwarded-For' in req_headers:
                real_ip = req_headers['X-Forwarded-For']
            if not real_ip and 'X-Real-Ip' in req_headers:
                real_ip = req_headers['X-Real-Ip']
            if not real_ip:
                real_ip = self.request.remote_ip
        except:
            real_ip = ''
        if real_ip.count(',') > 0:
            real_ip = re.sub(',.*', '', real_ip).strip()
        return real_ip


def api_limit(func):
    async def wrap(*args, **kw):
        self = args[0]
        try:
            unionid = self.get_argument('unionid')
        except:
            return self.send_json(errcode=10001, errmsg="参数错误")
        if not redis.rs0.set(f'pay_{unionid}', 1, ex=2, nx=True):
            return self.send_json(errcode=10003, errmsg="操作频繁")
        await func(*args, **kw)
    return wrap
