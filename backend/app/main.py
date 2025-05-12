from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import users, indices  # Importá tus routers
from app.core.config import settings  # Configuración desde .env si usás Pydantic
from app.services import stocks_service

app = FastAPI(
    title="Market Index Tracker API",
    description="Backend para monitoreo de índices del mercado",
    version="1.0.0"
)

# CORS settings (ajustá según el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, limitá esto a tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(stocks_service.router, prefix="/api/stocks", tags=["Stocks"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
# app.include_router(indices.router, prefix="/api/indices", tags=["Indices"])

# Puedes incluir un healthcheck
@app.get("/")
def read_root():
    return {"status": "ok"}
