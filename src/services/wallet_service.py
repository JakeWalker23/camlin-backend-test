from src.services.exchange_service import fetch_exchange_rates
from src.models.wallet import Wallet
from src.db.wallet_db import (
    fetch_all_currencies,
    add_currency_amount,
    subtract_currency_amount,
    remove_currency,
)

class WalletService:
    def __init__(self):
        pass

    async def get_wallet(self) -> Wallet:
        holdings = fetch_all_currencies()
        exchange_rates = await fetch_exchange_rates()

        pln_holdings = {}
        total_pln = 0.0

        for currency, amount in holdings.items():
            rate = exchange_rates.get(currency, 1.0 if currency == "PLN" else 0.0)
            pln_value = round(amount * rate, 2)
            pln_holdings[currency] = pln_value
            total_pln += pln_value

        return Wallet(
            holdings=holdings,
            pln_holdings=pln_holdings,
            total_pln=round(total_pln, 2),
        )

    async def add_currency_to_wallet(self, currency: str, amount: float):
        add_currency_amount(currency, amount)


    async def subtract_currency_from_wallet(self, currency: str, amount: float):
        subtract_currency_amount(currency, amount)
    
    async def remove_currency_from_wallet(self, currency: str):
        remove_currency(currency)





