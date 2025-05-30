# app/routers/root.py (new file or inline in the same file)

from fastapi import APIRouter, Depends
from app.services.auth.auth import validate_token, PermissionsValidator

router = APIRouter(
  prefix="/api/v1",
  tags=["Root"],
  responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_root():
    return {"status": "ok"}

@router.get("/public")
def public():
    return {"text": "This is a public message."}

@router.get("/protected", dependencies=[Depends(validate_token)])
def protected():
    return {"text": "This is a protected message."}

@router.get("/admin", dependencies=[Depends(PermissionsValidator(["read:admin-messages"]))])
def admin():
    return {"text": "This is an admin message."}
