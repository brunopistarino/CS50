from seasons import get_date
from datetime import date

def test_get_date():
    assert get_date("1999-01-01") == date(1999, 1, 1)
    assert get_date("1999-12-31") == date(1999, 12, 31)
    assert get_date("1970-01-01") == date(1970, 1, 1)
    assert get_date("January 1, 1999") == False