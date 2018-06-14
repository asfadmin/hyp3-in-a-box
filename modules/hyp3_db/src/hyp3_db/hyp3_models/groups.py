# groups/models.py
# Rohan Weeden
# Created: November 05, 2017

# Database models for groups

from sqlalchemy import (VARCHAR, Boolean, Column, ForeignKey, Integer, Table,
                        Text, orm, sql)

from .base import Base

subscriptions_in_groups = Table(
    'subscriptions_in_groups',
    Base.metadata,
    Column('sub_id', Integer, ForeignKey('subscriptions.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)


users_member_of_groups = Table(
    'users_member_of_groups',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text)
    is_public = Column(
        Boolean,
        nullable=False,
        server_default=sql.expression.text("false")
    )
    icon = Column(Text)

    subscriptions = orm.relationship(
        "Subscription",
        secondary=subscriptions_in_groups,
        lazy='joined'
    )

    users = orm.relationship(
        "User",
        secondary=users_member_of_groups,
        lazy='joined'
    )
    owner = orm.relationship('User')
