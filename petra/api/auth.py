import requests
from flask import abort, Blueprint, redirect, request, session

from petra.secrets import facebook
from petra.jsend import error, fail, success

auth = Blueprint('auth', __name__)


@auth.route('/redirect')
def redirect():
    return success('https://www.facebook.com/dialog/oauth?'
                   'client_id={}&redirect_uri={}&scope=email'.format(
                       facebook['app_id'], facebook['redirect_uri']
                   ))


@auth.route('/callback')
def callback():
    code = request.args.get('code', '')

    if not code:
        return abort(404)

    r = requests.get('https://graph.facebook.com/v2.3/oauth/access_token',
        params={
            'client_id': facebook['app_id'],
            'client_secret': facebook['app_secret'],
            'redirect_uri': facebook['redirect_uri'],
            'code': code,
        }
    )

    data = r.json()

    if 'error' in data:
        return fail(data['error']['message'])

    access_token = data.get('access_token', None)

    if not access_token:
        return error('Didn\'t receive access token?')

    session['fb_token'] = access_token

    return success(access_token)


@auth.route('/email')
def email():
    access_token = session.get('fb_token', '')
    if not access_token:
        return fail('No login token')
    
    r = requests.get('https://graph.facebook.com/v2.3/me',
        params={
            'fields': 'email',
            'access_token': access_token,
        },
    )

    data = r.json()

    if 'error' in data:
        return fail(data['error']['message'])

    session['email'] = data.get('email')

    return success(data)
