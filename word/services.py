from utils import Paging
from word.models import Word, wordDAO
import db

@db.transactional
def save_word(word):
    wordDAO.save(*word)

@db.transactional
def update_phonetic(phonetic: str, word: str, guid: int):
    return wordDAO.update_phonetic(phonetic, word, guid)


def get_world_by_book(guid: int, page: int, per_page: int):
    total = wordDAO.count_by_book(guid)[0]
    paging = Paging(total, page, per_page)
    words = wordDAO.find_by_book(guid, per_page, paging.offset)
    paging.add([Word.from_db(*word) for word in words])
    return paging


def get_first_word_by_book(book_guid: int) -> Word:
    _w = wordDAO.find_by_book_first(book_guid)
    if _w is not None:
        return Word.from_db(*_w)


def get_word_by_book_with_index(book_guid: int, start_index: int, per_page: int):
    words = wordDAO.find_by_book_with_start(book_guid, start_index, per_page)
    return [Word.from_db(*w) for w in words]
