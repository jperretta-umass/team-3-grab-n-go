import os

import pytest

# Import the SQLAlchemy Base so tests can create/drop the schema
# in the dedicated test database.
# get_db is imported so we can override the normal FastAPI database
# dependency and force the app to use the test session during tests.
from app.database import Base, get_db

# Import the FastAPI app instance used by TestClient.
from app.main import app

# These are the current models used by the test template.
# IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
# If models.py changes (field names, relationships, required columns, etc.),
# this file will likely need updates in:
# - seed_test_data()
# - imported model list
# - any assumptions used by the tests
from app.models import CustomerProfile, DelivererProfile, User
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# This points tests to the separate Dockerized test database.
# If the test database service name, database name, or DB driver changes,
# update this URL or .env.test accordingly.
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://app:app_pw@test_db:5432/app_test_db",
)

# Dedicated engine/session factory for tests only.
# This keeps the test database isolated from the development database.
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def seed_test_data(db):
    """
    Seed the test database with example data.

    This is TEMPLATE DATA for the testing framework, not necessarily the final
    production schema/data.

    IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
    If the real database schema changes, update this function to match:
    - new required columns
    - new foreign keys
    - renamed tables/fields
    - changed relationships

    These tests currently assume:
    - 2 users exist
    - 1 customer profile exists
    - 1 deliverer profile exists
    - sample dining halls/items exist
    - a customer cart exists
    """

    # Example customer user.
    user_1 = User(
        username="alice",
        email="alice@example.com",
        phone_num="111-111-1111",
        has_deliverer_profile=False,
    )

    # Example deliverer user.
    user_2 = User(
        username="bob",
        email="bob@example.com",
        phone_num="222-222-2222",
        has_deliverer_profile=True,
    )

    db.add_all([user_1, user_2])
    db.commit()
    db.refresh(user_1)
    db.refresh(user_2)

    # Example customer profile tied to user_1.
    customer_profile = CustomerProfile(
        user_id=user_1.id,
        current_order_id=None,
        past_order_id=None,
    )

    # Example deliverer profile tied to user_2 later via deliverer_id.
    deliverer_profile = DelivererProfile(
        past_order_id=None,
        current_order_id=None,
    )

    db.add_all([customer_profile, deliverer_profile])
    db.commit()
    db.refresh(deliverer_profile)

    # Link deliverer user to deliverer profile.
    # If the final schema changes how this relationship is stored,
    # update this line and related tests.
    user_2.deliverer_id = deliverer_profile.id
    db.commit()
    db.refresh(user_2)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Test database setup/teardown for the full pytest session.

    What it does:
    - drops all tables
    - recreates all tables
    - seeds initial test data
    - drops all tables after tests finish

    IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
    If the team switches from create_all/drop_all to migrations (Alembic),
    this fixture is the main place that should be updated.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    seed_test_data(db)
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """
    Per-test database session.

    Each test gets its own transaction so changes can be rolled back after
    the test finishes.

    This keeps tests isolated and prevents one test from affecting another.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    """
    FastAPI TestClient fixture.

    Overrides the app's normal get_db dependency so API tests use the test
    database session instead of the development database.

    IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
    If app dependency injection changes, update this override logic.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
