# processes/models.py
# Rohan Weeden
# Created June 7, 2017

from sqlalchemy import Boolean, Column, Float, Integer, Text, sql

from .base import Base


class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    suffix = Column(Text, nullable=False)
    enabled = Column(
        Boolean,
        nullable=False,
        server_default=sql.expression.text("true")
    )

    product_type = Column(Text)
    database_info_required = Column(Boolean, nullable=False)
    description = Column(Text, nullable=False)

    ami_id = Column(Text, nullable=False)
    ec2_size = Column(Text, nullable=False)

    script = Column(Text, nullable=False)
    supports_pair_processing = Column(Boolean, nullable=False)
    supports_time_series_processing = Column(
        Boolean,
        nullable=False,
        server_default=sql.expression.text("false")
    )

    maximum_area = Column(Float(53))
    text_id = Column(Text, nullable=False, unique=True)

    time_series_window_days = Column(Integer)
    requires_dual_pol = Column(
        Boolean,
        nullable=False,
        server_default=sql.expression.text("false")
    )
