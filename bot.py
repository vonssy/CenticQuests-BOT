from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, random, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Centic:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Host": "develop.centic.io",
            "Origin": "https://centic.io",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        
        self.BASE_API = "https://develop.centic.io"
        self.API_KEY = "dXoriON31OO1UopGakYO9f3tX2c4q3oO7mNsjB2nJsKnW406"
        self.ref_code = "eJwFwQERACAIBLBKwINCHPDeDMZ3k0ec4q1GsTgSaYxR32LrNMMcyDDtDwSCC20=" # U can change it with yours.
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.api_keys = {}

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
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    def generate_address(self, account: str):
        try:
            local_account = Account.from_key(account)
            address = local_account.address

            return address
        except Exception as e:
            return None
        
    def generate_payload(self, account: str, address: str):
        try:
            nonce = random.randint(10000, 999999)

            message = f"I am signing my one-time nonce: {nonce}.\n\nNote: Sign to log into your Centic account. This is free and will not require a transaction."
            encoded_message = encode_defunct(text=message)

            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            payload = {
                "address": address, 
                "nonce": nonce, 
                "signature": signature
            }

            return payload
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")
    
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None
    
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxyscrape Free Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Proxyscrape Free" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def user_login(self, account: str, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/dev/v3/auth/login"
        data = json.dumps(self.generate_payload(account, address))
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Apikey": self.API_KEY
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Error     :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
        
    async def user_confirm(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/ctp-api/centic-points/invites"
        data = json.dumps({"referralCode":self.ref_code})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Apikey": self.api_keys[address]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Error     :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Confirm Invite Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
    
    async def user_info(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/ctp-api/centic-points/user-info"
        headers = {
            **self.headers,
            "Content-Type": "application/json",
            "X-Apikey": self.api_keys[address]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Error     :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} GET CTP Points Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                
    async def user_tasks(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/ctp-api/centic-points/tasks"
        headers = {
            **self.headers,
            "Content-Type": "application/json",
            "X-Apikey": self.api_keys[address]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Error     :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} GET Task Lists Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
            
    async def claim_tasks(self, address: str, task_id: str, title: str, reward: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/ctp-api/centic-points/claim-tasks"
        data = json.dumps({"taskId":task_id, "point":reward})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "X-Apikey": self.api_keys[address]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Not Completed:{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
    
    async def process_user_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy     :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            login = await self.user_login(account, address, proxy)
            if login:
                self.api_keys[address] = login["apiKey"]

                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status    :{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
                )
                return True

            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)
                await asyncio.sleep(5)
                continue

            return False
                
    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_user_login(account, address, use_proxy, rotate_proxy)
        if logined:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
        
            await self.user_confirm(address, proxy)

            user = await self.user_info(address, proxy)
            if user:
                balance = user.get("totalPoint", 0)
                
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Balance   :{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {balance} CTP {Style.RESET_ALL}"
                )

            tasks = await self.user_tasks(address, proxy)
            if not tasks:
                return
            
            self.log(f"{Fore.CYAN + Style.BRIGHT}Task Lists:{Style.RESET_ALL}")
            
            all_tasks = []
            for key, value in tasks.items():
                if isinstance(value, list):
                    all_tasks.extend(value)
                elif isinstance(value, dict):
                    all_tasks.append(value)

            for task in all_tasks:
                if task:
                    task_id = task["_id"]
                    title = task["name"]
                    reward = task["point"]
                    is_claimed = task.get("claimed", None)

                    if is_claimed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                        )
                        continue

                    claim = await self.claim_tasks(address, task_id, title, reward, proxy)
                    if claim and claim.get("message") == "successfully":
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Completed Successfully{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Reward:{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {reward} CTP {Style.RESET_ALL}"
                        )

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]

            use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies(use_proxy_choice)

                separator = "=" * 25
                for account in accounts:
                    if account:
                        address = self.generate_address(account)
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        if not address:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}Status    :{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            continue

                        await self.process_accounts(account, address, use_proxy, rotate_proxy)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                
                delay = 12 * 60 * 60
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT}All Accounts Have Been Processed...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1

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