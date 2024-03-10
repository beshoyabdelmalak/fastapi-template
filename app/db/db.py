from typing import Generator
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///items.db"


engine = create_engine(DATABASE_URL, echo=True)


def get_db()-> Generator[Session, None, None]:
    database = Session(engine)
    try:
        yield database
    finally:
        database.close()
