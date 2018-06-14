"""
User Database
"""

import sys
import sqlite3
from user.account import create_account
import user
from utils import log
from version import DB_VERSION


# Connect to database
CONN = sqlite3.connect('data/pyrealm.db', isolation_level=None)
CONN.row_factory = sqlite3.Row
with CONN:
    CURSOR = CONN.cursor()

def create_accounts_table():
    """Table to store user / login data"""
    log.debug('FUNC create_accounts_table()')
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
        log.info('Creating Admin user account...')
        # FIXME: this needs to come from a config file outside of git repo
        # Alternatively, on boot w/ empty db, the first user to log in is
        # Run through login wizard with username fixed to Admin
        data = create_account('Admin', 'changeme')
        save_account(data)
    except sqlite3.Error as err:
        log.error("Error creating table: accounts - %s\n", err)
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
    except sqlite3.Error as err:
        log.error("Error creating table: login_history - %s\n", err)
        sys.exit(1)


def boot_userdb():
    """Check database exists, create tables if missing"""
    sql_tables = ["accounts", "login_history"]
    db_version = CURSOR.execute('PRAGMA user_version').fetchone()[0]
    if db_version == 0:
        log.info("Initializing database...")
        CURSOR.execute('PRAGMA user_version={};'.format(DB_VERSION))
    else:
        log.info("Database is version %s", db_version)
    sql = """SELECT COUNT(*) FROM sqlite_master WHERE NAME = ?;"""
    for table in sql_tables:
        if not CURSOR.execute(sql, (str(table),)).fetchone()[0]:
            log.info("Creating table: %s", table)
            func = 'create_{}_table'.format(table)
            getattr(user.db, func)()
        else:
            log.info("Found table: %s", table)


def account_exists(username):
    """Search user database to see if an account exists"""
    log.debug('FUNC account_exists(%s)', username)
    sql = 'SELECT COUNT(*) FROM accounts WHERE username=?'
    count = 0
    try:
        count = CURSOR.execute(sql, (username,)).fetchone()[0]
    except sqlite3.Error as err:
        log.debug('Query FAILED: %s -> err=%s', sql, err)
    if count > 0:
        return True
    return False


def load_account(username):
    """Return a dict of account data"""
    log.debug('FUNC load_account(%s)', username)
    sql = 'SELECT * FROM accounts WHERE username=?'
    log.debug('SQL: %s', sql)
    try:
        row = CURSOR.execute(sql, (username,)).fetchone()
    except sqlite3.Error as err:
        log.error('Load account FAILED: %s', err)
    log.debug('FUNC LEAVE: load_account(%s)', username)
    return dict(row)


def save_account(data):
    """Save account data - figures out whether to insert or update"""
    log.debug('FUNC save_account(%s)')
    result = None
    if account_exists(data['username']):
        sql = '''UPDATE accounts SET hash=?, salt=?,
                    active=?, playing=?, banned=?, created=?, last_login=?, 
                    logins=?, failures=? WHERE username=?'''
        log.debug('EXECUTE SQL: %s <- %s', sql, data)
        try:
            result = CURSOR.execute(sql, (data['hash'], data['salt'],
                                          data['active'], data['playing'],
                                          data['banned'], data['created'],
                                          data['last_login'], data['logins'],
                                          data['failures'], data['username']))
        except sqlite3.Error as err:
            log.error('save_account() FAILED: %s', err)
    else:
        sql = '''INSERT INTO accounts (username, hash, salt, active,
                    playing, banned, created, last_login, logins, failures ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        log.debug('EXECUTE SQL: %s <- %s', sql, data)
        try:
            result = CURSOR.execute(sql, (data['username'],
                                          data['hash'], data['salt'],
                                          data['active'], data['playing'],
                                          data['banned'], data['created'],
                                          data['last_login'], data['logins'],
                                          data['failures']))
        except sqlite3.Error as err:
            log.error('save_account() FAILED: %s', err)
    return result


def record_visit(data: dict):
    """Insert IP/date into login_history table"""
    log.debug('FUNC record_visit(%s)', data)
    sql = 'SELECT rowid FROM accounts WHERE username=?'
    log.debug('EXECUTE SQL: %s <- %s', sql, data['username'])
    try:
        result = CURSOR.execute(sql, (data['username'],)).fetchone()
    except sqlite3.Error as err:
        log.error('SQL query failed: %s -> %s', sql, err)
    log.debug('Result: %s', result[0])
    sql = 'INSERT INTO login_history (account, date, ip) VALUES (?, ?, ?);'
    try:
        log.debug('EXECUTE SQL: %s <- (%s, %s, %s)', sql, result[0], data['date'], data['ip'])
        result = CURSOR.execute(sql, (result[0], data['date'], data['ip']))
    except sqlite3.Error as err:
        log.error('SQL query failed: %s', err)
