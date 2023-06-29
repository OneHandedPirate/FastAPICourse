import pytest

from app.calculations import add, subtract, multiply, divide


@pytest.mark.parametrize("a, b, expected", [
    (2, 5, 7),
    (8, 8, 16),
    (-9, 7, -2),
    (-10, -11, -21)
])
def test_add(a, b, expected):
    print("Testing add")
    assert add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (2, 5, -3),
    (8, 8, 0),
    (-9, 7, -16),
    (-10, -11, 1)
])
def test_subtract(a, b, expected):
    print("Testing subtract")
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (2, 5, 10),
    (8, 8, 64),
    (-9, 7, -63),
    (-10, -11, 110)
])
def test_multiply(a, b, expected):
    print("Testing multiply")
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (2, 5, 0.4),
    (8, 8, 1.0),
    (-10, 10, -1.0),
    (0, 1, 0)
])
def test_divide(a, b, expected):
    print("Testing divide")
    assert divide(a, b) == expected


