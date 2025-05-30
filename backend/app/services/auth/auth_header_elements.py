from typing import NamedTuple

from starlette.requests import Request as StartletteRequest

from fastapi import HTTPException, status

class AuthorizationHeaderElements(NamedTuple):
  authorization_scheme: str
  bearer_token: str
  are_valid: bool

def get_authorization_header_elements(authorization_header: str) -> AuthorizationHeaderElements:
  try:
    authorization_scheme, bearer_token = authorization_header.split()
  except ValueError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Bad Credentials",
    )
  else:
    valid = authorization_scheme.lower() == "bearer" and bool(bearer_token.strip())
    return AuthorizationHeaderElements(
      authorization_scheme,
      bearer_token,
      valid
    )

def get_bearer_token(request: StartletteRequest) -> str:
  authorization_header = request.headers.get("Authorization")
  
  if authorization_header:
    athorization_header_elements = get_authorization_header_elements(authorization_header)

    if athorization_header_elements.are_valid:
      return athorization_header_elements.bearer_token
    else:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bad credentials",
      )
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Required authentication",
    )