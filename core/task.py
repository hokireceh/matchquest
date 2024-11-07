import requests
import time

from hokireceh_claimer import base
from core.headers import headers


def get_task(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/task/list"
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
        task_list = data["data"]
        return task_list
    except:
        return None


def complete_task(token, user_id, task_code, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/task/complete"
    payload = {"uid": user_id, "type": task_code}

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
        status = data["data"]
        return status
    except:
        return None


def claim_task(token, user_id, task_code, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/task/claim"
    payload = {"uid": user_id, "type": task_code}

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
        status = data["data"] == "success"
        return status
    except:
        return None


def process_do_task(token, user_id, proxies=None):
    task_dict = get_task(token=token, user_id=user_id, proxies=proxies)
    for task_type, task_list in task_dict.items():
        if task_list is not None:
            base.log(f"{base.white}Task Group: {base.yellow}{task_type}")
            for task in task_list:
                task_code = task["name"]
                task_name = task["description"]
                task_status = task["complete"]
                if task_status:
                    base.log(f"{base.white}{task_name}: {base.green}Completed")
                else:
                    complete_task_status = complete_task(
                        token=token,
                        user_id=user_id,
                        task_code=task_code,
                        proxies=proxies,
                    )
                    time.sleep(3)
                    claim_task_status = claim_task(
                        token=token,
                        user_id=user_id,
                        task_code=task_code,
                        proxies=proxies,
                    )
                    if claim_task_status:
                        base.log(f"{base.white}{task_name}: {base.green}Completed")
                    else:
                        base.log(
                            f"{base.white}{task_name}: {base.red}Not ready to claim"
                        )


def claim_ref(token, user_id, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/claim"
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
        return data
    except:
        return None


def process_claim_ref(token, user_id, proxies=None):
    while True:
        start_claim_ref = claim_ref(token=token, user_id=user_id, proxies=proxies)
        claim_ref_status = start_claim_ref["code"]
        if claim_ref_status == 200:
            claimed = start_claim_ref["data"] / 1000
            if claimed > 0:
                base.log(
                    f"{base.white}Auto Claim Ref: {base.green}Success | Added {claimed:,} points"
                )
                break
            else:
                base.log(f"{base.white}Auto Claim Ref: {base.red}No point from ref")
                break
        elif claim_ref_status == 403:
            time.sleep(5)
            continue
