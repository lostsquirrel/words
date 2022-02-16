from mysql import connector
from settings import mysql_host, mysql_user, mysql_password, mysql_db_name, mysql_pool_name, mysql_pool_size

class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

def build_mysql_config():
    return dict(
        pool_name=mysql_pool_name,
        pool_size=mysql_pool_size,
        host=mysql_host,
        user=mysql_user,
        database=mysql_db_name,
        passwd=mysql_password
    )

def create_pool():
    return connector.connect(**build_mysql_config())

pool = create_pool()

def choose_param(args, kwargs):
    if len(args) > 0:
        return args
    if len(kwargs) > 0:
        return kwargs

def transactional(method):
    def decorator(*args, **kwds):
        try:
            _result = method(*args, **kwds)
            pool.commit()
        except Exception as e:
            pool.rollback()
            raise e
        return _result

    return decorator

def insert(method):

    def decorator(dao, *args, **kwargs):
        cursor = pool.cursor()
        sql = method(dao, *args, **kwargs)
        cursor.execute(sql, kwargs)
        return cursor.lastrowid

    return decorator

def query(method):

    def decorator(dao, *args, **kwargs):
        cursor = pool.cursor()
        sql = method(dao, *args, **kwargs)
        cursor.execute(sql, args, kwargs)
        return cursor.fetchall()

    return decorator

def update(method):

    def decorator(dao, *args, **kwargs):
        cursor = pool.cursor()
        sql = method(dao, *args, **kwargs)
        cursor.execute(sql, args, kwargs)
        return cursor.rowcount

    return decorator

def get(method):
    def decorator(dao, *args, **kwargs):
        cursor = pool.cursor()
        sql = method(dao, *args, **kwargs)
        param = choose_param(args, kwargs)
        if param is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)
        return cursor.fetchone()
    return decorator