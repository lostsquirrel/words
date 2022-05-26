from datetime import datetime
import db


class InviteCode():
    def __init__(self, code: str):
        """生成邀请码

        Args:
            code (str): 邀请码
        """
        current_time = datetime.now()
        self.id = None
        self.code = code
        self.create_time = current_time
        self.modified_time = current_time
        self.bind = 0 # 绑定的用户ID， 未绑定为 0

    @staticmethod
    def from_db(*args):
        _o = InviteCode("")
        _o.id = args[0]
        _o.code = args[1]
        _o.create_time = args[2]
        _o.modified_time = args[3]
        _o.bind = args[4]
        return _o


class User(db.Base):

    def __init__(self):
        current_time = datetime.now()
        self.id = None
        self.device_id = None
        self.device_type = None
        self.create_time = current_time
        self.modified_time = current_time
        self.state = 0

    @staticmethod
    def from_db(*args):
        u = User()
        u.id = args[0]
        u.device_id = args[1]
        u.device_type = args[2]
        u.create_time = args[3]
        u.modified_time = args[4]
        u.state = args[5]
        return u


class Token(db.Base):

    def __init__(self, token, user_id):
        current_time = datetime.now()
        self.id = None
        self.token = token
        self.user_id = user_id
        self.create_time = current_time
        self.modified_time = current_time
        self.state = 0

    @staticmethod
    def from_db(*args):
        _t = Token("", "")
        _t.id = args[0]
        _t.token = args[1]
        _t.user_id = args[2]
        _t.create_time = args[3]
        _t.modified_time = args[4]
        _t.state = args[5]
        return _t


class InviteCodeDAO:

    @db.insert
    def save(self, **kwargs):
        sql = "INSERT INTO invite_code (code, create_time, modified_time) VALUES (%(code)s, %(create_time)s, %(modified_time)s)"
        return sql

    @db.get
    def find(self, code):
        sql = "SELECT id, code, create_time, modified_time, bind FROM invite_code WHERE code = %s AND bind = 0 LIMIT 1"
        return sql

    @db.update
    def update(self, *args):
        sql = "UPDATE invite_code SET bind = %s, modified_time = %s WHERE code = %s and bind = 0"
        return sql


class UserDAO:

    @db.insert
    def save(self, **kwargs):
        sql = "INSERT INTO user (device_id, device_type, create_time, modified_time, state) VALUES (%(device_id)s, %(device_type)s, %(create_time)s, %(modified_time)s, %(state)s)"
        return sql

    @db.get
    def find(self, uid: int):
        sql = "SELECT id, device_id, device_type, create_time, modified_time, state FROM user WHERE id = %s  LIMIT 1"
        return sql

    @db.get
    def find_by_device(self, device_id, device_type):
        sql = "SELECT id, device_id, device_type, create_time, modified_time, state FROM user WHERE device_id = %s AND device_type = %s LIMIT 1"
        return sql


class TokenDAO:

    @db.insert
    def save(self, **kwargs):
        sql = """INSERT INTO token (token, user_id, create_time, modified_time) 
            VALUES (%(token)s, %(user_id)s, %(create_time)s, %(modified_time)s)"""
        return sql

    @db.get
    def find(self, token):
        sql = "SELECT id, token, user_id, create_time, modified_time, state FROM token WHERE token = %s LIMIT 1"
        return sql

    @db.get
    def find_by_user(self, user_id):
        sql = "SELECT id, token, user_id, create_time, modified_time, state FROM token WHERE user_id = %s LIMIT 1"
        return sql

    @db.update
    def update(self, token, modified_time, token_id):
        sql = "UPDATE token SET token = %s, modified_time = %s WHERE id = %s"
        return sql


inviteCodeDAO = InviteCodeDAO()
userDAO = UserDAO()
tokenDAO = TokenDAO()
