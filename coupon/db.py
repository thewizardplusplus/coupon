import os
import sqlite3

import termcolor

from . import logger

def init_db():
    db_filename = os.environ.get('COUPON_DATABASE', './campaigns.db').strip()
    if len(db_filename) == 0:
        return None

    db_connection = sqlite3.connect(db_filename)
    with db_connection:
        db_connection.execute('''CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            name TEXT NOT NULL
        )''')

    logger.get_logger().info(
        'connect to the database ' + termcolor.colored(db_filename, 'green'),
    )

    return db_connection

def register_campaign(db_connection, name):
    with db_connection:
        db_connection.execute('INSERT INTO campaigns(name) VALUES(?)', (name,))

def count_registered_campaigns(db_connection, name, interval):
    (counter,) = db_connection.execute('''
        SELECT COUNT(*)
        FROM campaigns
        WHERE name=? AND timestamp >= DATETIME('now', ?)
    ''', (name, '-{:d} seconds'.format(interval))).fetchone()
    return counter