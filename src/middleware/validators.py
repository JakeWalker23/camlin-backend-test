from fastapi import HTTPException
import re


def validate_currency_amount(value: str) -> float:
    try:
        # Try to convert to float (int will work too)
        amount = float(value)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid amount: {value}. Must be a number."
        )

    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be non-negative.")

    return amount


def validate_currency_code(code: str) -> str:
    CURRENCY_REGEX = re.compile(r"^[a-zA-Z]{3}$")

    if not CURRENCY_REGEX.match(code):
        raise HTTPException(status_code=400, detail=f"Invalid currency code: {code}")
    return code.upper()
