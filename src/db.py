"""
Database implementation
"""

import sqlite3
import logging
mudlog = logging.getLogger('mudlog')
from version import DB_VERSION


# Connect to database
CONN = sqlite3.connect('../data/pyrealm.db')

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
              active INT,
              banned INT
              suspended TIMESTAMP,
              created TIMESTAMP,
              last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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


def check_db():
    """Check database exists, create tables if missing"""

    tables=["accounts", "login_history"]

    db_version = CURSOR.execute('PRAGMA user_version').fetchone()[0]

    if db_version == 0:
        mudlog.info("Initializing database...")
        CURSOR.execute('PRAGMA user_version={};'.format(DB_VERSION))
    else:
        mudlog.info("Database is version {}".format(db_version))

    sql = """SELECT COUNT(*) FROM sqlite_master WHERE NAME = ?;"""

    for table in tables:
        if not CURSOR.execute(sql, (str(table),)).fetchone()[0]:
            mudlog.info("Creating table: {}".format(table))
            exec('create_{}_table()'.format(table))
        else:
            mudlog.info("Found table: {}".format(table))

