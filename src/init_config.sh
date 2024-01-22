#!/bin/sh

#Create SECRET_KEY for flask-app
KEY=$(python3 -c "import secrets; print(secrets.token_hex())")

#Save key to .env
echo "SECRET_KEY=$KEY" > .env