from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from app.core.database import db

from app.models.User import User


router = APIRouter(
  prefix="/api/users",
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

@router.get("/me")
def read_current_user(user=Depends(get_current_user)):
    # user es el payload del token validado (contiene datos de Auth0, p.ej. sub, email, etc)
    return {"user": user}

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
