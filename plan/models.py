import db

from datetime import datetime


class Plan(db.Base):
    """背单词计划
    """

    def __init__(self):
        current_time = datetime.now()
        self.id = None
        self.user_id = None
        self.book_id = None
        self.strategy = 0
        self.amount_per_day = 10
        self.default = 0  # 默认进入的计划
        self.state = 0  # 0 进行中， 1 完成
        self.phonetic = 0  # 使用音标序号
        self.create_time = current_time
        self.modified_time = current_time

    @staticmethod
    def from_db(*args):
        _p = Plan()
        _p.id = args[0]
        _p.user_id = args[1]
        _p.book_id = args[2]
        _p.strategy = args[3]  # 背单词策略，后续扩展
        _p.amount_per_day = args[4]
        _p.default = args[5]
        _p.state = args[6]
        _p.phonetic = args[7]
        _p.create_time = args[8]
        _p.modified_time = args[9]
        return _p


class Memorize(db.Base):

    def __init__(self):
        self.id = None
        self.plan_id = None
        self.word_id = None
        self.create_time = datetime.now()
        self.familiarity = 0  # 0 不认识 1 有印象 2 已掌握

    @staticmethod
    def from_db(*args):
        _m = Memorize()
        _m.id = args[0]
        _m.plan_id = args[1]
        _m.word_id = args[2]
        _m.create_time = args[3]
        _m.familiarity = args[4]
        return _m


class PlanDAO:

    @db.insert
    def save(self, **kwargs):
        sql = """
        INSERT INTO `plan` (
            user_id, book_id, strategy, amount_per_day, 
            `default`, state, phonetic, create_time, 
            modified_time) 
        VALUES (%(user_id)s, %(book_id)s, %(strategy)s, %(amount_per_day)s, 
        %(default)s, %(state)s, %(phonetic)s, %(create_time)s, 
        %(modified_time)s)
        """
        return sql

    @db.get
    def find_default_by_user(self, user_id: int):
        sql = """
        SELECT id, user_id, book_id, strategy, amount_per_day, `default`, 
        state, phonetic, create_time, modified_time 
        FROM `plan` 
        WHERE `default` = 1 AND user_id = %s LIMIT 1
        """
        return sql


class MemorizeDAO:

    @db.insert
    def save(self, **kwargs):
        sql = """
        INSERT INTO `memorize` (plan_id, word_id, create_time, familiarity) 
        VALUES (%(plan_id)s, %(word_id)s, %(create_time)s, %(familiarity)s)
        """
        return sql

    @db.get
    def find_last_by_plan(self, plan_id: int):
        sql = "SELECT id, plan_id, word_id, create_time, familiarity FROM `memorize` WHERE plan_id = %s ORDER BY create_time DESC LIMIT 1"
        return sql


planDAO = PlanDAO()
memorizeDAO = MemorizeDAO()
