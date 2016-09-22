import requests
from flask import abort, Blueprint, request, session

from petra.config import config
from petra.db import db
from petra.jsend import error, fail, success
from petra.models import User

auth = Blueprint('auth', __name__)


@auth.route('/redirect')
def oauth_redirect():
    return success('https://www.facebook.com/dialog/oauth?'
                   'client_id={}&redirect_uri={}&scope=email'.format(
                       config['FACEBOOK']['APP_ID'],
                       config['FACEBOOK']['REDIRECT_URI'],
                   ))


@auth.route('/callback')
def oauth_callback():
    code = request.args.get('code', '')

    if not code:
        return abort(404)

    r = requests.get('https://graph.facebook.com/v2.3/oauth/access_token',
                     params={
                         'client_id': config['FACEBOOK']['APP_ID'],
                         'client_secret': config['FACEBOOK']['APP_SECRET'],
                         'redirect_uri': config['FACEBOOK']['REDIRECT_URI'],
                         'code': code,
                     })

    data = r.json()

    if 'error' in data:
        return fail(data['error']['message'])

    access_token = data.get('access_token', None)

    if not access_token:
        return error('Didn\'t receive access token?')

    session['fb_token'] = access_token

    return success(access_token)


@auth.route('/register', methods=['POST'])
def new_account():
    access_token = session.get('fb_token', None)
    if access_token is None:
        return fail('No login token')

    r = requests.get('https://graph.facebook.com/v2.3/me',
                     params={
                         'fields': 'email,first_name,last_name',
                         'access_token': access_token,
                     })

    data = r.json()

    if 'error' in data:
        return fail(data['error']['message'])

    email = data.get('email', None)
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)

    if not email or not first_name or not last_name:
        return fail('Missing fields')

    user = User.query.filter_by(email=email).first()

    if user:
        return fail('User already exists')

    user = User(
        name='{} {}'.format(first_name, last_name),
        email=email,
    )

    db.session.add(user)
    db.session.commit()

    session['email'] = email
    return success(user)


@auth.route('/login', methods=['POST'])
def login():
    if session.get('email', None):
        return fail('Already logged in')

    access_token = session.get('fb_token', None)
    if access_token is None:
        return fail('No facebook access token')

    r = requests.get('https://graph.facebook.com/v2.3/me',
                     params={
                         'fields': 'email',
                         'access_token': access_token,
                     })

    data = r.json()

    if 'error' in data:
        return fail(data['error']['message'])

    email = data.get('email', None)

    if not email:
        return fail('Bad response from facebook API')

    user = User.query.filter_by(email=email).first()

    if not user:
        return fail('No account')

    session['email'] = email
    return success(user)
