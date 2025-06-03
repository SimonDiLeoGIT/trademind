from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
  __tablename__ = "users"
  id: int | None = Field(default=None, primary_key=True)
  nickname: str = Field(index=True)
  username: str
  useremail: str
  auth0_id: str