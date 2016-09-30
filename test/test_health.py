import json

import pytest

import petra.app


@pytest.fixture
def app():
    petra_app = petra.app.app
    petra_app.config['TESTING'] = True
    return petra_app.test_client()


def test_health(app):
    resp = app.get('/health')
    data = json.loads(resp.data.decode('utf8'))
    assert data['data'] == 'ok'
