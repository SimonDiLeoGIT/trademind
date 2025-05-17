from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
  __tablename__ = "users"
  id: int | None = Field(default=None, primary_key=True)
  username: str = Field(index=True)
  useremail: str
  password: str