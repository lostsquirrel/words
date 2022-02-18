import db
from utils import Paging


from word.models import Word, wordDAO


@db.transactional
def saveWord(word):
    wordDAO.save(*word)


def getWorldByBook(guid, page, per_page):
    total = wordDAO.count_by_book(guid)[0]
    paging = Paging(total, page, per_page)
    words = wordDAO.find_by_book(guid, per_page, paging.offset)
    paging.add([Word.from_db(*word) for word in words ])
    return paging