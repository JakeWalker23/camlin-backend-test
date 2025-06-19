from fastapi import APIRouter, Depends, HTTPException, status
from src.middleware.validators import validate_currency_amount, validate_currency_code

from src.services.wallet_service import (
    get_wallet,
    add_currency_to_wallet,
    subtract_currency_from_wallet,
    remove_currency_from_wallet,
)
from src.services.auth_service import verify_jwt
from src.models.wallet import Wallet


router = APIRouter()


@router.get("/wallet", response_model=Wallet)
async def read_wallet(user=Depends(verify_jwt)):
    wallet = await get_wallet()
    return wallet


@router.post("/wallet/add/{currency}/{amount}")
async def add_to_wallet(currency: str, amount: float):
    try:
        validated_currency = validate_currency_code(currency)
        validated_amount = validate_currency_amount(amount)

        await add_currency_to_wallet(validated_currency, amount)
        return {"message": f"Added {amount} {validated_currency} to wallet"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/wallet/sub/{currency}/{amount}")
async def subtract_from_wallet(currency: str, amount: float):
    try:
        validated_currency = validate_currency_code(currency)
        validated_amount = validate_currency_amount(amount)

        await subtract_currency_from_wallet(validated_currency, amount)
        return {"message": f"Subtracted {amount} {validated_currency} from wallet."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/wallet/{currency}")
async def delete_currency_from_wallet(currency: str):
    try:
        validated_currency = validate_currency_code(currency)

        await remove_currency_from_wallet(validated_currency)
        return {"message": f"{validated_currency} removed from wallet."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
