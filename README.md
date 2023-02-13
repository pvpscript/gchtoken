# gchtoken
A tool that automates getting tokens for Grand Chase History

# How To Use
As of now, just run it with python3, providing each token as arguments.
After that, just provide the credentials asked from.

```sh
python3 gchtoken.py token1 [token2 [token3 [... [tokenN]]]]
```

# TODO
1. Create `Token` class to handle tokens for a given Login and separate each class in its own file (will need refactoring)
2. Add parameters with argparse: (-l --login [ask for login credentials]; -a --accounts accounts-file.txt [parse an account file, that contains logins and passwords, in the toml format (use tomllib)]
3. Add toml file parsing
4. Improve readme for the new features
