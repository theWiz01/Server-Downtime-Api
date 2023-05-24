from sqlmodel import create_engine, SQLModel, Session

# sqlite:///sdtmonitor.db

# postgresql+psycopg2://postgres:admin@localhost/sdtmonitor

engine = create_engine("sqlite:///sdtmonitor.db", connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session