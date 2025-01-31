from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from eth_account import Account
from eth_account.messages import encode_defunct
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, random, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Centic:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Host': 'develop.centic.io',
            'Origin': 'https://centic.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': FakeUserAgent().random
        }
        self.code = 'eJwFwQERACAIBLBKwINCHPDeDMZ3k0ec4q1GsTgSaYxR32LrNMMcyDDtDwSCC20='

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
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Centic Quests - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def generate_address(self, account: str):
        try:
            local_account = Account.from_key(account)
            address = local_account.address

            return address
        except Exception as e:
            return None, None
        
    def generate_payload(self, account: str, address: str):
        try:
            nonce = random.randint(10000, 999999)

            message = f"I am signing my one-time nonce: {nonce}.\n\nNote: Sign to log into your Centic account. This is free and will not require a transaction."
            encoded_message = encode_defunct(text=message)

            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = signed_message.signature.hex()

            data = {
                "address": address, 
                "nonce": nonce, 
                "signature": signature
            }

            return data
        except Exception as e:
            return None
    
    def mask_account(self, account):
        mask_account = account[:6] + '*' * 6 + account[-6:]
        return mask_account
    
    async def user_login(self, account: str, address: str, retries=5):
        url = 'https://develop.centic.io/dev/v3/auth/login'
        data = json.dumps(self.generate_payload(account, address))
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Apikey': 'dXoriON31OO1UopGakYO9f3tX2c4q3oO7mNsjB2nJsKnW406'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['apiKey']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return None
        
    async def user_confirm(self, apikey: str, retries=5):
        url = 'https://develop.centic.io/ctp-api/centic-points/invites'
        data = json.dumps({'referralCode':self.code})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Apikey': apikey
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return None
    
    async def user_info(self, apikey: str, retries=5):
        url = 'https://develop.centic.io/ctp-api/centic-points/user-info'
        headers = {
            **self.headers,
            'Content-Type': 'application/json',
            'X-Apikey': apikey
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return None
                
    async def user_tasks(self, apikey: str, retries=5):
        url = 'https://develop.centic.io/ctp-api/centic-points/tasks'
        headers = {
            **self.headers,
            'Content-Type': 'application/json',
            'X-Apikey': apikey
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return None
                
    async def claim_tasks(self, apikey: str, task_id: str, reward: int, retries=5):
        url = 'https://develop.centic.io/ctp-api/centic-points/claim-tasks'
        data = json.dumps({'taskId':task_id, 'point':reward})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Apikey': apikey
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 400:
                            return None
                        
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return None
                
    async def process_accounts(self, account: str, address: str):
        apikey = await self.user_login(account, address)
        if not apikey:
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Status    :{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Login Failed {Style.RESET_ALL}"
            )
            return
        
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Status    :{Style.RESET_ALL}"
            f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
        )
        
        await self.user_confirm(apikey)

        balance = "N/A"
        user = await self.user_info(apikey)
        if user:
            balance = user.get('totalPoint', 0)
            
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Balance   :{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {balance} CTP {Style.RESET_ALL}"
        )

        tasks = await self.user_tasks(apikey)
        if not tasks:
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Task Lists:{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
            )
            return
        
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Task Lists:{Style.RESET_ALL}"
        )
        
        all_tasks = []
        for key, value in tasks.items():
            if isinstance(value, list):
                all_tasks.extend(value)
            elif isinstance(value, dict):
                all_tasks.append(value)

        for task in all_tasks:
            if task:
                task_id = task['_id']
                title = task['name']
                reward = task['point']
                is_claimed = task.get('claimed', None)

                if is_claimed:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    ->{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Is Already Claimed{Style.RESET_ALL}"
                    )
                    continue

                claim = await self.claim_tasks(apikey, task_id, reward)
                if claim and claim.get("message") == 'successfully':
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    ->{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {reward} CTP {Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    ->{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                    )

                await asyncio.sleep(1)

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                separator = "=" * 20
                for account in accounts:
                    if account:
                        address = self.generate_address(account)
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )
                        await self.process_accounts(account, address)
                        await asyncio.sleep(3)     

                
                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*62)
                seconds = 12 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = Centic()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Centic Quests - BOT{Style.RESET_ALL}",                                       
        )