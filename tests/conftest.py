from typing import Generator
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import SQLModel, Session
from app.db.db import get_db

from main import app


DATABASE_URL = "sqlite:///:memory"

@pytest.fixture(scope="session")
def connection():
    engine = create_engine(DATABASE_URL, poolclass=StaticPool, echo=False)

    if not database_exists(engine.url):
        create_database(engine.url)

    connection = engine.connect()

    yield connection

    connection.close()
    drop_database(engine.url)


@pytest.fixture(scope="function")
def setup_db(connection, request) -> None:
    SQLModel.metadata.create_all(bind=connection)

    def teardown():
        SQLModel.metadata.drop_all(bind=connection)

    request.addfinalizer(teardown)

    return None

@pytest.fixture()
def db_session(connection, setup_db, request) -> Session:
    session = Session(bind=connection)
    session.begin_nested()

    def teardown():
        connection.rollback()
        session.close()

    request.addfinalizer(teardown)

    return session


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:

    def get_fake_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = get_fake_db

    with TestClient(app) as test_client:
        yield test_client
