from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum, Table
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime


class RoleEnum(str, enum.Enum):
student = 'student'
organizer = 'organizer'
faculty = 'faculty'
admin = 'admin'


# Association tables
team_members = Table(
'team_members', Base.metadata,
Column('team_id', Integer, ForeignKey('teams.id')),
Column('user_id', Integer, ForeignKey('users.id'))
)


class User(Base):
__tablename__ = 'users'
id = Column(Integer, primary_key=True, index=True)
email = Column(String, unique=True, index=True, nullable=False)
full_name = Column(String, nullable=True)
hashed_password = Column(String, nullable=False)
role = Column(Enum(RoleEnum), default=RoleEnum.student)
is_active = Column(Boolean, default=True)
created_at = Column(DateTime, default=datetime.utcnow)


teams = relationship('Team', secondary=team_members, back_populates='members')
events_created = relationship('Event', back_populates='creator')


class Event(Base):
__tablename__ = 'events'
id = Column(Integer, primary_key=True, index=True)
title = Column(String, index=True)
description = Column(Text)
location = Column(String, nullable=True)
start_time = Column(DateTime)
end_time = Column(DateTime)
capacity = Column(Integer, default=0)
creator_id = Column(Integer, ForeignKey('users.id'))
created_at = Column(DateTime, default=datetime.utcnow)


creator = relationship('User', back_populates='events_created')


class Team(Base):
__tablename__ = 'teams'
id = Column(Integer, primary_key=True, index=True)
name = Column(String, nullable=False)
description = Column(Text)
created_by = Column(Integer, ForeignKey('users.id'))
created_at = Column(DateTime, default=datetime.utcnow)


members = relationship('User', secondary=team_members, back_populates='teams')
