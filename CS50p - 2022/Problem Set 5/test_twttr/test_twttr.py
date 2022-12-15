from twttr import shorten

def test_shorten():
    assert shorten("aeiou") == ""
    assert shorten("twitter") == "twttr"
    assert shorten("aaabAAA") == "b"
    assert shorten("Ei123aO") == "123"
    assert shorten("hello, world.") == "hll, wrld."