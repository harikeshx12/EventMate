from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import RoleEnum


class Token(BaseModel):
access_token: str
token_type: str


class TokenData(BaseModel):
email: Optional[str] = None
role: Optional[str] = None


class UserBase(BaseModel):
email: EmailStr
full_name: Optional[str] = None


class UserCreate(UserBase):
password: str
role: Optional[RoleEnum] = RoleEnum.student


class UserOut(UserBase):
id: int
role: RoleEnum
is_active: bool
class Config:
orm_mode = True


class EventCreate(BaseModel):
title: str
description: Optional[str] = None
location: Optional[str] = None
start_time: datetime
end_time: datetime
capacity: Optional[int] = 0


class EventOut(EventCreate):
id: int
creator_id: int
created_at: datetime
class Config:
orm_mode = True


class TeamCreate(BaseModel):
name: str
description: Optional[str] = None


class TeamOut(TeamCreate):
id: int
members: List[UserOut] = []
class Config:
orm_mode = True
