import json
import urllib
import requests
import logging as log
from configs import userConfig


class HttpRequest:
    @staticmethod
    def toPython(data):
        return json.loads(data)

    @staticmethod
    def toJson(data, indent=None, ensure_ascii=True):
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

    def sendRequest(self, method, url, maxRetry: int = 2,
                    params=None, data=None, json=None, headers=None, **kwargs):
        for i in range(maxRetry + 1):
            try:
                session = requests.Session()
                result = session.request(method=method, url=url,
                                         params=params, data=data, headers=headers, **kwargs)
            except urllib.error.HTTPError as e:
                log.error(f'Http error:{e}')
                log.error(f'Request {i + 1} failed, retrying...')
            except KeyError as e:
                log.error(f'Response error:{e}')
                log.error(f'Request {i + 1} failed, retrying...')
            except Exception as e:
                log.error(f'Unknown error:{e}')
                log.error(f'Request {i + 1} failed, retrying...')
            else:
                return result
        log.error(f'Http request failed...')


req = HttpRequest()


class BaseRequest(object):
    def __init__(self, cookies: str = None):
        if not isinstance(cookies, str):
            log.error("Type Error: %s want a %s but got a %s"
                      .format(self.__class__, type(__name__), type(cookies)))
            return
        self._cookies = cookies

    def getHeader(self):
        header = {
            'User-Agent': userConfig.USER_AGENT,
            'Referer': userConfig.REFERER_URL,
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': self._cookies
        }
        return header
