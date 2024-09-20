import logging
import threading

from flask import g
from mysql import connector
from werkzeug.local import LocalProxy

from settings import (
    mysql_db_name,
    mysql_host,
    mysql_password,
    mysql_pool_name,
    mysql_pool_size,
    mysql_user,
)
from utils import LogicException

logger = logging.getLogger(__name__)
lock = threading.Lock()


class Base:
    def unbox(self):
        b = dict()
        for k, v in vars(self).items():
            if k.startswith(f"_{self.__class__.__name__}"):
                k = k.replace(self.__class__.__name__, "").lstrip("_")
            b[k] = v
        return b


def build_mysql_config():
    return dict(
        pool_name=mysql_pool_name,
        pool_size=mysql_pool_size,
        host=mysql_host,
        user=mysql_user,
        database=mysql_db_name,
        passwd=mysql_password,
    )


def create_pool():
    pool = connector.pooling.MySQLConnectionPool(**build_mysql_config())
    return pool


pool = create_pool()


def get_db_connection():
    global pool
    if "db_connection" not in g:
        try:
            conn = pool.get_connection()
            
            try:
                conn.ping(reconnect=True, attempts=3, delay=5)
                g.db_connection = conn
            except connector.Error as err:
                logger.error(f"Connection error: {err}")
                with lock:
                    pool = create_pool()
                conn = pool.get_connection()
                g.db_connection = conn

        except connector.PoolError as e:
            logger.error(e)
            raise LogicException("system busy")


    return g.db_connection


def close_db_connection(e=None):
    db_connection = g.pop("db_connection", None)
    if db_connection is not None:
        db_connection.close()


def init_app(app):
    app.teardown_appcontext(close_db_connection)


connection = LocalProxy(get_db_connection)


def choose_param(args, kwargs):
    if len(args) > 0:
        return args
    if len(kwargs) > 0:
        return kwargs


def execute(args, kwargs, cursor, sql):
    param = choose_param(args, kwargs)
    if param is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, param)


def transactional(method):
    def decorator(*args, **kwds):
        conn = get_db_connection()
        try:
            # conn.start_transaction()
            _result = method(*args, **kwds)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        return _result

    return decorator


def insert(method):
    def decorator(dao, *args, **kwargs):
        connection = get_db_connection()
        cursor = connection.cursor(buffered=True)
        try:
            sql = method(dao, *args, **kwargs)
            execute(args, kwargs, cursor, sql)
            return cursor.lastrowid
        except Exception as e:
            logger.error(e)
        finally:
            cursor.close()

    return decorator


def query(method):
    def decorator(dao, *args, **kwargs):
        cursor = get_db_connection().cursor(buffered=True)
        try:
            sql = method(dao, *args, **kwargs)
            execute(args, kwargs, cursor, sql)
            data = cursor.fetchall()

            return data
        except Exception as e:
            logger.error(e)
        finally:
            cursor.close()

    return decorator


def update(method):
    def decorator(dao, *args, **kwargs):
        connection = get_db_connection()
        cursor = connection.cursor(buffered=True)
        try:
            sql = method(dao, *args, **kwargs)
            execute(args, kwargs, cursor, sql)

            return cursor.rowcount
        except Exception as e:
            logger.error(e)
        finally:
            cursor.close()

    return decorator


def get(method):
    def decorator(dao, *args, **kwargs):
        connection = get_db_connection()
        cursor = connection.cursor(buffered=True)
        try:
            sql = method(dao, *args, **kwargs)
            execute(args, kwargs, cursor, sql)
            return cursor.fetchone()
        except Exception as e:
            logger.error(e)
        finally:
            cursor.close()

    return decorator
