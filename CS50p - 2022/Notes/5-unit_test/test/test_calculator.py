from calculator import square
import pytest


def test_positive():
    assert square(2) == 4
    assert square(3) == 9


def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9


def test_zero():
    assert square(0) == 0


def test_string():
    with pytest.raises(TypeError):
        square("a")

# pytest test
# python -m pytest test
