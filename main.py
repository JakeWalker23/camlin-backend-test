from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.controllers.wallet_controller import router as wallet_router
from src.core.init import init_app
from src.db.wallet_db import init_db, init_wallet_table
from src.utils.limiter import limiter

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

init_db()
init_wallet_table()

init_app()

app.include_router(wallet_router)
