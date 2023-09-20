import logging
import time
import uuid

from pydantic import BaseModel

from base.client import MHYClient, RoleInfo, IsSignInfo, SignInfo
from base.http_client import req, HttpRequest, BaseRequest
from configs import userConfig
import logging as log


class GenshinRoleInfo(RoleInfo, BaseModel):
    region: str
    game_uid: int
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


class GenshinSignInfo(SignInfo, BaseModel):
    retcode: int
    message: str


class GenshinClient(MHYClient):

    def get_user_game_roles(self, cookie: str) -> list[GenshinRoleInfo] | None:
        header = BaseRequest(cookie)
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
            return None

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

        if response is None:
            log.error("没有找到签到信息")

        info = response.get('data')
        if info is None:
            return info

        return GenshinIsSignInfo.model_validate(info)

    def sign(self, cookie: str) -> GenshinSignInfo | None:
        roles = self.get_user_game_roles(cookie)
        if roles is None:
            log.error("获取角色信息失败")
            return None

        for r in roles:
            sign_info = self.get_sign_state_info(cookie, r.region, r.game_uid)
            if sign_info is None:
                log.error("获取角色签到信息失败")

            if sign_info.first_bind is True:
                log.error("请先手动签到一次")

            if sign_info.is_sign is True:
                log.info(f"{r.game_uid}今天已经签到过了")

            log.info(f"名字:{r.nickname} 签到中......")
            time.sleep(1.5)

            header = BaseRequest(cookie).getHeader()
            header.update({
                'x-rpc-device_id': str(uuid.uuid3(
                    uuid.NAMESPACE_URL, cookie)).replace('-', '').upper(),
                'x-rpc-client_type': '5',
                'x-rpc-app_version': userConfig.APP_VERSION,
                'DS': self.getDigest(),
            })

            sign_data = {
                'act_id': userConfig.ACT_ID,
                'region': r.region,
                'uid': r.game_uid
            }

            response = {}
            try:
                response = HttpRequest.toPython(
                    req.sendRequest(method='post', url=userConfig.SIGN_URL, headers=header,
                                    data=HttpRequest.toJson(sign_data,
                                                            ensure_ascii=False)).text)
            except Exception as e:
                log.error(e)

            info = GenshinSignInfo.model_validate(response)
            return info


genshinClient = GenshinClient()
