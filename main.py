import logging
import os

from dotenv import load_dotenv

from mhy_game_client.genshin import genshinClient

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    load_dotenv()
    cookie = os.getenv("COOKIE")
    # info = genshinClient.get_sign_state_info(cookie, "cn_gf01", "105827582")
    # logging.info(info)
    genshinClient.sign(cookie)
    # roles = genshinClient.get_user_game_roles(cookie)
    # for r in roles:
    #     logging.info(r)