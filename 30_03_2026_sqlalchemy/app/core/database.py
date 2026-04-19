from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine("sqlite:///cinema.db", echo=False)

session_maker = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

def init_db():
     Base.metadata.create_all(bind=engine)

def get_session():
    with sessionmaker() as session:
        try:
            yield session
        finally:
            session.close()