from flask import Blueprint, request

from base import auth
from utils import Validator, render_json
from word import services as wordService
word = Blueprint("word", __name__)


@word.route("/")
@auth.login_required
def word_list():
    form = request.get_json()
    validator = Validator().rule("guid").rule("page", 1).rule("per_page", 10)
    guid, page, per_page = validator.validate_form(form)
    words = wordService.get_world_by_book(guid, page, per_page)
    return render_json(words)
