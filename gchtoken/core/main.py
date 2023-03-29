import sys

from getpass import getpass

from gchtoken.login.account import Account
from gchtoken.login.login_handler import LoginHandler
from gchtoken.gch_token.token_handler import TokenHandler
from gchtoken.core.input_parser import make_parser

def main():
    parser = make_parser()
    args = parser.parse_args()

    token_handler = TokenHandler(tokens=args.tokens)

    with LoginHandler() as login:
        if args.interactive_login:
            login.interactive_login()
        else:
            login.file_login(args.file_login[0])

        login_result = login.login_all()

        for username, session in login_result.items():
            print(f"Redeeming for username: {username}")
            token_handler.redeem_tokens(session)

            print("--------------------\n")

    return 0
