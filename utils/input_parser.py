import argparse

def make_parser():
    parser = argparse.ArgumentParser(
        prog="gchtoken",
        description="Automatically redeems tokens for GCH accounts"
    )

    parser.add_argument('tokens',
                        metavar='TOKEN', type=str, nargs='+',
                        help='The token itself')

    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument('--interactive-login',
                            dest='interactive_login', action='store_true',
                            help='Login will be prompted')
    file_group.add_argument('--file-login',
                            nargs=1, dest='file_login', metavar='file_path',
                            help=('Use a file containing TOML formatted '
                                  'login data, as "login = password"'))

    return parser
