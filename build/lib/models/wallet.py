from pydantic import BaseModel
from typing import Dict

class Wallet(BaseModel):
    holdings: Dict[str, float]

    @property
    def pln_total(self) -> float:
        return self.holdings.get("PLN", 0.0)