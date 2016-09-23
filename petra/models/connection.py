from petra.db import db
from petra.serializer import Serializer


class Connection(db.Model, Serializer):
    __tablename__ = 'Connections'

    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(80))
    plaid_token = db.Column(db.String(180))

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    accounts = db.relationship('Account')

    def __init__(self, account_type, plaid_token):
        self.account_type = account_type
        self.plaid_token = plaid_token
