# setup_db.py
# Rohan Weeden
# June 14, 2018

# Database setup functions. Need to pull them out from lambda_function to avoid
# naming conflicts during unit test imports

from hyp3_db.hyp3_models.base import Base
from sqlalchemy.sql import text


ADD_USER_SQL = text("""
CREATE USER hyp3_user WITH PASSWORD :password;
GRANT ALL PRIVILEGES ON DATABASE hyp3db to hyp3_user;
""")


def setup_db(db):
    """ Creates hyp3 user as well as all database tables """
    db.engine.execute(ADD_USER_SQL, password="testpass")
    Base.metadata.create_all(db.engine)
