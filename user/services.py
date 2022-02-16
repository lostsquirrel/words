from datetime import datetime
import db
from user.models import InviteCode, inviteCodeDAO, User, userDAO, Token, tokenDAO
from utils import LogicException, generate_uuid


def isInviteCodeExists(code: str) -> bool:
    x = getInviteCode(code)
    return x is not None


@db.transactional
def createUser(code: str, device_id, device_type):
    user = getUserByDevice(device_id, device_type)
    if user is not None:
        raise LogicException("device already bind")
    current_time = datetime.now()
    c = getInviteCode(code)
    if c is None:
        raise LogicException("invalid code")
    
    u = User()
    u.device_id = device_id
    u.device_type = device_type
    user_id = userDAO.save(**u)
    inviteCodeDAO.update(user_id, current_time, code)
    return getUser(user_id)


def getUser(uid: str) -> User:
    _u = userDAO.find(uid)
    return User.from_db(*_u)


def getUserByDevice(device_id, device_type) -> User:
    _u = userDAO.find_by_device(device_id, device_type)
    if _u is not None:
        return User.from_db(*_u)


def getTokenByUser(uid):
    _t = tokenDAO.find_by_user(uid)
    if _t is not None:
        return Token.from_db(*_t)


@db.transactional
def login(device_id, device_type):
    user = getUserByDevice(device_id, device_type)
    if user is not None:
        token = generate_uuid()
        old_token = getTokenByUser(user.id)
        if old_token is None:
            _token = Token(token, user.id)
            tokenDAO.save(**_token)
        else:
            tokenDAO.update(token, datetime.now(), old_token.id)
        return token


def getInviteCode(code: str) -> InviteCode:
    _code = inviteCodeDAO.find(code)
    if _code is not None:
        return InviteCode.from_db(*_code)

@db.transactional
def generate_invite_code():
    _code = generate_uuid()
    code = InviteCode(_code)
    inviteCodeDAO.save(**code)

    return _code

def getToken(token: str) -> Token:
    _t = tokenDAO.find(token)
    if _t is not None:
        return Token.from_db(*_t)

