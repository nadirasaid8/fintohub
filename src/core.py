import os
import asyncio
import aiohttp
import random
from . import *
from colorama import *
from datetime import datetime
from src.headers import headers

init(autoreset=True)
config = read_config()

class Fintopio:
    def __init__(self):
        self.base_url = "https://fintopio-tg.fintopio.com/api"
        self.headers = headers()
        self.auto_break_asteroid = config.get('auto_break_asteroid', False)
        self.auto_complete_task = config.get('auto_complete_task', False)
        self.account_delay = config.get('account_delay', 5)
        self.use_proxies = config.get('use_proxies', False)
        self.proxies = self.load_proxies() if self.use_proxies else []

    def load_proxies(self):
        proxies_file = os.path.join(os.path.dirname(__file__), '../proxies.txt')
        formatted_proxies = []
        with open(proxies_file, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:
                    if proxy.startswith("socks5://"):
                        formatted_proxies.append(proxy)
                    elif not (proxy.startswith("http://") or proxy.startswith("https://")):
                        formatted_proxies.append(f"http://{proxy}")
                    else:
                        formatted_proxies.append(proxy)
        return formatted_proxies

    async def auth(self, user_data, proxy=None):
        url = f"{self.base_url}/auth/telegram"
        headers = {**self.headers, "Webapp": "true"}
        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"{url}?{user_data}", headers=headers, proxy=proxy) as response:
                if response.status != 200:
                    log(f"Failed to authenticate, status: {response.status}, reason: {await response.text()}")
                    return None
                data = await response.json()
                return data['token']

    async def get_profile(self, token, proxy=None):
        url = f"{self.base_url}/fast/init"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Webapp": "false, true",
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def check_in_daily(self, token, proxy=None):
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Origin": "https://fintopio-tg.fintopio.com",
        }
        async with aiohttp.ClientSession() as sess:
            try:
                referral_url = f"{self.base_url}/referrals/data"
                async with sess.get(referral_url, headers=headers) as referral_response:
                    jData = await referral_response.json()
                    jsondaily = jData.get('isDailyRewardClaimed', False)

                    if not jsondaily:
                        log(hju + f'Daily Check-in Successfully{Fore.RESET}')
                        checkin_url = f"{self.base_url}/daily-checkins"
                        async with sess.post(checkin_url, headers=headers, proxy=proxy) as checkin_response:
                            try:
                                data = await checkin_response.json()
                                if 'rewards' in data:
                                    rewards = data['rewards']
                                    total_days = data.get('totalDays', 0)
                                    log(hju + f"Total Days Checked In: {pth}{total_days}")
                                    for reward in rewards:
                                        if reward['status'] == 'now':
                                            log(hju + f"Today's reward: {pth}{reward['reward']} {hju}claimed")
                                else:
                                    log(f"Failed to check-in: {checkin_response.status} Response: {data}")
                            except aiohttp.ContentTypeError:
                                text_data = await checkin_response.text()
                                log(f"Non-JSON response: {checkin_response.status}, content: {text_data}")
                    else:
                        log(kng + f"Daily reward already claimed")
            except (Exception, AttributeError) as e:
                log(f'Daily check-in error: {str(e)}')
                await asyncio.sleep(5)

    async def get_farming_state(self, token, proxy=None):
        url = f"{self.base_url}/farming/state"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def start_farming(self, token, proxy=None):
        url = f"{self.base_url}/farming/farm"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {} 
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, headers=headers, json=payload, proxy=proxy) as response:
                data = await response.json()
                finish_timestamp = data.get('timings', {}).get('finish')
                if finish_timestamp:
                    finish_time = datetime.fromtimestamp(finish_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    log(hju + f"Starting farm successfully")
                    log(hju + f"Farming end time: {pth}{finish_time}")
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def claim_farming(self, token, proxy=None):
        url = f"{self.base_url}/farming/claim"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {} 
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, headers=headers, json=payload, proxy=proxy) as response:
                if response.status == 200:                  
                    log(hju + f"Farm claimed successfully! ")
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def get_diamond_info(self, token, proxy=None):
        url = f"{self.base_url}/clicker/diamond/state"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    return await response.json()    
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def claim_diamond(self, token, diamond_number, total_reward, proxy=None):
        url = f"{self.base_url}/clicker/diamond/complete"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {"diamondNumber": diamond_number}
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload, headers=headers, proxy=proxy) as response:
                if response.status == 200:    
                    log(hju + f"Success claim {pth}{total_reward} {hju}diamonds!")
                    return response
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def get_task(self, token, proxy=None):
        url = f"{self.base_url}/hold/tasks"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(mrh + f"Error make request status {response.status}")

    async def start_task(self, token, task_id, slug, proxy=None):
        start_url = f"{self.base_url}/hold/tasks/{task_id}/start"
        verify_url = f"{self.base_url}/hold/tasks/{task_id}/verify"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "origin": "https://fintopio-tg.fintopio.com"
        }
        payload = {}

        try:
            async with aiohttp.ClientSession() as sess:
                start_response = await sess.post(start_url, headers=headers, json=payload, proxy=proxy)
                response_data = await start_response.json()
                if start_response.status == 200:
                    verify_response = await sess.post(verify_url, headers=headers, json=payload, proxy=proxy)
                    verify_data = await verify_response.json()
                    if verify_response.status == 201 and verify_data.get("status") == "verifying":
                        log(hju + f"Task {pth}{slug} is being verified!")
                    else:
                        log(kng + f"Failed to verify task {pth}{slug}: {verify_response.status}")
                elif start_response.status == 201:
                    log(hju + f"Task {bru}{slug} {hju}in progress & verifying. ")
                else:
                    log(kng + f"Failed to start task {pth}{slug}: {start_response.status} Response: {pth}{response_data}")
        except (Exception, AttributeError) as error:
            log(mrh + f"Error starting task: {kng}{str(error)}")

    async def claim_task(self, token, task_id, slug, reward_amount, proxy=None):
        url = f"{self.base_url}/hold/tasks/{task_id}/claim"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "origin": "https://fintopio-tg.fintopio.com"
        }
        payload = {} 
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.post(url, headers=headers, json=payload, proxy=proxy) as response:
                    response_data = await response.json()
                    if response.status == 201 and response_data.get("status") == "completed":
                        log(hju + f"Task {bru}{slug}{hju}, reward {pth}{reward_amount} {hju}diamonds!")
                    else:
                        log(mrh + f"Failed to claim task {bru}{slug}. Response: {pth}{response_data}")
        except (Exception, AttributeError) as error:
            log(mrh + f"Error claiming task: {kng}{str(error)}")

    def calculate_wait_time(self, first_account_finish_time):
        if not first_account_finish_time:
            return None
        now = datetime.now()
        finish_time = datetime.fromtimestamp(first_account_finish_time / 1000)
        duration = (finish_time - now).total_seconds()
        return duration * 1000  

    async def main(self):
        log_line()
        proxy_index = 0
        with open("data.txt", "r") as file:
            data = file.read().strip().split("\n")
        users = [user for user in data if user]

        first_account_finish_time = None
        log(hju + f"Number of accounts: {bru}{len(users)}")
        log(hju + f"Total Proxies: {pth}{len(self.proxies)}" if self.proxies else f"{pth}No proxies used")
        log_line()

        while True:
            try:
                for i, user_data in enumerate(users):
                    log(hju + f"Account: {bru}{i + 1}/{len(users)}")
                    proxy = None
                    if self.use_proxies and self.proxies:
                        proxy = self.proxies[proxy_index]
                        proxy_host = proxy.split('@')[-1]
                        log(hju + f"Proxy: {pth}{proxy_host}")
                        proxy_index = (proxy_index + 1) % len(self.proxies)
                    log(htm + "~" * 38)
                    token = await self.auth(user_data, proxy)
                    if token:
                        profile = await self.get_profile(token, proxy)
                        if profile:
                            if 'profile' in profile and 'telegramUsername' in profile['profile']:
                                username = profile['profile']['telegramUsername']
                                balance = profile['balance'].get('balance', 'N/A') 
                                log(hju + f"Username: {pth}{username}")
                                log(hju + f"Balance: {pth}{balance}")
                            await self.check_in_daily(token)
                            if self.auto_break_asteroid:
                                diamond = await self.get_diamond_info(token, proxy)
                                if diamond['state'] == 'available':
                                    log(hju + f"Trying to Break the Asteroid..")
                                    await countdown_timer(int((random.random() * (21 - 10)) + 10))
                                    await self.claim_diamond(token, diamond['diamondNumber'], diamond['settings']['totalReward'], proxy)
                                else:
                                    next_diamond_timestamp = diamond['timings'].get('nextAt')
                                    if next_diamond_timestamp:
                                        next_diamond_time = datetime.fromtimestamp(next_diamond_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                        log(hju + f"Next Asteroid: {pth}{next_diamond_time}")
                                        if i == 0:
                                            first_account_finish_time = next_diamond_timestamp

                            farming_state = await self.get_farming_state(token, proxy)
                            if farming_state:
                                current_state = farming_state.get('state', "N/A")
                                current_farmed = farming_state.get('farmed', 0)
                                reward_amount = farming_state.get('settings', "N/A").get('reward', 0)

                                if current_state == "idling":
                                    log(hju + "Farm is idling, starting farming session.")
                                    await self.start_farming(token, proxy)
                                elif current_state in ["farmed", "farming"]:
                                    finish_timestamp = farming_state['timings'].get('finish')
                                    if finish_timestamp:
                                        finish_time = datetime.fromtimestamp(finish_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                        log(hju + f"Currently farming: {pth}{current_farmed} {hju}/ {pth}{reward_amount}")
                                        log(hju + f"Farming end time: {pth}{finish_time}")

                                        current_time = datetime.now().timestamp() * 1000
                                        if current_time > finish_timestamp:
                                            log(hju + "Farming session has ended, claiming rewards.")
                                            await self.claim_farming(token, proxy)
                                            await self.start_farming(token, proxy)
                                        else:
                                            log(hju + "Farming session is still ongoing.")

                            if self.auto_complete_task:
                                task_state = await self.get_task(token, proxy)
                                if task_state:
                                    for item in task_state['tasks']:
                                        status = item['status']
                                        task_id = item['id']
                                        slug = item['slug']
                                        reward_amount = item['rewardAmount']

                                        if status == 'available':
                                            await self.start_task(token, task_id, slug, proxy)
                                        elif status == 'verified':
                                            await self.claim_task(token, task_id, slug, reward_amount, proxy)
                                        elif status == 'in-progress':
                                            log(hju + f"Task {bru}{slug}{hju} Skipping...")
                                        else:
                                            log(hju + f"Verifying task {bru}{slug}{hju} with status {pth}{status}!")

                    log_line()
                    await countdown_timer(self.account_delay)

                wait_time = self.calculate_wait_time(first_account_finish_time)
                if wait_time and wait_time > 0:
                    await countdown_timer(int(wait_time / 1000))
                else:
                    log(bru + f"Continuing loop immediately.")
                    log(htm + "~" * 38)
                    await countdown_timer(self.account_delay)

            except (ValueError, AttributeError, KeyError, aiohttp.ClientError) as e:
                log(f"An error occured check last.log!")
                log_error(f"{str(e)}")
                await asyncio.sleep(5)
            except Exception as e:
                log(f"An error occured check last.log!")
                log_error(f"{str(e)}")
                await asyncio.sleep(5) 