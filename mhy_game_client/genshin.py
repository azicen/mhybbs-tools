from base.client import MHYClient, RoleInfo, IsSignInfo, SignInfo
from base.http_client import req, HttpRequest, BaseRequest
from configs import userConfig
import logging as log


class GenshinRoleInfo(RoleInfo):
    def __init__(self, region: str, game_uid: str, nickname: str, region_name: str, level: int):
        self.region = region
        self.game_uid = game_uid
        self.nickname = nickname
        self.region_name = region_name
        self.level = level

    def __str__(self):
        return HttpRequest.toJson({
            "region": self.region,
            "game_uid": self.game_uid,
            "nickname": self.nickname,
            "region_name": self.region_name,
            "level": self.level
        }, ensure_ascii=False)


class GenshinIsSignInfo(IsSignInfo):
    pass


class GenshinSignInfo(SignInfo):
    pass


class GenshinClient(MHYClient):
    def get_user_game_roles(self, cookie: str) -> list[GenshinRoleInfo] | None:
        header = BaseRequest(cookie)
        response = {}
        try:
            log.info("获取原神账号信息")
            response = HttpRequest.toPython(
                req.sendRequest('get', userConfig.GENSHIN_ROLE_URL, headers=header.getHeader()).text)
            message = response['message']
        except Exception as e:
            log.error(f'{e}')
            return None

        if response is None:
            return None

        if response.get('retcode', 1) != 0 or response.get('data', None) is None:
            log.error(message)

        user_list = []
        user_info = response.get('data', {}).get('list', [])
        for user in user_info:
            user_list.append(GenshinRoleInfo(
                user['region'],
                user['game_uid'],
                user['nickname'],
                user['region_name'],
                user['level']
            ))

        return user_list

    def get_sign_state_info(self, cookie: str) -> GenshinIsSignInfo | None:
        pass

    def sign(self, cookie: str) -> GenshinSignInfo | None:
        pass


genshinClient = GenshinClient()
