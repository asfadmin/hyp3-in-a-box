from sqlalchemy import (REAL, VARCHAR, BigInteger, Boolean, Column, DateTime,
                        ForeignKey, Integer, Text, orm)

from .base import Base
from .groups import subscriptions_in_groups


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)

    subscription_id = Column(
        ForeignKey('subscriptions.id', deferrable=True, initially='DEFERRED'),
        index=True
    )

    name = Column(Text, nullable=False)

    hash = Column(Text, nullable=False)
    size = Column(BigInteger, nullable=False)
    hash_type = Column(Text, nullable=False)

    creation_date = Column(
        DateTime(True), nullable=False
    )
    user_id = Column(
        ForeignKey('users.id', deferrable=True, initially='DEFERRED'),
        index=True
    )

    browse_url = Column(Text)
    process_id = Column(
        ForeignKey('processes.id', deferrable=True, initially='DEFERRED')
    )

    proc_node_type = Column(Text)
    local_queue_id = Column(Integer)
    ok_to_duplicate = Column(
        Boolean, nullable=False, server_default='false'
    )

    subscription = orm.relationship('Subscription')
    user = orm.relationship('User')

    groups = orm.relationship(
        'Group',
        secondary=subscriptions_in_groups,
        primaryjoin="subscriptions_in_groups.c.sub_id == Product.subscription_id",
        lazy="joined"
    )


class Browse(Base):
    __tablename__ = 'browse'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(VARCHAR(32), nullable=False)

    product_id = Column(
        ForeignKey('products.id', deferrable=True, initially='DEFERRED'),
        index=True,
        nullable=False
    )

    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    epsg = Column(Integer)

    lat_min = Column(REAL)
    lat_max = Column(REAL)
    lon_min = Column(REAL)
    lon_max = Column(REAL)

    resolution = Column(VARCHAR(32))

    product = orm.relationship(
        'Product', backref=orm.backref('browse', lazy='joined')
    )
