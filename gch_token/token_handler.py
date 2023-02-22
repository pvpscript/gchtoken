import re
import sys

from requests import Session
from typing import Any, List

from html.parser import HTMLParser
from collections.abc import Iterator, Sequence

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
