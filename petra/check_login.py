from functools import wraps

from flask import g, session

from petra.models import User
from petra.jsend import fail


def user_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = g.get('user', None)
        if user is None:
            email = session.get('email', None)
            if not email:
                return fail('No email found')

            user = User.query.filter_by(email=email).first()

            if not user:
                return fail('No account with email found')

            g.user = user

        return f(*args, **kwargs)

    return decorated_function
