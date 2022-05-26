from flask import Blueprint
from utils import LogicException, render_json
from wordbook import services as workbookService

wordbook = Blueprint("wordbook", __name__)


@wordbook.route("/")
def list():
    wordbooks = workbookService.all()
    return render_json(wordbooks)


@wordbook.route("/guid/<book_guid>")
def get(book_guid):
    wb = workbookService.get_wordbook_by_guid(book_guid)
    if wb is None:
        raise LogicException(f"cannot find wordbook with guid <{book_guid}>", 404)
    return render_json(wb)
