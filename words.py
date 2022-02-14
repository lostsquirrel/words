from flask import Flask
from wordbook.api import wordbook

app = Flask(__name__)

app.register_blueprint(wordbook, url_prefix='/wordbook')