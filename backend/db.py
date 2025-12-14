from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./app.db"

# creates the database engine in debugging mode
engine = create_engine(DATABASE_URL, echo=True)

# initialize database
def init_db():
    # scans all classes if they inherit from SQLModel and creates tables
    SQLModel.metadata.create_all(engine)
