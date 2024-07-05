from project import strike, color, is_pending


def test_strike():
    assert strike("Hello") == "H\u0336e\u0336l\u0336l\u0336o\u0336"
    assert strike(
        "Hello World") == "H\u0336e\u0336l\u0336l\u0336o\u0336 \u0336W\u0336o\u0336r\u0336l\u0336d\u0336"
    assert strike(
        "Hello World!") == "H\u0336e\u0336l\u0336l\u0336o\u0336 \u0336W\u0336o\u0336r\u0336l\u0336d\u0336!\u0336"
    assert strike(
        "this is cs50") == "t\u0336h\u0336i\u0336s\u0336 \u0336i\u0336s\u0336 \u0336c\u0336s\u03365\u03360\u0336"


def test_color():
    assert color("Hello") == "\33[92mHello\033[0m"
    assert color("Hello World") == "\33[92mHello World\033[0m"
    assert color("Hello World!") == "\33[92mHello World!\033[0m"
    assert color("this is cs50") == "\33[92mthis is cs50\033[0m"


def test_is_pending():
    assert is_pending({"task": "Hello", "done": "False"})
    assert not is_pending({"task": "Hello", "done": "True"})
    assert is_pending({"task": "Hello World", "done": "False"})
    assert not is_pending({"task": "Hello World", "done": "True"})
    assert is_pending({"task": "Hello World!", "done": "False"})
    assert not is_pending({"task": "Hello World!", "done": "True"})
    assert is_pending({"task": "this is cs50", "done": "False"})
