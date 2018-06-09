# models.py
# Hal DiMarchi, Rohan Weeden
# Created May 25, 2017

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Boolean,
    Table,
    ForeignKey
)
from sqlalchemy import orm
from sqlalchemy import sql

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False)
    last_login = Column(DateTime(True))
    is_admin = Column(Boolean, nullable=False, default=False)
    is_authorized = Column(Boolean, nullable=False, default=False)
    granules_processed = Column(Integer, nullable=False, default=0)
    max_granules = Column(Integer)
    priority = Column(Integer, nullable=False,
                      server_default=sql.expression.text("10"))
    can_expedite = Column(Boolean, server_default=sql.expression.text("false"))
    wants_email = Column(Boolean, server_default=sql.expression.text("true"))


users_member_of_projects = Table(
    'users_member_of_projects',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(ForeignKey('users.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)
    create_time = Column(DateTime(
        True), nullable=False, server_default=sql.func.now())

    owner = orm.relationship('User')
    users = orm.relationship(
        'User', secondary=users_member_of_projects, lazy='joined')


class OneTimeAction(Base):
    __tablename__ = 'one_time_actions'

    id = Column(Integer, primary_key=True)
    hash = Column(Text, nullable=False, unique=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    action = Column(Text, nullable=False)
    params = Column(Text)
    expires = Column(DateTime(True), server_default=sql.expression.text(
        "(now() + interval '30 days')"))
    enabled = Column(Boolean, nullable=False,
                     server_default=sql.expression.text('true'))

    user = orm.relationship('User')
