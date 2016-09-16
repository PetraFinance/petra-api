from petra.config import config

# Enable debug mode.
DEBUG = config.get('FLASK_DEBUG_MODE', False)

# Secret key for session management.
SECRET_KEY = config['FLASK_SECRET_KEY']

# Connect to the database
DB = config['MYSQL']
SQLALCHEMY_DATABASE_URI = '{}:///{}:{}@{}/db'.format(
    DB['TYPE'],
    DB['USER'],
    DB['PASS'],
    DB['HOST'],
)

# Disable warning about deprecated feature
SQLALCHEMY_TRACK_MODIFICATIONS = False
