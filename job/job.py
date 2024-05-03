from collections import deque
import glob
import os
import logging
import asyncio
import aioschedule as schedule
from datetime import datetime
from conf.config import Config
from base.api_error import MihoyoBBSException
from conf.config import Config
from mhy_game_client.genshin import genshinClient
from mhy_game_client.honkai_star_rail import honkaiStarRailClient

logger = logging.getLogger(__name__)

# 配置文件目录, 默认: ./config
CONFIG_DIR = os.environ.get("CONFIG_DIR", os.path.join(os.getcwd(), "config"))

# JOB每次执行的时间间隔, 默认: 30分钟
JOB_TIME_INTERVAL = int(os.environ.get("JOB_TIME_INTERVAL", 30))

# 两个用户之间的签到时间间隔, 默认: 5分钟, 用户数量 x USER_INTERVAL 应该大于 JOB_TIME_INTERVAL
USER_INTERVAL = int(os.environ.get("USER_INTERVAL", 5)) * 60


class SignRecord:
    config = dict()
    genshin_impact = dict()
    honkai_star_rail = dict()

    def config_is_sign(self, config_path: str) -> bool:
        if config_path in self.config:
            return self.config[config_path]
        return False

    def config_done_sign(self, config_path: str) -> None:
        self.config[config_path] = True

    def genshin_impact_is_sign(self, game_uid: int) -> bool:
        if game_uid in self.genshin_impact:
            return self.genshin_impact[game_uid]
        return False

    def genshin_impact_done_sign(self, game_uid: int) -> None:
        self.genshin_impact[game_uid] = True

    def honkai_star_rail_is_sign(self, game_uid: int) -> bool:
        if game_uid in self.honkai_star_rail:
            return self.honkai_star_rail[game_uid]
        return False

    def honkai_star_rail_done_sign(self, game_uid: int) -> None:
        self.honkai_star_rail[game_uid] = True


previous_time = datetime.now()
sign_record = SignRecord()


async def genshin_impact_sign(config: Config) -> bool:
    global sign_record

    if not config.act.genshin_impact:
        return True

    user_is_sign = []
    try:
        user_list = await genshinClient.get_user_game_roles(config.cookie)
    except MihoyoBBSException as e:
        logger.error(f"MihoyoBBSException: {e}")
        return False
    except Exception as e:
        logger.error(f"{e}")
        return False

    for user in user_list:
        try:
            if sign_record.genshin_impact_is_sign(user.game_uid):
                user_is_sign.append(True)
                continue
            sign_info = await genshinClient.get_sign_state_info(
                config.cookie, user.region, user.game_uid
            )
            if sign_info.is_sign:
                user_is_sign.append(True)
            else:
                done = await genshinClient.sign(
                    config.cookie, user.region, user.game_uid
                )
                user_is_sign.append(done)
                if done:
                    sign_record.genshin_impact_done_sign(user.game_uid)
        except MihoyoBBSException as e:
            user_is_sign.append(False)
            logger.error(f"MihoyoBBSException: {e}")
        except Exception as e:
            user_is_sign.append(False)
            logger.error(f"{e}")

    return all(user_is_sign)


async def honkai_star_rail_sign(config: Config) -> bool:
    global sign_record

    if not config.act.honkai_star_rail:
        return True

    user_is_sign = []
    try:
        user_list = await honkaiStarRailClient.get_user_game_roles(config.cookie)
    except MihoyoBBSException as e:
        logger.error(f"MihoyoBBSException: {e}")
        return False
    except Exception as e:
        logger.error(f"{e}")
        return False

    for user in user_list:
        try:
            if sign_record.honkai_star_rail_is_sign(user.game_uid):
                user_is_sign.append(True)
                continue
            sign_info = await honkaiStarRailClient.get_sign_state_info(
                config.cookie, user.region, user.game_uid
            )
            if sign_info.is_sign:
                user_is_sign.append(True)
            else:
                done = await honkaiStarRailClient.sign(
                    config.cookie, user.region, user.game_uid
                )
                user_is_sign.append(done)
                if done:
                    sign_record.honkai_star_rail_done_sign(user.game_uid)
        except MihoyoBBSException as e:
            user_is_sign.append(False)
            logger.error(f"MihoyoBBSException: {e}")
        except Exception as e:
            user_is_sign.append(False)
            logger.error(f"{e}")

    return all(user_is_sign)


async def task(config_path: str, config: Config):
    global sign_record

    if sign_record.config_is_sign(config_path):
        logger.info(f"跳过配置文件: {config_path}, 已完成所有签到。")
        return

    if all([await genshin_impact_sign(config), await honkai_star_rail_sign(config)]):
        sign_record.config_done_sign(config_path)


async def job():
    global sign_record, previous_time

    logger.info("执行Job任务...")

    current_time = datetime.now()
    difference = current_time - previous_time
    if difference.days >= 1:
        # 第二天, 清空签到记录
        logger.info("已清空前一天签到记录。")
        previous_time = datetime.now()
        sign_record = SignRecord()

    toml_files = glob.glob(pathname="*.toml", root_dir=CONFIG_DIR)

    queue = deque([os.path.join(CONFIG_DIR, toml_name) for toml_name in toml_files])

    while len(queue) > 0:
        file_path = queue.pop()

        logger.info(f"读取配置文件: {file_path}")
        config = Config.load(file_path)

        now = datetime.now()
        time_object = datetime.strptime(config.job.trigger_time, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if now > time_object:
            logger.info("执行签到任务...")
            await task(file_path, config)
        else:
            logger.info("配置未到执行时间, 继续等待...")

        if len(queue) > 0:
            await asyncio.sleep(USER_INTERVAL)

    logger.info("Job任务执行完成。")


async def run():
    logger.info("开启Job...")
    # 默认每半小时执行一次, 修改`JOB_TIME_INTERVAL`环境变量
    schedule.every(JOB_TIME_INTERVAL).minutes.do(job)
    await job()
    while True:
        await schedule.run_pending()
        await asyncio.sleep(USER_INTERVAL)
