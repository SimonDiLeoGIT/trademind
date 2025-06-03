from dataclasses import dataclass

import jwt

from fastapi import HTTPException, status
from app.core.config import settings

from fastapi import Depends, HTTPException, status

from app.services.authentication.auth_header_elements import get_bearer_token

@dataclass
class JsonWebToken:
  
  access_token: str
  auth0_issuer_url: str = f"https://{settings.AUTH0_DOMAIN}/"
  auth0_audience: str = settings.AUTH0_AUDIENCE
  algorithm: str = "RS256"
  jwks_uri: str = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"

  def validate(self):
    try:
      
      jwks_client = jwt.PyJWKClient(self.jwks_uri)
      signing_key = jwks_client.get_signing_key_from_jwt(self.access_token).key

      payload = jwt.decode(
        self.access_token,
        signing_key,
        algorithms=[self.algorithm],
        audience=self.auth0_audience, 
        issuer=self.auth0_issuer_url
      )
    
    except jwt.exceptions.PyJWKClientError:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to verify credentials"
            )
    
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bad credentials"
            )
    
    return payload


def validate_token(token: str = Depends(get_bearer_token)):
    payload = JsonWebToken(access_token=token).validate()
    print(payload)
    if "permissions" not in payload:
        payload["permissions"] = []
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