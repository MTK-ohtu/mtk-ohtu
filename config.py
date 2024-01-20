from os import getenv

SECRET_KEY = getenv("SECRET_KEY")

if SECRET_KEY in (None, "PUT_THE_KEY_HERE"):
    raise Exception("Missing SECRET_KEY enviroment variable.")