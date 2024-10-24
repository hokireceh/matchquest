import sys

sys.dont_write_bytecode = True

import urllib3

urllib3.disable_warnings()

from hokireceh_claimer import base
from core.token import get_token
from core.info import get_info
from core.task import process_do_task, process_claim_ref
from core.farm import process_farming
from core.boost import process_buy_daily_booster, process_buy_game_booster
from core.game import process_play_game

import time
import json


class MatchQuest:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data-proxy.json")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="MatchQuest")

        # Get config
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim_ref = base.get_config(
            config_file=self.config_file, config_name="auto-claim-ref"
        )

        self.auto_farm = base.get_config(
            config_file=self.config_file, config_name="auto-farm"
        )

        self.auto_buy_daily_booster = base.get_config(
            config_file=self.config_file, config_name="auto-buy-daily-booster"
        )

        self.auto_buy_game_booster = base.get_config(
            config_file=self.config_file, config_name="auto-buy-game-booster"
        )

        self.auto_play_game = base.get_config(
            config_file=self.config_file, config_name="auto-play-game"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            accounts = json.load(open(self.data_file, "r"))["accounts"]
            num_acc = len(accounts)
            base.log(self.line)
            base.log(f"{base.green}Numer of accounts: {base.white}{num_acc}")

            for no, account in enumerate(accounts):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = base.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    break

                actual_ip = base.check_ip(proxy_info=proxy_info)

                proxies = base.format_proxy(proxy_info=proxy_info)

                try:
                    token, user_id = get_token(data=data, proxies=proxies)

                    if token:

                        get_info(token=token, user_id=user_id, proxies=proxies)

                        # Do task
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                            process_do_task(
                                token=token, user_id=user_id, proxies=proxies
                            )
                        else:
                            base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                        # Claim ref
                        if self.auto_claim_ref:
                            base.log(f"{base.yellow}Auto Claim Ref: {base.green}ON")
                            process_claim_ref(
                                token=token, user_id=user_id, proxies=proxies
                            )
                        else:
                            base.log(f"{base.yellow}Auto Claim Ref: {base.red}OFF")

                        # Farm
                        if self.auto_farm:
                            base.log(f"{base.yellow}Auto Farm: {base.green}ON")
                            process_farming(
                                token=token, user_id=user_id, proxies=proxies
                            )
                        else:
                            base.log(f"{base.yellow}Auto Farm: {base.red}OFF")

                        # Daily Booster
                        if self.auto_farm:
                            base.log(
                                f"{base.yellow}Auto Buy Daily Booster: {base.green}ON"
                            )
                            process_buy_daily_booster(
                                token=token, user_id=user_id, proxies=proxies
                            )
                        else:
                            base.log(
                                f"{base.yellow}Auto Buy Daily Booster: {base.red}OFF"
                            )

                        # Game Booster
                        if self.auto_farm:
                            base.log(
                                f"{base.yellow}Auto Buy Game Booster: {base.green}ON"
                            )
                            process_buy_game_booster(
                                token=token, user_id=user_id, proxies=proxies
                            )
                        else:
                            base.log(f"{base.yellow}Auto Game Booster: {base.red}OFF")

                        # Play game
                        if self.auto_play_game:
                            base.log(f"{base.yellow}Auto Play Game: {base.green}ON")
                            process_play_game(token=token, proxies=proxies)
                        else:
                            base.log(f"{base.yellow}Auto Play Game: {base.red}OFF")

                        get_info(token=token, user_id=user_id, proxies=proxies)

                    else:
                        base.log(f"{base.red}Token not found! Please get new query id")
                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        matchquest = MatchQuest()
        matchquest.main()
    except KeyboardInterrupt:
        sys.exit()
