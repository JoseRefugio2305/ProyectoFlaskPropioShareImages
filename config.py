from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_CONNECTION_DATA = [os.environ["MYSQL_USER"],os.environ["MYSQL_PASS"], os.environ["MYSQL_HOST"], os.environ["MYSQL_BDD"], os.environ["MYSQL_PORT"]]