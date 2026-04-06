import pytest

@pytest.fixture(scope="function")
def db_session():
    # create session
    yield session
    # rollback changes