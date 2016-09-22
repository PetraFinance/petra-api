from flask import Blueprint

from petra.jsend import success
from petra.plaid_client import client

finance = Blueprint('finance', __name__)


@finance.route('/institutions')
def institutions():
    data = client.institutions().json()
    return success(data)


@finance.route('/categories')
def categories():
    data = client.categories().json()
    return success(data)
