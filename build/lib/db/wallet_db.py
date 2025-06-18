import sqlite3

DB_PATH = 'wallet.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS wallet (
                currency TEXT PRIMARY KEY,
                amount REAL NOT NULL CHECK(amount >= 0)
            )
        ''')
        conn.commit()


def fetch_all_currencies():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT currency, amount FROM wallet')
        rows = cursor.fetchall()
        return {currency: amount for currency, amount in rows}

def init_wallet_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM wallet')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute('INSERT INTO wallet (currency, amount) VALUES (?, ?)', ('PLN', 0.0))
            conn.commit()