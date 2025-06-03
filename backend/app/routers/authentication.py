from fastapi import Request, APIRouter

from authlib.integrations.starlette_client import OAuth  

from app.core.config import settings

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration'
)

router = APIRouter(
  prefix="/api/v1/authentication",
  tags=["Users"],
  responses={404: {"description": "Not found"}},
)

@router.post("/login")
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

# @app.route("/logout")
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
