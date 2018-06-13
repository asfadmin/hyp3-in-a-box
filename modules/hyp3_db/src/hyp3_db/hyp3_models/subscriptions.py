# subscriptions/models.py
# Hal DiMarchi, Rohan Weeden
# June 7, 2017

# Database models for subscription table


from sqlalchemy import (
    Column,
    Integer,
    Text,
    Date,
    Boolean,
    ForeignKey,
    ARRAY
)
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql
from sqlalchemy import sql
from geoalchemy2 import Geography

from .base import Base
from .groups import subscriptions_in_groups


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)

    platform = Column(Text, nullable=False)
    name = Column(Text, nullable=False)

    polarization = Column(
        ARRAY(postgresql.TEXT()),
        nullable=False
    )
    orbit_dir = Column(Text, nullable=False)

    paths = Column(
        ARRAY(postgresql.INT4RANGE()),
        nullable=False
    )

    location = Column(
        Geography(geometry_type='MULTIPOLYGON', srid=4326),
        index=True,
        nullable=False
    )

    start_date = Column(Date)
    end_date = Column(Date)
    start_date_handled = Column(
        Boolean,
        nullable=False,
        server_default=sql.expression.text("false")
    )

    process_old = Column(Boolean, nullable=False)
    process_id = Column(
        ForeignKey('processes.id', deferrable=True, initially='DEFERRED'),
        nullable=False,
        index=True
    )

    user_id = Column(
        ForeignKey('users.id', deferrable=True, initially='DEFERRED'),
        nullable=False,
        index=True
    )

    crop_to_selection = Column(Boolean, nullable=False)
    extra_arguments = Column(Text)

    enabled = Column(
        Boolean,
        nullable=False,
        server_default=sql.expression.text("true")
    )

    project_id = Column(ForeignKey('projects.id'))
    description = Column(Text)
    priority = Column(
        Integer,
        nullable=False,
        server_default=sql.expression.text("10")
    )

    process = orm.relationship('Process')
    project = orm.relationship('Project')
    user = orm.relationship('User')
    groups = orm.relationship(
        'Group', secondary=subscriptions_in_groups, lazy='joined'
    )
