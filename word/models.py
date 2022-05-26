import db


class Phonetic(db.Base):

    def __init__(self, value, file):
        self.value = value  # 音标
        self.file = file  # 发音音频文件地址


class Word(db.Base):

    def __init__(self):
        self.id = None
        self.guid = None  # 词库编号
        self.word = None  # 单词
        self.__phonetic = None
        self.description = None  # 释义
        self.score = 0

    @staticmethod
    def from_db(*args):
        _w = Word()
        _w.id = args[0]
        _w.guid = args[1]
        _w.word = args[2]
        _w.phonetic = args[3]
        _w.description = args[4]
        _w.score = 0
        return _w

    @property
    def phonetic(self):
        return self.__phonetic

    @phonetic.setter
    def phonetic(self, value):
        _p = value.split(";")
        # print(value)
        self.__phonetic = [Phonetic(*_px.split("__"))
                           for _px in _p if len(_px) > 1]


class WordDAO:

    @db.insert
    def save(self, *args):
        sql = "INSERT INTO words (guid, word, phonetic, description) VALUES (%s, %s, %s, %s)"
        return sql

    @db.get
    def count_by_book(self, guid: int):
        sql = "SELECT count(*) AS total FROM words WHERE guid = %s"
        return sql

    @db.update
    def update_phonetic(self, phonetic: str, word: str, guid: int):
        sql = """
        UPDATE words SET phonetic = %s
        WHERE word = %s AND guid = %s
        """
        return sql

    @db.update
    def update_phonetic_by_id(self, phonetic: str, word_id: int):
        sql = """UPDATE words SET phonetic = %s WHERE id = %s"""
        return sql

    @db.query
    def find_by_book(self, guid: int, limit: int, offset: int):
        sql = "SELECT id, guid, word, phonetic, description, score FROM words WHERE guid = %s LIMIT %s OFFSET %s"
        return sql

    @db.get
    def find_by_book_first(self, book_id: int):
        sql = "SELECT id, guid, word, phonetic, description, score FROM words WHERE guid = %s LIMIT 1"
        return sql

    @db.query
    def find_by_book_with_start(self, guid: int, start_index: int, limit: int):
        sql = "SELECT id, guid, word, phonetic, description, score FROM words WHERE guid = %s AND id > %s LIMIT %s"
        return sql

    @db.query
    def find_by_familiar(self, plan_id: int):
        sql = """
        SELECT w.id, w.guid, w.word, w.phonetic, w.description, w.score FROM words w
        LEFT JOIN memorize m
        ON w.id = m.word_id
        WHERE m.plan_id = %s
        """
        return sql


wordDAO = WordDAO()
