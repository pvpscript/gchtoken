import sys
import string
import urllib
import random

from .account import Account

from requests import Session
from typing import Optional, Type, Dict
from types import TracebackType

class LoginHandler:
    LOGIN_URL = "https://chasehistory.net/Auth/Login"

    def __init__(self, accounts: list[Account]):
        self._accounts = accounts

        self._sessions = {}

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> bool:
        for _, v in self._sessions.items():
            v.close()

    def _generate_phpsessid(self) -> str:
        return ''.join(random.choice(string.ascii_lowercase + string.digits)
                       for _ in range(26))

    def _cookies(self) -> dict[str, str]:
        phpsessid = self._generate_phpsessid()

        return {
            'PHPSESSID': phpsessid
        }

    def _login(self, account: Account) -> Optional[Session]:
        username = account.username
        login_data = {
            'login': username,
            'password': account.password,
        }

        cookies = self._cookies()

        self._sessions[username] = (session := Session())
        login_res = session.post(url=self.LOGIN_URL,
                                 cookies=cookies,
                                 data=login_data)

        if (code := login_res.status_code) != 200:
            print(f"Request error. Status: {code}", file=sys.stderr)
            return None 

        login_res_dict = login_res.json()

        if (login_res_dict := login_res.json())['code'] == 0:
            print(f"Login error for '{username}': {login_res_dict['msg']}",
                  file=sys.stderr)
            return None 

        print(f"Login successful for username: {username}")

        return session


    def login(username: str) -> Optional[Session]:
        if (acc := next((i for i in accounts if i.username == username), None)):
            return None

        return self._login(acc)

    def login_all(self) -> Dict[str, Session]:
        return {account.username: self._login(account)
                for account in self._accounts}
