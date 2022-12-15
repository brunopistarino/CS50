from fuel import convert, gauge
import pytest

def test_convert():
    assert convert("0/1") == 0
    assert convert("1/2") == 50
    assert convert("1/1") == 100

    with pytest.raises(ValueError):
        assert convert("a/1")
        assert convert("1/a")
        assert convert("a/a")
        assert convert("2/1")

    with pytest.raises(ZeroDivisionError):
        assert convert("1/0")


def test_gauge():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(50) == "50%"
    assert gauge(99) == "F"
    assert gauge(100) == "F"