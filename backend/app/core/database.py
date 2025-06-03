from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

class Database:
  def __init__(self):
    self.database_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    self.engine = create_engine(self.database_url, echo=True)  

  def create_db_and_tables(self):
    SQLModel.metadata.create_all(self.engine)

  def get_session(self):
    with Session(self.engine) as session:
      yield session


# Singleton instance
db = Database()

# Dependency
# SessionDep = Annotated[Session, Depends(db.get_session)]