from petra.db import db
from petra.serializer import Serializer


class Connection(db.Model, Serializer):
    __tablename__ = 'Connections'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(80), nullable=False)
    plaid_token = db.Column(db.String(180), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    accounts = db.relationship('Account', lazy='dynamic')
