import logging
import uuid

from pydantic import BaseModel

from base.api_error import MihoyoBBSException
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

    # 获取用户角色信息
    def get_user_game_roles(self, cookie: str) -> list[GenshinRoleInfo]:
        header = BaseRequest(cookie)
        try:
            log.info("获取原神账号信息")
            response = HttpRequest.toPython(
                req.sendRequest('get', userConfig.GENSHIN_ROLE_URL, headers=header.getHeader()).text)
            message = response['message']
        except Exception as e:
            log.error(f'{e}')
            raise e

        if response.get('retcode', 1) != 0 or response.get('data', None) is None:
            log.error(message)
            raise MihoyoBBSException(response)

        user_list = []
        user_info = response.get('data', {}).get('list', [])
        for user in user_info:
            user_list.append(GenshinRoleInfo.model_validate(user))
        logging.info(f"共有{len(user_list)}个角色")

        return user_list

    # 获取角色签到信息
    def get_sign_state_info(self, cookie, region: str, uid: int) -> GenshinIsSignInfo:
        header = BaseRequest(cookie)
        log.info(f"正在验证id:{uid}签到信息")
        try:
            response = HttpRequest.toPython(
                req.sendRequest('get', userConfig.INFO_URL.format(region, userConfig.ACT_ID, uid),
                                headers=header.getHeader()).text)

        except Exception as e:
            raise e

        if response.get('retcode', 1) != 0 or response.get('data', None) is None:
            raise MihoyoBBSException(response)

        logging.info(f"角色签到信息{response}")

        return GenshinIsSignInfo.model_validate(response.get('data'))

    # 角色签到
    def sign(self, cookie, region: str, uid: int) -> bool:

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
            'region': region,
            'uid': uid
        }

        try:
            response = HttpRequest.toPython(
                req.sendRequest(method='post', url=userConfig.SIGN_URL, headers=header,
                                data=HttpRequest.toJson(sign_data, ensure_ascii=False)).text)
        except Exception as e:
            raise e

        if response.get('retcode', 1) != 0 or response.get('data', None) is None:
            raise MihoyoBBSException(response)

        return True


genshinClient = GenshinClient()
