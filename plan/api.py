

from flask import Blueprint
from base import auth
from plan import services as planService

plan = Blueprint("plan", __name__)

@plan.route("/", methods=["POST"])
@auth.login_required
def create_plan():
    user = auth.current_user()

