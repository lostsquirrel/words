from flask import Blueprint, jsonify
from wordbook import services as workbookService

wordbook = Blueprint("wordbook", __name__)

@wordbook.route("/")
def hello_world():
    return jsonify(workbookService.all())