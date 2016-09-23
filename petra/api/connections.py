from flask import Blueprint, g, request

from petra.db import db
from petra.jsend import fail, success
from petra.models import Connection, Account
from petra.plaid_client import client
from petra.check_login import user_required

connections = Blueprint('connections', __name__)


def login_succeeded():
    connection = Connection(
        institution=None,
        plaid_token=client.access_token,
    )

    data = client.connect_get().json()

    user = g.user

    user.connections.append(connection)
    for account in data['accounts']:
        connection.institution = account['institution_type']
        account = Account(
            unique_id=account['_id'],
            available_balance=account['balance']['available'],
            current_balance=account['balance']['current'],
            name=account.get('meta', dict()).get('name', None),
            number=account.get('meta', dict()).get('number', None),
            limit=account.get('meta', dict()).get('limit', None),
            type=account['type'],
            subtype=account.get('subtype', None),
        )
        connection.accounts.append(account)

    db.session.add(user)
    db.session.commit()
    return success(connection)


@connections.route('/new', methods=['POST'])
@user_required
def new_connection():
    public_token = request.form.get('public_token', None)
    if public_token is None:
        return fail('Missing fields: public_token')

    client.exchange_token(public_token)

    return login_succeeded()
