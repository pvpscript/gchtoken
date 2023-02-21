import re
import sys
import string
import urllib
import random

from requests import Session
from dataclasses import dataclass
from getpass import getpass
from typing import Optional, Type, Dict, Any, List
from types import TracebackType

from html.parser import HTMLParser
from collections.abc import Iterator, Sequence

@dataclass
class Account:
    username: str
    password: str

class Login:
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

class TokenHandler:
    TOKEN_URL = "https://chasehistory.net/Token/Redeem"

    class _SuccessParser(HTMLParser):
        _div_tag = False
        _content_flag = False
        _success_data = None

        def _is_token_form(
            self,
            tag: str,
            attrs: Sequence[tuple[Any, ...]]
        ) -> bool:
            return (tag == "div" and attrs[0][0] == "class" and
                    attrs[0][1].split(' ')[0] == "token-redeem-content-form")

        def handle_starttag(
            self,
            tag: str,
            attrs: Sequence[tuple[Any, ...]]
        ) -> None:
            if not self._div_tag:
                if self._is_token_form(tag, attrs):
                    self._div_tag = True
            elif tag == "pre":
                self._content_flag = True

        def handle_data(self, data: str):
            if self._content_flag:
                self._content_flag = False
                self._success_data = data

        @property
        def success_data(self):
            return self._success_data

    def __init__(self, tokens: List[str] = []):
        self._tokens = tokens

    def _parse_token_content(self, html: str) -> str:
        parser = self._SuccessParser()
        parser.feed(html)

        return parser.success_data

    def _redeem_token(self, account_session: Session, token: str) -> str:
        token_data = {'token': token}
        token_res = account_session.post(url=self.TOKEN_URL,
                                         data=token_data)

        if (code := token_res.status_code) != 200:
            print(f"Request error. Status: {code}", file=sys.stderr)
            return None

        pattern = "_alert\(\"(.*)\"\);"
        if len(err_data := re.findall(pattern, token_res.text)) > 0:
            return err_data[0]
        else:
            return self._parse_token_content(token_res.text)

    def redeem_tokens(self, session: Session) -> None:
        for token in self._tokens:
            result = self._redeem_token(session, token).rstrip()

            print(f"Token: {token}")
            print(f"{result}\n")


if __name__ == '__main__':
    accounts = []
    while True:
        username = input("Username: ")
        password = getpass("Password: ")

        accounts.append(
            Account(username=username, password=password)
        )

        if input("more? (y/n)").lower() != 'y':
            break

    token_handler = TokenHandler(tokens=sys.argv[1:])

    with Login(accounts) as login:
        login_result = login.login_all()

        for username, session in login_result.items():
            print(f"Redeeming for username: {username}")
            token_handler.redeem_tokens(session)

            print("--------------------\n")

