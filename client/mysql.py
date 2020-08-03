#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column
from functools import partial
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.mysql import TIMESTAMP, DATETIME
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper
import logging
import settings

NotNullColumn = partial(Column, nullable=False, server_default='')


def model2dict(model):
    if not model:
        return {}
    fields = class_mapper(model.__class__).columns.keys()
    return dict((col, getattr(model, col)) for col in fields)


def model_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return model2dict(ret)
    return wrap


def models_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [model2dict(r) for r in ret]
    return wrap


def tuples_first_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [item[0] for item in ret]
    return wrap


class declare_base(object):

    create_time = NotNullColumn(DATETIME)
    update_time = NotNullColumn(TIMESTAMP, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')

    @declared_attr
    def __table_args__(cls):
        return {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8'
        }


Base = declarative_base(cls=declare_base)

CONF = {
    'kwargs': {
        'pool_recycle': 3600,
        # 'echo': options.debug,
        # 'echo_pool': options.debug
    },
    'schema': 'mysql://%s:%s@%s:%d/%s?charset=utf8'
}


def create_session(user, passwd, host, port, db):
    schema = CONF['schema'] % (user, passwd, host, port, db)
    logging.info(schema)
    engine = create_engine(schema, **CONF['kwargs'])
    session = scoped_session(sessionmaker(bind=engine))
    return session()


class BaseMysql(object):

    def __init__(self, db):
        self.master = create_session(**db['master'])
        # self.slave = create_session(**db['slave'])

    def close(self):
        self.master.commit()
        self.master.close()
        # self.slave.commit()
        # self.slave.close()

    def add(self, one):
        self.master.add(one)
        self.master.commit()
        return one


study = BaseMysql(settings.MYSQL['study'])

