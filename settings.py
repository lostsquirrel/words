import logging
import os

mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_user = os.getenv('MYSQL_USER', 'word')
mysql_password = os.getenv('MYSQL_PASSWORD', '')
mysql_db_name = "words"
mysql_pool_name = "words"
mysql_pool_size = int(os.getenv('MYSQL_POOL_SIZE', 10))

log_format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
log_level = logging.INFO
is_dev = os.getenv('IS_DEV', 1)
if int(is_dev) == 1:
    log_level = logging.DEBUG
logging.basicConfig(level=log_level, format=log_format)
