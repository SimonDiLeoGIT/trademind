from app.services.auth.auth_header_elements import get_bearer_token
from fastapi import Depends, HTTPException, status
from app.services.auth.json_web_token import JsonWebToken

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


def validate_token(token: str = Depends(get_bearer_token)):
    payload = JsonWebToken(access_token=token).validate()
    if "permissions" not in payload:
        payload["permissions"] = []  # o lanzar una excepción
    return payload


class PermissionsValidator:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(validate_token)):
        token_permissions = token.get("permissions")
        token_permissions_set = set(token_permissions)
        required_permissions_set = set(self.required_permissions)

        if not required_permissions_set.issubset(token_permissions_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
            )