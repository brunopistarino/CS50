from bank import value


def test_bank():
    assert value("hello") == 0
    assert value("HeLlO") == 0
    assert value("Hi") == 20
    assert value("cat") == 100