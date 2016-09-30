import json


def test_health(app):
    with app.test_client() as c:
        resp = c.get('/health')
        data = json.loads(resp.data.decode('utf8'))
        assert data['data'] == 'ok'
