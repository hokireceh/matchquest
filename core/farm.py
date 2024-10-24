import requests
import time

from hokireceh_claimer import base
from core.headers import headers


def claim(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim"
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
        status = data["code"]
        return status
    except:
        return None


def farming(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming"
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
        status = data["code"]
        return status
    except:
        return None


def process_farming(token, user_id, proxies=None):
    while True:
        claim_status = claim(token=token, user_id=user_id, proxies=proxies)
        if claim_status == 200:
            base.log(f"{base.white}Auto Farm: {base.green}Claim Success")
            break
        elif claim_status == 403:
            time.sleep(5)
            continue
        else:
            base.log(f"{base.white}Auto Farm: {base.red}Not ready to claim")
            break

    time.sleep(3)

    while True:
        farming_status = farming(token=token, user_id=user_id, proxies=proxies)
        if farming_status == 200:
            base.log(f"{base.white}Auto Farm: {base.green}Start Farming Success")
        elif farming_status == 403:
            time.sleep(5)
            continue
        else:
            base.log(f"{base.white}Auto Farm: {base.red}Not ready to farm")
            break
