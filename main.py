from fastapi import FastAPI
from src.controllers.wallet_controller import router as wallet_router
from src.core.init import init_app
from src.db.wallet_db import init_db, init_wallet_table

app = FastAPI()

init_db()
init_wallet_table()

init_app()

app.include_router(wallet_router)
