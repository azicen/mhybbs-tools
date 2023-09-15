from base.client import MHYClient, RoleInfo, IsSignInfo, SignInfo


class GenshinRoleInfo(RoleInfo):
    pass


class GenshinIsSignInfo(IsSignInfo):
    pass


class GenshinSignInfo(SignInfo):
    pass


class GenshinClient(MHYClient):
    def get_user_game_roles(self, cookie: str) -> GenshinRoleInfo | None:
        pass

    def get_sign_state_info(self, cookie: str) -> GenshinIsSignInfo | None:
        pass

    def sign(self, cookie: str) -> GenshinSignInfo | None:
        pass
