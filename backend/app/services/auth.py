from urllib.parse import quote_plus, urlencode
import requests, os
from app.core.config import settings

from fastapi import HTTPException, APIRouter, Request
from fastapi.responses import RedirectResponse

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.requests_client import OAuthError

from fastapi.middleware.cors import CORSMiddleware

from starlette.config import Config

# from starlette.responses import JSONResponse
# from starlette.templating import Jinja2Templates

# Middleware para obtener token del header Authorization
http_bearer = HTTPBearer()

# get auth0 public keys
def get_jwks():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    return requests.get(jwks_url).json()

jwks = get_jwks()


router = APIRouter(
  prefix="/api/auth",
  tags=["Auth"],
  responses={404: {"description": "Not found"}},
)

oauth = OAuth()

oauth.register(
    name='auth0',
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration'
)
  
