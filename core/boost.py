import requests

from hokireceh_claimer import base
from core.headers import headers


def buy_daily_booster(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/purchase"
    payload = {"uid": user_id, "type": "daily"}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
            verify=False,
        )
        data = response.json()
        return data
    except:
        return None


def process_buy_daily_booster(token, user_id, proxies=None):
    daily_booster = buy_daily_booster(token=token, user_id=user_id, proxies=proxies)
    try:
        status = daily_booster["code"] == 200
        msg = daily_booster["msg"]
        if status:
            base.log(f"{base.white}Auto Buy Daily Booster: {base.green}{msg}")
        else:
            base.log(f"{base.white}Auto Buy Daily Booster: {base.red}{msg}")
    except:
        base.log(f"{base.white}Auto Buy Daily Booster: {base.red}Buy Boost Error")


def buy_game_booster(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/purchase"
    payload = {"uid": user_id, "type": "game"}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
            verify=False,
        )
        data = response.json()
        return data
    except:
        return None


def process_buy_game_booster(token, user_id, proxies=None):
    game_booster = buy_game_booster(token=token, user_id=user_id, proxies=proxies)
    try:
        status = game_booster["code"] == 200
        msg = game_booster["msg"]
        if status:
            base.log(f"{base.white}Auto Buy Game Booster: {base.green}{msg}")
        else:
            base.log(f"{base.white}Auto Buy Game Booster: {base.red}{msg}")
    except:
        base.log(f"{base.white}Auto Buy Game Booster: {base.red}Buy Boost Error")
