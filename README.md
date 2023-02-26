# gchtoken
A tool that automates getting tokens for Grand Chase History

# Usage
```sh
gchtoken [-h] (--interactive-login | --file-login file_path) TOKEN [TOKEN ...]

Automatically redeems tokens for GCH accounts

positional arguments:
  TOKEN                 The token itself

options:
  -h, --help            show this help message and exit
  --interactive-login   Login will be prompted
  --file-login file_path
                        Use a file containing TOML formatted login data, as "login = password"
```

## Interactive Login
```sh
python3 gchtoken.py --interactive-login TOKEN_1 TOKEN_2
```
A login and password inputs will be prompted in order to login. A question will
be asked in order to input more accounts or not.
Every given token will be redeemed for every successfully logged in account.
```sh
Username: username
Password: **********************************************
more? (y/n)
```
## File Login
```sh
python3 gchtoken.py --file-login ~/login_file.txt TOKEN_1 TOKEN_2
```
**or**
```sh
python3 gchtoken.py TOKEN_1 TOKEN_2 --file-login ~/login_file.txt
```
Will run the login process for every account that is present on `login_file.txt`
and redeem every given token for every successfully logged in account.
### Example: login file
```
username1 = "password1"
username2 = "password2"
...
usernameN = "passwordN"
```
