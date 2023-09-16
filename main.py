import logging
import os

from dotenv import load_dotenv

from mhy_game_client.genshin import genshinClient

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    load_dotenv()
    roles = genshinClient.get_user_game_roles(os.getenv("COOKIE"))
    for r in roles:
        logging.info(r)