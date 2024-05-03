import logging
import uuid

from pydantic import BaseModel

from base.api_error import MihoyoBBSException
from base.client import MHYClient, RoleInfo, LunaInfo, SignInfo
from base.http_client import req, HttpRequest, BaseRequest
from base import constant

logger = logging.getLogger(__name__)


class HonkaiStarRailRoleInfo(RoleInfo, BaseModel):
    region: str
    game_uid: int
    nickname: str
    region_name: str
    level: int


class HonkaiStarRailLunaInfo(LunaInfo, BaseModel):
    total_sign_day: int
    today: str
    is_sign: bool
    is_sub: bool
    sign_cnt_missed: int
    short_sign_day: int


class HonkaiStarRailSignInfo(SignInfo, BaseModel):
    retcode: int
    message: str


class HonkaiStarRailClient(MHYClient):

    # 获取用户角色信息
    async def get_user_game_roles(self, cookie: str) -> list[HonkaiStarRailRoleInfo]:
        header = BaseRequest(cookie)
        try:
            logger.info("获取星穹铁道账号信息")
            response = await req.sendRequest(
                "get",
                constant.HONKAI_STAR_RAIL_ROLE_URL,
                headers=header.getHeader(),
            )
            text = await response.text()
            data_dict = HttpRequest.toPython(text)
            message = data_dict["message"]
        except Exception as e:
            logger.error(f"{e}")
            raise e

        if data_dict.get("retcode", 1) != 0 or data_dict.get("data", None) is None:
            logger.error(message)
            raise MihoyoBBSException(data_dict)

        user_list = []
        user_info = data_dict.get("data", {}).get("list", [])
        for user in user_info:
            user_list.append(HonkaiStarRailRoleInfo.model_validate(user))
        logger.info(f"共有{len(user_list)}个角色")

        return user_list

    # 获取角色签到信息
    async def get_sign_state_info(
        self, cookie, region: str, uid: int
    ) -> HonkaiStarRailLunaInfo:
        header = BaseRequest(cookie)
        logger.info(f"正在验证id:{uid}签到信息")
        try:
            response = await req.sendRequest(
                "get",
                constant.HONKAI_STAR_RAIL_INFO_URL.format(
                    constant.HONKAI_STAR_RAIL_ACT_ID, region, uid
                ),
                headers=header.getHeader(),
            )
            text = await response.text()
            data_dict = HttpRequest.toPython(text)
        except Exception as e:
            raise e

        if data_dict.get("retcode", 1) != 0 or data_dict.get("data", None) is None:
            raise MihoyoBBSException(data_dict)

        logger.info(f"角色签到信息{data_dict}")

        sign_info = HonkaiStarRailLunaInfo.model_validate(data_dict.get("data"))
        if sign_info.is_sign:
            logger.info(f"{uid}已签到")

        return sign_info

    # 角色签到
    async def sign(self, cookie, region: str, uid: int) -> bool:
        header = BaseRequest(cookie).getHeader()
        header.update(
            {
                "x-rpc-device_id": str(uuid.uuid3(uuid.NAMESPACE_URL, cookie))
                .replace("-", "")
                .upper(),
                "x-rpc-client_type": "5",
                "x-rpc-app_version": constant.APP_VERSION,
                "DS": self.getDigest(),
            }
        )

        sign_data = {
            "act_id": constant.HONKAI_STAR_RAIL_ACT_ID,
            "region": region,
            "uid": uid,
            "lang": "zh-cn",
        }

        try:
            response = await req.sendRequest(
                method="post",
                url=constant.HONKAI_STAR_RAIL_SIGN_URL,
                headers=header,
                data=HttpRequest.toJson(sign_data, ensure_ascii=False),
            )
            text = await response.text()
            data_dict = HttpRequest.toPython(text)
        except Exception as e:
            raise e

        if data_dict.get("retcode", 1) != 0 or data_dict.get("data", None) is None:
            raise MihoyoBBSException(data_dict)

        logger.info(f"{uid}签到成功")
        return True


honkaiStarRailClient = HonkaiStarRailClient()
