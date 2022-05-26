import db
from datetime import datetime


class Wordbook(db.Base):

    def __init__(self):
        current_time = datetime.now()
        self.id = None
        self.guid = None
        self.name = None
        self.word_amount = 0
        self.create_time = current_time
        self.modified_time = current_time

    @staticmethod
    def from_db(*args):

        _b = Wordbook()
        _b.id = args[0]
        _b.guid = args[1]
        _b.name = args[2]
        _b.word_amount = args[3]
        _b.create_time = args[4]
        _b.modified_time = args[5]
        return _b


class WordbookDAO:

    @db.query
    def find_all(self):
        sql = "SELECT id, guid, name, word_amount, create_time, modified_time FROM wordbook ORDER BY guid"
        return sql

    @db.get
    def find(sel, book_id: int):
        sql = "SELECT id, guid, name, word_amount, create_time, modified_time FROM wordbook WHERE id = %s"
        return sql

    @db.get
    def find_by_guid(self, guid: int):
        sql = """SELECT
        id, guid, name, word_amount, create_time, modified_time
        FROM wordbook WHERE guid = %s"""
        return sql


wordbookDAO = WordbookDAO()
