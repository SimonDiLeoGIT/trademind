from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Query, Request
from sqlmodel import Session, select

from app.core.database import db

from app.core.config import settings

from app.models.User import User

from app.services.auth.auth import oauth


router = APIRouter(
  prefix="/api/v1/users",
  tags=["Users"],
  responses={404: {"description": "Not found"}},
)

class UserUpdate(User):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

@router.post("/", response_model=User)
def create_user(user: User, session: Annotated[Session, Depends(db.get_session)]) -> User:
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/")
def get_users(session: Annotated[Session, Depends(db.get_session)], offset: int = 0, limit:  Annotated[int, Query(le=100)] = 100) -> list[User]:
  users = session.exec(select(User).offset(offset).limit(limit)).all()
  return users

@router.get("/{user_id}")
def get_users(session: Annotated[Session, Depends(db.get_session)], user_id: int) -> User:

  user = session.exec(select(User).where(User.id == user_id)).first()
  return user

@router.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session: Annotated[Session, Depends(db.get_session)]):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete("/useres/{user_id}")
def delete_user(user_id: int, session: Annotated[Session, Depends(db.get_session)]):
    user = session.get(user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


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
