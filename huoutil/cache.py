#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json
import redis
import logging


class RedisCache(object):
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        try:
            _cache = redis.StrictRedis(
                host=self.host, port=self.port, db=self.db)
        except:
            logging.warning('Connect redis failed. The cache will not work')
            return None
        self._cache = _cache
        self._key_sep = '\x01'
        self._expire = None

    def set_key_sep(self, sep):
        self._key_sep = sep

    def set_expire(self, time):
        self._expire = time

    def _wrap_key(
            self,
            k,
    ):
        if isinstance(k, (list, tuple)):
            return self._key_sep.join(k)
        else:
            return k

    def get(self, k):
        k = self._wrap_key(k)
        return self._cache.get(k)

    def set(self, k, v, ex=None):
        k = self._wrap_key(k)
        if ex is None:
            ex = self._expire
        return self._cache.set(k, v, ex=ex)

    def get_list(self, k, sep='\x01'):
        k = self._wrap_key(k)
        return sep.split(self._cache.get(k))

    def set_list(self, k, v, sep='\x01', ex=None):
        k = self._wrap_key(k)
        if v is None:
            nv = None
        else:
            nv = sep.join(v)
        if ex is None:
            ex = self._expire
        return self._cache.set(k, nv, ex=ex)

    def get_json(self, k):
        k = self._wrap_key(k)
        jsn_str = self._cache.get(k)
        if jsn_str is None:
            return None
        else:
            return json.loads(jsn_str)

    def set_json(self, k, v, ex=None):
        k = self._wrap_key(k)
        if v is None:
            nv = None
        else:
            nv = json.dumps(v, ensure_ascii=False)
        if ex is None:
            ex = self._expire
        return self._cache.set(k, nv, ex=ex)