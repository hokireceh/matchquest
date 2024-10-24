import requests
import json
from urllib.parse import parse_qs

from hokireceh_claimer import base
from core.headers import headers

import certifi


parse_data = lambda data: {key: value[0] for key, value in parse_qs(data).items()}


def get_token(data, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/login"
    parser = parse_data(data)
    user = json.loads(parser["user"])
    payload = {
        "uid": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "tg_login_params": data,
    }

    # try:
    response = requests.post(
        url=url,
        headers=headers(),
        json=payload,
        proxies=proxies,
        timeout=20,
        verify=False,
        # verify=False,
    )
    data = response.json()
    token = data["data"]["token"]
    user_id = data["data"]["user"]["uid"]
    return token, user_id
    # except:
    #     return None
