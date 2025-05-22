from fastapi.testclient import TestClient

import pytest

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.api.server import app
from src.api.database.engine import get_session_engine
from src.api.database.models import table_registry

@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    # Override antes de criar o TestClient
    def override_get_session_engine_test():
        print("BANCO TESTE SENDO USADO")
        return session

    app.dependency_overrides[get_session_engine] = override_get_session_engine_test

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()