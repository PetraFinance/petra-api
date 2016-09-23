from petra.db import db
from petra.serializer import Serializer


class Account(db.Model, Serializer):
    __tablename__ = 'Accounts'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(80), unique=True, nullable=False)

    available_balance = db.Column(db.Integer, nullable=False)
    current_balance = db.Column(db.Integer, nullable=False)

    name = db.Column(db.String(180))
    number = db.Column(db.Integer)
    limit = db.Column(db.Integer)
    type = db.Column(db.String(80), nullable=False)
    subtype = db.Column(db.String(80))

    connection_id = db.Column(db.Integer, db.ForeignKey('Connections.id'))
