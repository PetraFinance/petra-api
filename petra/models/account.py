from petra.db import db
from petra.serializer import Serializer


class Account(db.Model, Serializer):
    __tablename__ = 'Accounts'

    id = db.Column(db.Integer, primary_key=True)

    connection_id = db.Column(db.Integer, db.ForeignKey('Connections.id'))

    def __init__(self):
        pass
