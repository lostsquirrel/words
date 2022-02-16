

from base import auth
from flask import Blueprint, request
from utils import render_error, render_json, validate_form

from user import services as userService

user = Blueprint("user", __name__)


@user.route("/join", methods=["POST"])
def join():
    form = request.get_json()
    invite_code, device_id, device_type = validate_form(form,
                                                        "invite_code", "device_id", "device_type")

    if not userService.isInviteCodeExists(invite_code):
        return render_error("invalid code")
    user = userService.createUser(invite_code, device_id, device_type)
    return render_json(user)


@user.route("/login", methods=["POST"])
def login():
    form = request.get_json()

    device_id, device_type = validate_form(form, "device_id", "device_type")

    token = userService.login(device_id, device_type)
    if token is None:
        return render_error("invalid device")
    return render_json({"token": token})


@user.route("/generate", methods=["POST"])
@auth.login_required(role=["admin"])
def generate_invite_code():
    _code = userService.generate_invite_code()
    code = userService.getInviteCode(_code)
    return render_json(code)
