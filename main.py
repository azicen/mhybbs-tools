from mhy_game_client.genshin import genshinClient

if __name__ == '__main__':
    roles = genshinClient.get_user_game_roles("")
    for r in roles:
        print(str(r))