# oauth/models.py
# Rohan Weeden
# Created: June 7, 2017

# Database models for authentication table

from app import db


class ApiKey(db.Model):
    __tablename__ = 'api_keys'

    id =        db.Column(db.Integer, primary_key=True)
    hash =      db.Column(db.Text, nullable=False, unique=True)
    user_id =   db.Column(db.ForeignKey('users.id'), nullable=False)
    enabled =   db.Column(db.Boolean, server_default=db.text("true"), nullable=False)

    user =      db.relationship('User')
