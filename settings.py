import os

mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_user = os.getenv('MYSQL_USER', 'word')
mysql_password = os.getenv('MYSQL_PASSWORD', '')
mysql_db_name = "words"
mysql_pool_name = "words"
mysql_pool_size = int(os.getenv('MYSQL_POOL_SIZE', 10))