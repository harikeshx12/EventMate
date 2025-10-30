from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, auth, schemas


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post('/register', response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
existing = crud.get_user_by_email(db, user.email)
if existing:
raise HTTPException(status_code=400, detail='Email already registered')
return crud.create_user(db, user)


@router.post('/token', response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
user = crud.get_user_by_email(db, form_data.username)
if not user or not auth.verify_password(form_data.password, user.hashed_password):
raise HTTPException(status_code=401, detail='Incorrect username or password')
access_token = auth.create_access_token(data={"sub": user.email, "role": user.role.va
