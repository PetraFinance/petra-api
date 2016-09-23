from petra.db import db
from petra.serializer import Serializer


class User(db.Model, Serializer):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    connections = db.relationship('Connection')

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email
