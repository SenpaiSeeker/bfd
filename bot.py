import requests
import json
import random
import os
import urllib.parse
from colorama import *
from datetime import datetime, timedelta
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class BFDcoin:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.bfdcoin.org',
            'Origin': 'https://bfdcoin.org',
            'Pragma': 'no-cache',
            'Referer': 'https://bfdcoin.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}BFD Coin - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            user_id = user_data['id']
            first_name = user_data['first_name']
            return user_id, first_name
        else:
            raise ValueError("User data not found in query.")

    def account_info(self, user_id: int):
        url = 'https://api.bfdcoin.org/api?act=accountInfo'
        self.headers.update({
            'Content-Type': 'application/json',
            'Token': str(user_id)
        })

        response = self.session.post(url, headers=self.headers)
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
        
    def common_tasklist(self, user_id: int):
        url = 'https://api.bfdcoin.org/api?act=getCommonTaskList'
        self.headers.update({
            'Content-Type': 'application/json',
            'Token': str(user_id)
        })

        response = self.session.post(url, headers=self.headers)
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
        
    def finish_task(self, user_id: int, task_id: int):
        url = 'https://api.bfdcoin.org/api?act=finishTask'
        data = str(task_id)
        self.headers.update({
            'Content-Type': 'application/json',
            'Token': str(user_id)
        })

        response = self.session.post(url, headers=self.headers, data=data)
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
        
    def collect_spesialbox(self, user_id: int):
        url = 'https://api.bfdcoin.org/api?act=collectSpecialBoxCoin'
        data = {'boxType': 2, 'coinCount': 2100}
        self.headers.update({
            'Content-Type': 'application/json',
            'Token': str(user_id)
        })

        response = self.session.post(url, headers=self.headers, json=data)
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
        
    from colorama import Fore, Style

    def question(self):
        while True:
            collect = input("Inject Collect Spesial Box? [y/n] -> ").strip().lower()
            if collect in ["y", "n"]:
                collect = collect == "y"
                break
            else:
                print(f"{Fore.RED + Style.BRIGHT}Invalid Input.{Fore.WHITE + Style.BRIGHT} Choose 'y' to Yes or 'n' to No.{Style.RESET_ALL}")

        if collect:
            while True:
                try:
                    print("1. Multi Account Processing")
                    print("2. Single Account Processing")
                    choose = int(input("Choose [1/2] -> ").strip())

                    if choose in [1, 2]:
                        print(f"{Fore.GREEN + Style.BRIGHT}You chose {'Multi' if choose == 1 else 'Single'} Account Processing.{Style.RESET_ALL}")
                        return collect, choose
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")
        
        return collect, None
    
    def process_query(self, query: str, collect: bool, choose: int):

        user_id, first_name = self.load_data(query)

        account = self.account_info(user_id)
        if account:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {account['currentAmount']:.3f} $BFD {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Level{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {account['userLevel']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )

            tasklists = self.common_tasklist(user_id)
            if tasklists:

                tasks = tasklists['data']
                if tasks:
                    for task in tasks:
                        task_id = task['taskId']

                        if task and task['taskStatus'] == 0:
                            finish = self.finish_task(user_id, task_id)
                            if finish:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['taskName']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {finish['bonusAmount']} $BFD {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['taskName']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
            if collect:
                if choose == 1:
                    success = self.collect_spesialbox(user_id)
                    if success:
                        balance = self.account_info(user_id)
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Special Box{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {success['collectAmount']:.3f} $BFD {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Collected{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Balance{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {balance['currentAmount']:.3f} $BFD {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Special Box{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Isn't Collected {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    time.sleep(1)
                else:
                    while True:
                        success = self.collect_spesialbox(user_id)
                        if success:
                            balance = self.account_info(user_id)
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Special Box{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {success['collectAmount']:.3f} $BFD {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Collected{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Balance{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {balance['currentAmount']:.3f} $BFD {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Special Box{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Collected {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        # time.sleep(0.01)
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Special Box{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Skipped {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            collect, choose = self.question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query, collect, choose)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] BFD Coin - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bfd = BFDcoin()
    bfd.main()
