from src.models.wallet import Wallet
from src.db.wallet_db import fetch_all_currencies

def get_wallet() -> Wallet:
    data = fetch_all_currencies()
    return Wallet(holdings=data)