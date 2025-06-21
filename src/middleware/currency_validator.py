from fastapi import HTTPException
import re

class CurrencyValidator:
    CURRENCY_REGEX = re.compile(r"^[a-zA-Z]{3}$")

    @staticmethod
    def validate_currency_amount(value: str) -> float:
        try:
            amount = float(value)
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid amount: {value}. Must be a number."
            )

        if amount < 0:
            raise HTTPException(status_code=400, detail=f"Invalid Amount: {value}. Must be non-negative.")

        return amount

    @staticmethod
    def validate_currency_code(code: str) -> str:
        if not CurrencyValidator.CURRENCY_REGEX.match(code):
            raise HTTPException(status_code=400, detail=f"Invalid currency code: {code}")
        return code.upper()