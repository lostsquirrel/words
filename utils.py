import uuid

from flask import make_response


def generate_uuid():
    return uuid.uuid4().hex


def render_json(data):
    r = make_response(data)
    r.mimetype = "application/json"
    return r


def render_error(msg, code=200):
    msg = dict(message=msg)
    r = make_response(msg)
    r.status_code = code
    r.mimetype = "application/json"
    return r


def validate_form(param, *args):
    if param is None:
        raise ValidationError(f"{args} is required")
    _param = []
    for k in args:
        if param.get(k) is None:

            raise ValidationError(f"{k} is required")
        else:
            _param.append(param[k])
    return _param


class ValidationError(Exception):

    def __init__(self, message):
        self. value = message

    def __str__(self):
        return self.value


class LogicException(Exception):
    def __init__(self, message):
        self. value = message

    def __str__(self):
        return self.value
