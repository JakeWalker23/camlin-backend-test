from src.middleware.currency_validator import CurrencyValidator
from src.services.wallet_service import WalletService
from src.services.auth_service import AuthService
from src.models.wallet import Wallet

from src.utils.limiter import limiter

from fastapi import APIRouter, Depends, HTTPException, status, Request

wallet_service = WalletService()
currency_validator = CurrencyValidator()

router = APIRouter(
    dependencies=[Depends(AuthService.verify_jwt)]
)

@router.get("/wallet", response_model=Wallet)
@limiter.limit("10/minute")
async def read_wallet(request: Request):
    return await wallet_service.get_wallet()


@router.post("/wallet/add/{currency}/{amount}")
async def add_to_wallet(currency: str, amount: str):
    try:
        validated_currency = currency_validator.validate_currency_code(currency)
        validated_amount = currency_validator.validate_currency_amount(amount)

        await wallet_service.add_currency_to_wallet(validated_currency, validated_amount)
        
        return {"message": f"Added {amount} {validated_currency} to wallet"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/wallet/sub/{currency}/{amount}")
async def subtract_from_wallet(currency: str, amount: str):
    try:
        validated_currency = currency_validator.validate_currency_code(currency)
        validated_amount = currency_validator.validate_currency_amount(amount)

        await wallet_service.subtract_currency_from_wallet(validated_currency, validated_amount)
        
        return {"message": f"Subtracted {amount} {validated_currency} from wallet."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/wallet/{currency}")
async def delete_currency_from_wallet(currency: str):
    try:
        validated_currency = currency_validator.validate_currency_code(currency)

        await wallet_service.remove_currency_from_wallet(validated_currency)
        
        return {"message": f"{validated_currency} removed from wallet."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
