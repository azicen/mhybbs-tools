import logging

from pydantic import BaseModel

from base.client import MHYClient, RoleInfo, IsSignInfo, SignInfo
from base.http_client import req, HttpRequest, BaseRequest
from configs import userConfig
import logging as log


class GenshinRoleInfo(RoleInfo, BaseModel):
    region: str
    game_uid: str
    nickname: str
    region_name: str
    level: int


class GenshinIsSignInfo(IsSignInfo, BaseModel):
    total_sign_day: int
    today: str
    is_sign: bool
    first_bind: bool
    is_sub: bool
    month_first: bool
    sign_cnt_missed: int
    month_last_day: bool


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
            user_list.append(GenshinRoleInfo.model_validate(user))

        return user_list

    def get_sign_state_info(self, cookie, region: str, uid: int) -> GenshinIsSignInfo | None:
        header = BaseRequest(cookie)
        log.info(f"正在验证id:{uid}签到信息")
        try:
            response = HttpRequest.toPython(
                req.sendRequest('get', userConfig.INFO_URL.format(region, userConfig.ACT_ID, uid),
                                headers=header.getHeader()).text)
        except Exception as e:
            log.error(e)
            return None

        info = response.get('data')
        if info is None:
            return info

        return GenshinIsSignInfo.model_validate(info)

    def sign(self, cookie: str) -> GenshinSignInfo | None:
        pass


genshinClient = GenshinClient()
