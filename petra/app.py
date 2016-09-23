import logging
import os

from flask import Flask

from petra.api.auth import auth
from petra.api.connections import connections
from petra.api.finance import finance
from petra.db import db
from petra.jsend import error, success
from petra.models import User
from petra.serializer import SerializingJSONEncoder

app = Flask(__name__)
app.config.from_object('petra.flaskconfig')
app.json_encoder = SerializingJSONEncoder

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return success(User.query.all())


@app.route('/health')
def health():
    return success('ok')


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(connections, url_prefix='/connections')
app.register_blueprint(finance, url_prefix='/finance')

# Error handlers.


@app.errorhandler(500)
def internal_error(error_details):
    return error('Internal Error', 500)


@app.errorhandler(404)
def not_found_error(error_details):
    return error('Page not found', 404)


if not app.debug:
    file_handler = logging.FileHandler('error.log')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: '
                          '%(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
