import os
from typing import Callable
import logging

from auth import verify_token
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from route import router
from schema import User
from starlette.types import ASGIApp
from utils import is_running_on_lambda
from pydantic import ValidationError

CORS_ALLOW_ORIGINS = os.environ.get("CORS_ALLOW_ORIGINS", "*")

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s - %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(router)

# NOTE: 組織のセキュリティポリシーに従い、適切にCORSを設定してください
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def error_handler_factory(status_code: int) -> Callable[[Exception], JSONResponse]:
    def error_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse({"errors": [str(exc)]}, status_code=status_code)

    return error_handler


app.add_exception_handler(ValueError, error_handler_factory(400))
app.add_exception_handler(TypeError, error_handler_factory(400))
app.add_exception_handler(Exception, error_handler_factory(500))
app.add_exception_handler(ValidationError, error_handler_factory(422))

security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded = verify_token(token.credentials)
        # Return user information
        return User(
            id=decoded["sub"],
            name=decoded["cognito:username"],
        )
    except (IndexError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

@app.middleware("http")
def add_current_user_to_request(request: Request, call_next: ASGIApp):
    if is_running_on_lambda():
        
        authorization = request.headers.get("Authorization")
        if authorization:
            token_str = authorization.split(" ")[1]
            token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_str)
            request.state.current_user = get_current_user(token)
    else:
        request.state.current_user = User(id="test_user", name="test_user")

    response = call_next(request)
    return response