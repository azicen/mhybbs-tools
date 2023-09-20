import hashlib
import random
import string
import time


class RoleInfo(object):
    pass


class IsSignInfo(object):
    pass


class SignInfo(object):
    pass


class MHYClient(object):

    @staticmethod
    def getDigest():
        n = '9nQiU3AV0rJSIBWgdynfoGMGKaklfbM7'
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        text = 'salt=' + n + '&t=' + i + '&r=' + r
        md5 = hashlib.md5()
        md5.update(text.encode())
        c = md5.hexdigest()
        return '{},{},{}'.format(i, r, c)

    # 获取用户角色
    def get_user_game_roles(self, cookie: str) -> list[RoleInfo]:
        raise NotImplementedError('Method not implemented!')

    # 获取用户是否签到
    def get_sign_state_info(self, cookie, region: str, uid: int) -> IsSignInfo:
        raise NotImplementedError('Method not implemented!')

    def sign(self, cookie: str) -> list[SignInfo]:
        raise NotImplementedError('Method not implemented!')
