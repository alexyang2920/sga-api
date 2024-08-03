import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer


# declare that the token url is '/api/auth/token'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


# To get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "10c6b69df90c84ed7253106f928c39553141ad644a61c28a059251ea1763f8b3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def parse_access_token(token: str):
    try:
      return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except InvalidTokenError:
        return None

