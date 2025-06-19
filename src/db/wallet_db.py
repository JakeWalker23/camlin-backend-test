import sqlite3

DB_PATH = "wallet.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS wallet (
                currency TEXT PRIMARY KEY,
                amount REAL NOT NULL CHECK(amount >= 0)
            )
        """
        )
        conn.commit()


def fetch_all_currencies():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT currency, amount FROM wallet")
        rows = cursor.fetchall()
        return {currency: amount for currency, amount in rows}


def init_wallet_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM wallet")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(
                "INSERT INTO wallet (currency, amount) VALUES (?, ?)", ("PLN", 0.0)
            )
            conn.commit()


def add_currency_amount(currency: str, amount: float):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE wallet SET amount = amount + ? WHERE currency = ?",
            (amount, currency),
        )

        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO wallet (currency, amount) VALUES (?, ?)",
                (currency, amount),
            )

        conn.commit()
    conn.close()


def subtract_currency_amount(currency: str, amount: float):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT amount FROM wallet WHERE currency = ?", (currency,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"Currency '{currency}' not found in wallet.")

        current_amount = row[0]

        if amount > current_amount:
            raise ValueError(f"Insufficient funds in {currency}.")

        cursor.execute(
            "UPDATE wallet SET amount = amount - ? WHERE currency = ?",
            (amount, currency),
        )

    conn.commit()


def remove_currency(currency: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wallet WHERE currency = ?", (currency,))
        if cursor.rowcount == 0:
            raise ValueError(f"Currency '{currency}' does not exist in the wallet.")
    conn.commit()
