from dotenv import load_dotenv
import os

import httpx

load_dotenv()

class ExchangeService:
    BASE_URL = os.getenv('EXCHANGE_URL')

    async def fetch_exchange_rates(self) -> dict[str, float]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()

        rates_list = data[0]["rates"]
        rates = {rate["code"]: rate["mid"] for rate in rates_list}
        rates["PLN"] = 1.0

        return rates
