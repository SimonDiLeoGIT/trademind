import requests, os
from app.core.config import settings

from fastapi import HTTPException, APIRouter, Request

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.requests_client import OAuthError

from fastapi.middleware.cors import CORSMiddleware

from starlette.config import Config

# from starlette.responses import JSONResponse
# from starlette.templating import Jinja2Templates


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


@router.post("/token")
def get_auth_token():
  headers = {"Content-Type": "application/json"}

  payload = {
      "client_id": settings.AUTH0_CLIENT_ID,
      "client_secret": settings.AUTH0_CLIENT_SECRET,
      "audience": settings.AUTH0_AUDIENCE,
      "grant_type": "client_credentials"
  }

  try:
      response = requests.post(
          f"https://{settings.AUTH0_DOMAIN}/oauth/token",
          json=payload,
          headers=headers
      )
      response.raise_for_status()
      return response.json()
  except requests.exceptions.RequestException as e:
      raise HTTPException(status_code=500, detail=f"Auth0 Error: {str(e)}")
  
@router.get("/login")
async def login(request: Request):
    redirect_uri = settings.AUTH0_CALLBACK_URL
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    userinfo = await oauth.auth0.parse_id_token(request, token)
    # Save in session if needed
    request.session["user"] = dict(userinfo)
    return userinfo

# @router.route("/logout")
# def logout():
#     session.clear()
#     return redirect(
#         "https://" + env.get("AUTH0_DOMAIN")
#         + "/v2/logout?"
#         + urlencode(
#             {
#                 "returnTo": url_for("home", _external=True),
#                 "client_id": env.get("AUTH0_CLIENT_ID"),
#             },
#             quote_via=quote_plus,
#         )
#     )