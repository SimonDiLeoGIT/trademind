from dataclasses import dataclass

import jwt

from fastapi import HTTPException, status
from app.core.config import settings

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