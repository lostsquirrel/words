from flask import Blueprint
from utils import render_json
from wordbook import services as workbookService

wordbook = Blueprint("wordbook", __name__)

@wordbook.route("/")
def hello_world():
    wordbooks = workbookService.all()
    return render_json(wordbooks)