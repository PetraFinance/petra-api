import json
from unittest.mock import Mock, patch

import flask

from petra.db import db
from petra.models import User


def test_redirect(app):
    with app.test_client() as c:
        resp = c.get('/auth/redirect')
        parsed = json.loads(resp.data.decode('utf-8'))

        assert 'https://www.facebook.com/dialog/oauth?client_id=' in parsed['data']


def test_register_no_token(app):
    with app.test_client() as c:
        resp = c.post('/auth/register')
        assert resp.status_code == 400
        parsed = json.loads(resp.data.decode('utf-8'))
        assert 'No login token' in parsed['data']


def test_register_fb_error(app):
    with app.test_client() as c:
        with c.session_transaction() as session:
                session['fb_token'] = 'a value'

        mock_get = Mock()
        mock_get.json = Mock(
            return_value={
                'error': {'message': 'some error'}
            }
        )
        with patch('petra.api.auth.requests.get', return_value=mock_get):
            resp = c.post('/auth/register')
            assert resp.status_code == 400
            parsed = json.loads(resp.data.decode('utf-8'))
            assert 'some error' == parsed['data']

    with app.app_context():
        assert User.query.count() == 0


def test_register(app):
    with app.test_client() as c:
        with c.session_transaction() as session:
                session['fb_token'] = 'a value'

        mock_get = Mock()
        mock_get.json = Mock(
            return_value={
                'email': 'test@example.org',
                'first_name': 'Testus',
                'last_name': 'Maximus',
            }
        )

        with patch('petra.api.auth.requests.get', return_value=mock_get):
            resp = c.post('/auth/register')
            assert resp.status_code == 200
            parsed = json.loads(resp.data.decode('utf-8'))

            assert 'Testus Maximus' == parsed['data']['name']
            assert 'test@example.org' == parsed['data']['email']

            assert flask.session['email'] == 'test@example.org'

    with app.app_context():
        assert User.query.count() == 1
        user = User.query.first()

        assert user.email == 'test@example.org'
        assert user.name == 'Testus Maximus'


def test_login(app):
    with app.app_context():
        user = User(
            name='Testus Maximus',
            email='test@example.org',
        )
        db.session.add(user)
        db.session.commit()
        assert User.query.count() == 1

    with app.test_client() as c:
        with c.session_transaction() as session:
                session['fb_token'] = 'a value'

        mock_get = Mock()
        mock_get.json = Mock(
            return_value={
                'email': 'test@example.org',
            }
        )

        with patch('petra.api.auth.requests.get', return_value=mock_get):
            resp = c.post('/auth/login')
            assert resp.status_code == 200
            parsed = json.loads(resp.data.decode('utf-8'))

            assert 'Testus Maximus' == parsed['data']['name']
            assert 'test@example.org' == parsed['data']['email']

            assert flask.session['email'] == 'test@example.org'
