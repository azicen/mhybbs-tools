import hashlib
import random
import string
import time

from base.http_client import BaseRequest


class RoleInfo(object):
    pass


class IsSignInfo(object):
    pass


class SignInfo(object):
    pass


class MHYClient(object):

    @staticmethod
    def getDigest():
        # v2.3.0-web @povsister & @journey-ad
        n = '9nQiU3AV0rJSIBWgdynfoGMGKaklfbM7'
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        md5 = hashlib.md5()
        return '{},{},{}'.format(i, r, md5.update(('salt=' + n + '&t=' + i + '&r=' + r).encode()))

    # 获取用户角色
    def get_user_game_roles(self, cookie: str) -> list[RoleInfo] | None:
        raise NotImplementedError('Method not implemented!')

    # 获取用户是否签到
    def get_sign_state_info(self, cookie, region: str, uid: int) -> IsSignInfo | None:
        raise NotImplementedError('Method not implemented!')

    def sign(self, cookie: str) -> SignInfo | None:
        raise NotImplementedError('Method not implemented!')
