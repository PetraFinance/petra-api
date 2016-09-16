import requests
from flask import abort, Blueprint, request, session

from petra.config import config
from petra.db import db
from petra.jsend import error, fail, success
from petra.models import User
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
