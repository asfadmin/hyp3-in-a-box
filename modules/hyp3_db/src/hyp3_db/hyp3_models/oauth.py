# oauth.py
# Rohan Weeden, William Horn
# Created: June 7, 2017

# Database models for authentication table

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Text,
    orm,
    sql
)

from .base import Base


class ApiKey(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True)

    hash = Column(Text, nullable=False, unique=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)

    enabled = Column(
        Boolean,
        server_default=sql.expression.text("true"),
        nullable=False
    )

    user = orm.relationship('User')
