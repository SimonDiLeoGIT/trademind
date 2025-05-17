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

# class UserCreate(User):
#     secret_name: str

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