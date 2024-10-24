import requests
import time
import random

from hokireceh_claimer import base
from core.headers import headers


def start_game(token, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/play"

    try:
        response = requests.get(
            url=url,
            headers=headers(token=token),
            proxies=proxies,
            timeout=20,
            verify=False,
        )
        data = response.json()
        return data
    except:
        return None


def claim_game(token, game_id, point, proxies=None):
    url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/claim"
    payload = {"game_id": game_id, "point": point}

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


def process_play_game(token, proxies=None):
    while True:
        game = start_game(token=token, proxies=proxies)
        try:
            game_id = game["data"]["game_id"]
            ticket_left = game["data"]["game_count"]
            if game_id != "":
                base.log(f"{base.yellow}Playing for 30 seconds...")
                time.sleep(30)
                point = random.randint(130, 150)
                start_claim_game = claim_game(
                    token=token, game_id=game_id, point=point, proxies=proxies
                )
                status = start_claim_game["code"] == 200
                if status:
                    base.log(
                        f"{base.white}Auto Play Game: {base.green}Success | Added {point} points - Ticket left: {base.white}{ticket_left}"
                    )
                else:
                    base.log(f"{base.white}Auto Play Game: {base.red}Claim game error")
                    break

                if ticket_left == 0:
                    base.log(
                        f"{base.white}Auto Play Game: {base.red}No ticket available"
                    )
                    break
            else:
                base.log(f"{base.white}Auto Play Game: {base.red}No ticket available")
                break
        except:
            base.log(f"{base.white}Auto Play Game: {base.red}Start game error")
            break
