import sys

from getpass import getpass

from login.account import Account
from login.login_handler import LoginHandler

from gch_token.token_handler import TokenHandler
from utils.input_parser import make_parser

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

    with LoginHandler(accounts) as login:
        login_result = login.login_all()

        for username, session in login_result.items():
            print(f"Redeeming for username: {username}")
            token_handler.redeem_tokens(session)

            print("--------------------\n")

