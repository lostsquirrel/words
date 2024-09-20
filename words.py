from flask import Flask

from plan.api import _plan
from user.api import user
from utils import LogicException, ValidationError, render_error
from word.api import word
from wordbook.api import wordbook
from db import init_app
app = Flask(__name__)

app.register_blueprint(wordbook, url_prefix="/wordbook")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(word, url_prefix="/word")
app.register_blueprint(_plan, url_prefix="/plan")
app.register_error_handler(ValidationError, lambda e: render_error(str(e), 400))
app.register_error_handler(LogicException, lambda e: render_error(e.value, e.code))
app.register_error_handler(500, lambda e: render_error("system error", code=500))
init_app(app)

@app.errorhandler(500)
def system_error(e):
    return render_error("system error", code=500)
