"""
User Database
"""

import sys
import sqlite3
from utils import log
from version import DB_VERSION


# Connect to database
CONN = sqlite3.connect('data/pyrealm.db', isolation_level=None)
CONN.row_factory = sqlite3.Row
with CONN:
    CURSOR = CONN.cursor()


def create_accounts_table():
    """Table to store user / login data"""

    sql = """CREATE TABLE IF NOT EXISTS accounts (
              username TEXT,
              email TEXT,
              hash BLOB,
              salt TEXT,
              active INT,
              playing TEXT,
              banned INT,
              created TIMESTAMP,
              last_login TIMESTAMP,
              logins INT,
              failures INT);"""
    try:
        CURSOR.execute(sql)
    except sqlite3.Error as e:
        log.error("Error creating table: accounts - {}\n".format(e))
        sys.exit(1)


def create_login_history_table():
    """Table to store ip, login dates for users"""
    sql = """CREATE TABLE IF NOT EXISTS login_history (
                account INT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip TEXT KEY NOT NULL
                );"""
    try:
        CURSOR.execute(sql)
    except sqlite3.Error as e:
        log.error("Error creating table: login_history - {}\n".format(e))
        sys.exit(1)


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
    log.debug('FUNC account_exists({})'.format(username))
    sql = 'SELECT COUNT(*) FROM accounts WHERE username=?'
    count = 0
    try:
        count = CURSOR.execute(sql, (username,)).fetchone()[0]
    except sqlite3.Error as e:
        log.debug('Query FAILED: {} -> e={}'.format(sql, e))
    if count > 0:
        return True
    return False


def load_account(username):
    """Return a dict of account data"""
    log.debug('FUNC load_account({})'.format(username))
    sql = 'SELECT * FROM accounts WHERE username=?'
    log.debug('SQL: {}'.format(sql))
    try:
        row = CURSOR.execute(sql, (username,)).fetchone()
    except sqlite3.Error as e:
        log.error('Load account FAILED: {}'.format(e))
    log.debug('FUNC LEAVE: load_account({})'.format(username))
    return dict(row)


def save_account(data):
    """Save account data - figures out whether to insert or update"""
    log.debug('FUNC save_account({data})')
    result = None
    if account_exists(data['username']):
        sql = '''UPDATE accounts SET hash=?, salt=?,
                    active=?, playing=?, banned=?, created=?, last_login=?, 
                    logins=?, failures=? WHERE username=?'''
        log.debug('EXECUTE SQL: {} <- {}'.format(sql, data))
        try:
            result = CURSOR.execute(sql, (data['hash'], data['salt'],
                data['active'], data['playing'], data['banned'], data['created'],
                data['last_login'], data['logins'], data['failures'],
                data['username']))
        except sqlite3.Error as e:
            log.error('save_account() FAILED: {}'.format(e))
    else:
        sql = '''INSERT INTO accounts (username, hash, salt, active,
                    playing, banned, created, last_login, logins, failures ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        log.debug('EXECUTE SQL: {} <- {}'.format(sql, data))
        try:
            result = CURSOR.execute(sql, (data['username'],
                data['hash'], data['salt'], data['active'], 
                data['playing'], data['banned'],
                data['created'], data['last_login'], 
                data['logins'], data['failures']))
        except sqlite3.Error as e:
            log.error('save_account() FAILED: {}'.format(e))
    return result


def record_visit(data: dict):
    """Insert IP/date into login_history table"""
    log.debug('FUNC record_visit({})'.format(data))
    sql = 'SELECT rowid FROM accounts WHERE username=?'
    log.debug('EXECUTE SQL: {} <- {}'.format(sql, data['username']))
    try:
        result = CURSOR.execute(sql, (data['username'],)).fetchone()
    except sqlite3.Error as e:
        log.error('SQL query failed: {}'.format(sql))
    log.debug('Result: {}'.format(result[0]))
    sql = 'INSERT INTO login_history (account, date, ip) VALUES (?, ?, ?);'
    try:
        log.debug('EXECUTE SQL: {} <- {}'.format(sql, result[0], data['date'], data['ip']))
        result = CURSOR.execute(sql, (result[0], data['date'], data['ip']))
    except sqlite3.Error as e:
        log.error('SQL query failed: {}'.format(sql))    

