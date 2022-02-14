from wordbook.models import wordbookDAO, Wordbook


def all():
    data = wordbookDAO.find_all()
    return [Wordbook(*r) for r in data]
