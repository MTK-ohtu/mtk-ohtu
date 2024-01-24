from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
DATABASE_URL= getenv("DATABASE_URL")
DATABASE_NAME= getenv("DATABASE_NAME")
DATABASE_USER= getenv("DATABASE_USER")
DATABASE_PASSWORD= getenv("DATABASE_PASSWORD")

if SECRET_KEY in (None, "PUT_THE_KEY_HERE"):
    raise Exception("Missing SECRET_KEY enviroment variable.")