import db

class Phonetic(db.Row):

    def __init__(self, value, file):
        self.value = value # 音标
        self.file = file # 发音音频文件地址

class Word():

    def __init__(self):
        self.id = None
        self.guid = None # 词库编号
        self.word = None # 单词
        self.__phonetic = None
        self.description = None # 释义
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
        self.__phonetic = [Phonetic(*_px.split(",")) for _px in _p ]
        



class WordDAO:

    @db.insert
    def save(self, *args):
        sql = "INSERT INTO words (guid, word, phonetic, description) VALUES (%s, %s, %s, %s)"
        return sql

    @db.get
    def count_by_book(self, guid: int):
        sql = "SELECT count(*) AS total FROM words WHERE guid = %s"
        return sql

    @db.query
    def find_by_book(self, guid: int, limit: int, offset: int):
        sql = "SELECT id, guid, word, phonetic, description, score FROM words WHERE guid = %s LIMIT %s OFFSET %s"
        return sql


wordDAO = WordDAO()