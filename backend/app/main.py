from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services import stocks_service
from app.core.database import db

from app.routers import users, root

from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(
    title="Market Index Tracker API",
    description="Backend para monitoreo de índices del mercado",
    version="1.0.0",
)

# CORS settings (ajustá según el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, limitá esto a tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="secret")

# Incluir rutas
app.include_router(stocks_service.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(users.router)
app.include_router(root.router)
# app.include_router(indices.router, prefix="/api/indices", tags=["Indices"])

@app.on_event("startup")
def on_startup():
    db.create_db_and_tables()
