from base.client import MHYClient, RoleInfo, IsSignInfo, SignInfo
from base.http_client import req, HttpRequest, BaseRequest
from configs import userConfig
import logging as log


class GenshinRoleInfo(RoleInfo):
    pass


class GenshinIsSignInfo(IsSignInfo):
    pass


class GenshinSignInfo(SignInfo):
    pass


class GenshinClient(MHYClient):
    def get_user_game_roles(self, cookie: str) -> GenshinRoleInfo | None:
        header = BaseRequest(cookie)
        response = {}
        try:
            response = HttpRequest.toPython(req.sendRequest('get', userConfig.GENSHIN_ROLE_URL, headers=header.getHeader()).text)
            if response is None:
                return None
        except Exception as e:
            log.error(f'{e}')
            return None



    def get_sign_state_info(self, cookie: str) -> GenshinIsSignInfo | None:
        pass

    def sign(self, cookie: str) -> GenshinSignInfo | None:
        pass


genshinClient = GenshinClient()
