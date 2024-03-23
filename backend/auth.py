import os
import logging

import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from schema import User

REGION = os.environ.get("REGION", "us-west-2")
USER_POOL_ID = os.environ.get("USER_POOL_ID", "us-west-2_slVtgO1Fl")
CLIENT_ID = os.environ.get("CLIENT_ID", "st1j43kamprg34hrcpfu3qvbc")

security = HTTPBearer()

logging.basicConfig(level=logging.INFO)


def verify_token(token: str) -> dict:
    # Verify JWT token
    url = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
    response = requests.get(url)
    keys = response.json()["keys"]
    header = jwt.get_unverified_header(token)
    key = [k for k in keys if k["kid"] == header["kid"]][0]
    decoded = jwt.decode(token, key, algorithms=["RS256"], audience=CLIENT_ID)
    return decoded

