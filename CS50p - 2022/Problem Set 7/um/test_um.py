from um import count

def test_word():
    assert count("um") == 1
    assert count("um?") == 1

def test_sentence():
    assert count("Um, thanks for the album.") == 1
    assert count("Um, thanks, um...") == 2

def test_blank():
    assert count("") == 0
    assert count("hey") == 0