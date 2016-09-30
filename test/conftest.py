import os
from importlib import reload

import pytest
import tempfile

import petra.app
import petra.db


@pytest.fixture
def app():
    reload(petra.app)
    petra_app = petra.app.app
    fd, fname = tempfile.mkstemp()

    petra_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(fname)
    petra_app.config['TESTING'] = True

    petra.db.db.init_app(petra_app)
    with petra_app.app_context():
        petra.db.db.create_all()

    yield petra_app

    os.close(fd)
    os.unlink(fname)
