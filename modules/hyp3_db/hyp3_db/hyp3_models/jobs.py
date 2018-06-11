# jobs/models.py
# Rohan Weeden
# Created: June 7, 2017

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    DateTime,
    String,
    ARRAY
)
from sqlalchemy import sql
from sqlalchemy import orm

from .base import Base


class LocalQueue(Base):
    __tablename__ = 'local_queue'

    id = Column(Integer, primary_key=True, autoincrement=True)

    sub_id = Column(ForeignKey('subscriptions.id'))
    user_id = Column(ForeignKey('users.id'), nullable=False)
    process_id = Column(ForeignKey('processes.id'), nullable=False)

    process = orm.relationship('Process')
    sub = orm.relationship('Subscription')
    user = orm.relationship('User')

    granule = Column(Text, nullable=False)
    granule_url = Column(Text, nullable=False)
    other_granules = Column(Text)
    other_granule_urls = Column(Text)

    request_time = Column(DateTime(True), nullable=False)
    priority = Column(Integer, nullable=False,
                      server_default=sql.expression.text("10"))
    status = Column(
        String(20),
        nullable=False,
        server_default=sql.expression.text("'QUEUED'::character varying")
    )
    message = Column(Text)
    processed_time = Column(DateTime(True))


class TimeSeriesData(Base):
    __tablename__ = 'time_series_info'

    job_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=False
    )
    granules = Column(
        ARRAY(String(67)),
        nullable=False
    )
    swath = Column(Integer)
    stages = Column(ARRAY(String(255)), nullable=False)

    coherence_threshold = Column(Float)
    atmo_filter_length = Column(Float)
    percent_coherent_images = Column(Float)
