import logging
import os

from dotenv import load_dotenv

from mhy_game_client.genshin import genshinClient

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    load_dotenv()
    cookie = os.getenv("COOKIE")
    user_list = genshinClient.get_user_game_roles(cookie)
    for user in user_list:
        sign_info = genshinClient.get_sign_state_info(cookie,user.region,user.game_uid)
        if sign_info.is_sign is False:
            genshinClient.sign(cookie, user.region, user.game_uid)

