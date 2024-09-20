import json
import math
import uuid
from dataclasses import asdict, is_dataclass
from datetime import date, datetime

from flask import make_response

from db import Base


def generate_uuid():
    return uuid.uuid4().hex


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, Base):
            return obj.unbox()

            
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        
        else:
            return json.JSONEncoder.default(self, obj)


encoder = CustomEncoder()


def render_json(data):
    content = encoder.encode(data)
    r = make_response(content)
    r.mimetype = "application/json"
    return r


def render_error(msg, code=200):
    msg = dict(message=msg)
    r = make_response(msg)
    r.status_code = code
    r.mimetype = "application/json"
    return r


class Rule:

    def __init__(self, key, default=None):
        self.key = key
        self.required = default is None
        self.default = default


class Validator():

    def __init__(self):
        self.rules = []

    def rule(self, key, default=None):
        self.rules.append(Rule(key, default))
        return self

    def validate_form(self, form):

        _param = []
        for rule in self.rules:
            if rule.required:
                if form is None or form.get(rule.key) is None:
                    raise ValidationError(f"{rule.key} is required")
                else:
                    _param.append(form[rule.key])
            else:
                if form is not None and form.get(rule.key) is not None:
                    _param.append(form[rule.key])
                else:
                    _param.append(rule.default)
        if len(_param) == 1:
            return _param[0]
        return _param


class Paging(Base):

    def __init__(self, total: int, page: int, per_page: int):

        self.total = total
        self.page = page
        self.per_page = per_page
        self.pages = math.ceil((total - 1 + per_page) / per_page)
        self.list = []

    @property
    def offset(self):
        return (self.page - 1) * self.per_page

    def add(self, data):
        if data is not None:
            self.list.extend(data)


class ValidationError(Exception):

    def __init__(self, message):
        self.value = message

    def __str__(self):
        return self.value


class LogicException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.value = message
        self.code = code

    def __str__(self):
        return self.value
