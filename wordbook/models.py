import db

class Wordbook(db.Row):

    def __init__(self, *args):

        self.id = args[0]
        self.guid = args[1]
        self.name = args[2]
        self.word_amount = args[3]
        self.create_time = args[4]
        self.modified_time = args[5]

class WordbookDAO:

    @db.query
    def find_all(self):
        sql = "SELECT id, guid, name, word_amount, create_time, modified_time FROM wordbook ORDER BY guid"
        return sql

wordbookDAO = WordbookDAO()