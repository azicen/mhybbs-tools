import json
import logging
import aiohttp
from base import constant

logger = logging.getLogger(__name__)


class HttpRequest:
    @staticmethod
    def toPython(data):
        return json.loads(data)

    @staticmethod
    def toJson(data, indent=None, ensure_ascii=True):
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

    async def sendRequest(
        self,
        method,
        url,
        maxRetry: int = 2,
        params=None,
        data=None,
        json=None,
        headers=None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        for i in range(maxRetry + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        headers=headers,
                        **kwargs,
                    )
            except Exception as e:
                logger.error(f"Unknown error:{e}")
                logger.error(f"Request {i + 1} failed, retrying...")
            else:
                return response
        logger.error(f"Http request failed...")


req = HttpRequest()


class BaseRequest(object):
    def __init__(self, cookies: str = None):
        if not isinstance(cookies, str):
            logger.error(
                f"Type Error: {self.__class__} want a {type(__name__)} but got a {type(cookies)}"
            )
            return
        self._cookies = cookies

    def getHeader(self):
        header = {
            "Origin": constant.Origin_URL,
            "User-Agent": constant.USER_AGENT,
            "Referer": constant.REFERER_URL,
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": self._cookies,
        }
        return header
