#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import settings

rs0 = redis.StrictRedis(**settings.REDIS['rs0'])
rs1 = redis.StrictRedis(**settings.REDIS['rs1'])

