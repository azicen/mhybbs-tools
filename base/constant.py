API_TAKUMI_URL = "https://api-takumi.mihoyo.com"
USER_GAME_ROLES = f"{API_TAKUMI_URL}/binding/api/getUserGameRolesByCookie"

APP_VERSION = "2.70.1"
USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
    f" miHoYoBBS/{APP_VERSION}"
)
Origin_URL = "https://act.mihoyo.com"
REFERER_URL = "https://act.mihoyo.com/"

# 原神
GENSHIN_X_RPC_SIGNGAME = "hk4e"
GENSHIN_ACT_ID = "e202311201442471"
GENSHIN_ROLE_URL = f"{USER_GAME_ROLES}?game_biz=hk4e_cn"
GENSHIN_INFO_URL = (
    f"{API_TAKUMI_URL}/event/luna/info?" "act_id={}&region={}&uid={}&lang=zh-cn"
)
GENSHIN_SIGN_URL = f"{API_TAKUMI_URL}/event/luna/sign"

# 星铁
HONKAI_STAR_RAIL_ACT_ID = "e202304121516551"
HONKAI_STAR_RAIL_ROLE_URL = f"{USER_GAME_ROLES}?game_biz=hkrpg_cn"
HONKAI_STAR_RAIL_INFO_URL = (
    f"{API_TAKUMI_URL}/event/luna/info?" "act_id={}&region={}&uid={}&lang=zh-cn"
)
HONKAI_STAR_RAIL_SIGN_URL = f"{API_TAKUMI_URL}/event/luna/sign"
