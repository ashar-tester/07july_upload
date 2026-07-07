import pytest

@pytest.fixture
def user_data():
    return {"username": "admin", "password": "admin123"}

def login(username, password):
    return username == "admin" and password == "admin123"

def test_valid_login(user_data):
    assert login(user_data["username"], user_data["password"])

def test_invalid_login(user_data):
    assert not login(user_data["username"], "wrong")