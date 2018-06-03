"""
User Database
"""

import sqlite3
from utils import log
from version import DB_VERSION


# Connect to database
CONN = sqlite3.connect('../../data/pyrealm.db')

with CONN:
    CURSOR = CONN.cursor()


def create_accounts_table():
    """Table to store user / login data"""

    sql = """CREATE TABLE IF NOT EXISTS accounts (
              id INT PRIMARY KEY);"""
    """,
              name TEXT,
              email TEXT,
              hash TEXT,
              salt TEXT,
              active INT,
              banned INT
              created TIMESTAMP,
              last_login TIMESTAMP,
              logins INT,
              failures INT);"""
    try:
        CURSOR.execute(sql)
    except Exception as e:
        print("Error creating table: accounts - {}\n".format(e))


def create_login_history_table():
    """Table to store ip, login dates for users"""
    sql = """CREATE TABLE IF NOT EXISTS login_history (
                id INT PRIMARY KEY,
                account INT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip TEXT KEY NOT NULL
                );"""
    try:
        CURSOR.execute(sql)
    except Exception as e:
        print("Error creating table: accounts - {}\n".format(e))


def boot_db():
    """Check database exists, create tables if missing"""

    tables=["accounts", "login_history"]

    db_version = CURSOR.execute('PRAGMA user_version').fetchone()[0]

    if db_version == 0:
        log.info("Initializing database...")
        CURSOR.execute('PRAGMA user_version={};'.format(DB_VERSION))
    else:
        log.info("Database is version {}".format(db_version))

    sql = """SELECT COUNT(*) FROM sqlite_master WHERE NAME = ?;"""

    for table in tables:
        if not CURSOR.execute(sql, (str(table),)).fetchone()[0]:
            log.info("Creating table: {}".format(table))
            exec('create_{}_table()'.format(table))
        else:
            log.info("Found table: {}".format(table))


def account_exists(username):
    """Search user database to see if an account exists"""
    sql = 'SELECT COUNT(*) FROM accounts WHERE username={};'.format(username)
    CURSOR.execute(sql)
    if len(CURSOR.fetchall()) > 0:
        return True
    else:
        return False


def load_account(username):
    """Return a dict of account data"""
    sql = 'SELECT * FROM accounts WHERE username={};'.format(username)
    account = CURSOR.execute(sql).fetchone()
    return account


def save_account(data):
    """Save account data - figures out whether to insert or update"""
    if account_exists(data.username):
        sql = '''UPDATE accounts SET VALUES = (username="{}", hash="{}",
                     salt="{}", active={}, banned={}, 
                     created={}, last_login={}, logins={}, 
                     failures={});'''.format(data.username,
                     data.hash, data.salt, data.active, data.banned, 
                     data.created, data.last_login, data.logins, 
                     data.failures)
    else:
        sql = '''INSERT INTO accounts VALUES (username="{}", hash="{}", 
                     salt="{}", active={}, banned={}, 
                     created={}, last_login={}, logins={}, 
                     failures={});'''.format(data.username,
                     data.hash, data.salt, data.active, data.banned, 
                     data.suspended, data.created, data.last_login, 
                     data.logins, data.failures)
    log.debug('EXECUTE SQL: {}'.format(sql))
    result = CURSOR.execute(sql)
    return result
