import tornado.httpserver
import tornado.web
from pymemcache.client import base
import uuid

class CacheHandler():
    @staticmethod
    def get_cache_client():
        client = base.Client(('localhost', 11211))
        return client

    @staticmethod
    def remove_encode_format(object):
        return str(object).replace("b'", "")[:-1]

    def set_cache(self, requestHandler, username):
        cacheClient = self.get_cache_client()
        newUuid = str(uuid.uuid4())
        requestHandler.set_cookie(username, newUuid)
        cacheClient.set(username, newUuid)

    def get_cache(self, requestHandler, currentUser):
        username = self.remove_encode_format(currentUser)
        if username in requestHandler.cookies:
            cacheClient = self.get_cache_client()
            cachedCookie = cacheClient.get(username)
            cachedCookieStr = self.remove_encode_format(cachedCookie)
            currentCookie = requestHandler.cookies[username].value
            if(currentCookie == cachedCookieStr):
                print('Logged in')
                return currentUser
            else:
                print('Logging out')
                requestHandler.clear_cookie("user")
                requestHandler.clear_cookie(username)
        return None
