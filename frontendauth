from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from . import core
from .schemas import TokenData
from .database import get_db
from sqlalchemy.orm import Session
from . import models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def verify_password(plain_password, hashed_password):
return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
to_encode = data.copy()
if expires_delta:
expire = datetime.utcnow() + expires_delta
else:
expire = datetime.utcnow() + timedelta(minutes=core.ACCESS_TOKEN_EXPIRE_MINUTES)
to_encode.update({"exp": expire})
encoded_jwt = jwt.encode(to_encode, core.SECRET_KEY, algorithm=core.ALGORITHM)
return encoded_jwt


# dependency to get current user
from fastapi import Security


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
try:
payload = jwt.decode(token, core.SECRET_KEY, algorithms=[core.ALGORITHM])
email: str = payload.get("sub")
role: str = payload.get("role")
if email is None:
raise credentials_exception
token_data = TokenData(email=email, role=role)
except JWTError:
raise credentials_exception
user = db.query(models.User).filter(models.User.email == token_data.email).first()
if user is None:
raise credentials_exception
return user


# role guard
from fastapi import HTTPException


def require_role(role: str):
def role_checker(current_user = Depends(get_current_user)):
if current_user.role.value != role and current_user.role.value != 'admin':
raise HTTPException(status_code=403, detail='Operation not permitted')
return current_user
return role_checker
