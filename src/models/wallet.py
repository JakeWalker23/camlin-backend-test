from pydantic import BaseModel
from typing import Dict


class Wallet(BaseModel):
    holdings: Dict[str, float]
    pln_holdings: Dict[str, float]
    total_pln: float
