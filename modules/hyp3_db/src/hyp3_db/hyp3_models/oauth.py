# oauth.py
# Rohan Weeden, William Horn
# Created: June 7, 2017

# Database models for authentication table
import string
import random

from passlib.hash import pbkdf2_sha512
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

    @classmethod
    def generate_new(cls, user_id):
        key = make_new_api_key()

        return key, cls(
            user_id=user_id,
            hash=get_hashed(key)
        )


def make_new_api_key():
    valid_characters = string.ascii_letters + string.digits
    seed = random.SystemRandom()

    key = ''.join(
        seed.choice(valid_characters) for _ in range(64)
    )

    return key


def get_hashed(api_key):
    return pbkdf2_sha512.encrypt(api_key, salt_size=16)
