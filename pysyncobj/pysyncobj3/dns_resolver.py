#
#  WARNING: this is generated file, use gen_py3.sh to update it.
#
import time
import socket
import random
from .debug_utils import LOG_WARNING


class DnsCachingResolver(object):
    def __init__(self, cacheTime, failCacheTime):
        self.__cache = {}
        self.__cacheTime = cacheTime
        self.__failCacheTime = failCacheTime

    def setTimeouts(self, cacheTime, failCacheTime):
        self.__cacheTime = cacheTime
        self.__failCacheTime = failCacheTime

    def resolve(self, hostname):
        currTime = time.time()
        cachedTime, ips = self.__cache.get(hostname, (0, []))
        timePassed = currTime - cachedTime
        if (timePassed > self.__cacheTime) or (not ips and timePassed > self.__failCacheTime):
            prevIps = ips
            ips = self.__doResolve(hostname)
            if not ips:
                ips = prevIps
            self.__cache[hostname] = (currTime, ips)
        return None if not ips else random.choice(ips)

    def __doResolve(self, hostname):
        try:
            ips = socket.gethostbyname_ex(hostname)[2]
        except socket.gaierror:
            LOG_WARNING('failed to resolve host %s' % hostname)
            ips = []
        return ips

_g_resolver = None
def globalDnsResolver():
    global _g_resolver
    if _g_resolver is None:
        _g_resolver = DnsCachingResolver(cacheTime=600.0, failCacheTime=30.0)
    return _g_resolver
