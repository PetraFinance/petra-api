from flask import jsonify


def success(data=None):
    return jsonify({
        'status': 'success',
        'data': data,
    }), 200


def fail(data=None, status_code=400):
    return jsonify({
        'status': 'fail',
        'data': data,
    }), status_code


def error(message, status_code=500, data=None, error_code=None):
    return jsonify({
        'status': 'error',
        'message': message,
        'data': data,
        'code': error_code,
    }), status_code
