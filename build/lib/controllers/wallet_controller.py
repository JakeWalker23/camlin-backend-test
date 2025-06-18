from fastapi import APIRouter
from src.services.wallet_service import get_wallet
from src.models.wallet import Wallet

router = APIRouter()

@router.get("/wallet", response_model=Wallet)
def read_wallet():
    return get_wallet()