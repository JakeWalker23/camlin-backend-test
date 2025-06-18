import httpx

NBP_API_URL = "https://api.nbp.pl/api/exchangerates/tables/A"

async def fetch_exchange_rates() -> dict[str, float]:
    async with httpx.AsyncClient() as client:
        response = await client.get(NBP_API_URL, headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()
    
    rates_list = data[0]["rates"]
    rates = {rate["code"]: rate["mid"] for rate in rates_list}
    
    rates["PLN"] = 1.0
    
    return rates