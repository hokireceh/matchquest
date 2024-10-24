import requests

from hokireceh_claimer import base
from core.headers import headers


def get_info(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/balance"
    payload = {"uid": user_id}

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
        balance = data["data"] / 1000

        base.log(f"{base.green}Balance: {base.white}{balance:,}")
        return data
    except:
        return None
