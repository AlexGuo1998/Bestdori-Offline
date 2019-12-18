# -*- encoding:utf-8 -*-
# ==============================================
# Author:      AlexGuo1998
# Description: Manage resources, with ETag and last-modified support
# Date:        2019/12/16
# ==============================================

import os
import time
import requests
import pickle
import typing


class CacheControl:
    def __init__(self):
        self.path = ''
        self.lastRead = 0  # for resource cleaning
        self.lastCheck = 0
        self.staleTs = 0  # for updating
        self.lastModified = 0
        self.etag = None

    def touchAndTestStale(self):
        t = int(time.time())
        self.lastRead = t
        return t >= self.staleTs


class RequestManager:
    def __init__(self, cacheIndex, cacheDir):
        self.cacheIndex = cacheIndex
        self.cacheDir = cacheDir
        if not (self.cacheDir.endswith('/') or self.cacheDir.endswith('\\')):
            self.cacheDir += '/'
        os.makedirs(self.cacheDir, exist_ok=True)
        data = {}
        try:
            with open(self.cacheIndex, 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            pass
        self.session = data.get('session')
        if not self.session:
            self.session = requests.Session()
        self.cacheControl: typing.Dict[str, CacheControl] = data.get('cache-control', {})
        self.cacheControlLock = None  # TODO

    def get(self, path, cacheable=True, session=False, force=False):
        resourceName = self._pathToResourceName(path)
        if cacheable and not force:
            cacheControl = self.cacheControl.get(resourceName)
            if cacheControl is not None and cacheControl.path == path:
                stale = cacheControl.touchAndTestStale()
                print(stale)  # TODO
                filename = self.cacheDir + resourceName
                try:
                    with open(filename, 'rb') as f:
                        content = f.read()
                    return content
                except:
                    pass
        # cache miss, read the content, update cache
        if session:
            r = self.session.get(path)
        else:
            r = requests.get(path)
        content = r.content
        if cacheable:
            # TODO parse header
            # r.headers
            filename = self.cacheDir + resourceName
            with open(filename, 'wb') as f:
                f.write(content)
            cacheControl = CacheControl()
            cacheControl.path = path
            self.cacheControl[resourceName] = cacheControl
        return content

        pass

    @staticmethod
    def _pathToResourceName(path: str):
        o = ''
        if path.startswith('http://'):
            path = path[7:]
        elif path.startswith('https://'):
            path = path[8:]
            o = 's@'
        o += path.replace('/', '@')
        return o

    def saveCacheIndex(self):
        data = {
            'session': self.session,
            'cache-control': self.cacheControl,
        }
        with open(self.cacheIndex, 'wb') as f:
            pickle.dump(data, f)

_manager = None


def getManager() -> RequestManager:
    global _manager
    if _manager is None:
        _manager = RequestManager('cache-index.pickle', 'cache/')
    return _manager
