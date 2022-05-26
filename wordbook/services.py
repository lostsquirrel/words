from wordbook.models import wordbookDAO, Wordbook


def all():
    data = wordbookDAO.find_all()
    return [Wordbook.from_db(*r) for r in data]


def get_wordbook(book_id: int):
    _b = wordbookDAO.find(book_id)
    if _b is not None:
        return Wordbook.from_db(*_b)


def get_wordbook_by_guid(guid: int):
    _b = wordbookDAO.find_by_guid(guid)
    if _b is not None:
        return Wordbook.from_db(*_b)
