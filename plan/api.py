

from flask import Blueprint, request
from base import auth
from utils import Validator, render_error, render_json
from plan import services as planService
from word import services as wordService
from wordbook import services as wordbookService

_plan = Blueprint("plan", __name__)


@_plan.route("/", methods=["POST"])
@auth.login_required
def create_plan():
    book_id, strategy, amount_per_day, phonetic = Validator().rule(
        "book_id").rule(
        "strategy", 0).rule(
        "amount_per_day").rule(
        "phonetic", 0).validate_form(request.get_json())
    user = auth.current_user()

    plan_id = planService.create_plan(
        user.id, book_id, strategy, amount_per_day, phonetic)
    return render_json(plan_id)


@_plan.route("/default", methods=["GET"])
@auth.login_required
def get_default_plan():
    user = auth.current_user()
    plan = planService.get_user_default_plan(user.id)
    if plan is None:
        return render_error("no default plan found", 404)
    return render_json(plan)


@_plan.route("/memorize", methods=["POST"])
@auth.login_required
def create_memorize():
    plan_id, word_id, familiarity = Validator().rule("plan_id").rule(
        "word_id").rule(
        "familarity", 1).validate_form(request.get_json())
    memorize_id = planService.create_memorize(plan_id, word_id, familiarity)
    return render_json(memorize_id)


@_plan.route("/familiar", methods=["GET"])
@auth.login_required
def get_familiar_set():
    """获取当前计划背的单词
    """
    user = auth.current_user()
    words = planService.get_familiar_set(user.id)
    return render_json(words)
