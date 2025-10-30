from sqlalchemy.orm import Session
from . import models, schemas, auth


# user


def get_user_by_email(db: Session, email: str):
return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
hashed = auth.get_password_hash(user.password)
db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed, role=user.role)
db.add(db_user)
db.commit()
db.refresh(db_user)
return db_user


# events


def create_event(db: Session, event: schemas.EventCreate, creator_id: int):
ev = models.Event(**event.dict(), creator_id=creator_id)
db.add(ev)
db.commit()
db.refresh(ev)
return ev


def get_events(db: Session, skip: int = 0, limit: int = 100):
return db.query(models.Event).offset(skip).limit(limit).all()


# teams


def create_team(db: Session, team: schemas.TeamCreate, creator_id: int):
t = models.Team(name=team.name, description=team.description, created_by=creator_id)
db.add(t)
db.commit()
db.refresh(t)
return t


def add_member_to_team(db: Session, team_id: int, user_id: int):
team = db.query(models.Team).filter(models.Team.id == team_id).first()
user = db.query(models.User).filter(models.User.id == user_id).first()
if team and user:
team.members.append(user)
db.commit()
return team
return None
