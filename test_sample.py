import pytest

def test_addition():
    assert 2 + 3 == 5

def test_string():
    assert "qa".upper() == "QA"

def test_list():
    assert len([1, 2, 3]) == 3

@pytest.mark.smoke
def test_login():
    assert True