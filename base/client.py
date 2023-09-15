from base.http_client import BaseRequest


class RoleInfo(object):
    pass


class IsSignInfo(object):
    pass


class SignInfo(object):
    pass


class MHYClient(object):

    # 获取用户角色
    def get_user_game_roles(self, cookie: str) -> RoleInfo | None:
        raise NotImplementedError('Method not implemented!')

    # 获取用户是否签到
    def get_sign_state_info(self, cookie: str) -> IsSignInfo | None:
        raise NotImplementedError('Method not implemented!')

    def sign(self, cookie: str) -> SignInfo | None:
        raise NotImplementedError('Method not implemented!')
