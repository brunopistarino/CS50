from numb3rs import validate

def test_over():
    assert validate("256.1.1.1") == False
    assert validate("1.256.1.1") == False
    assert validate("1.1.256.1") == False
    assert validate("1.1.1.256") == False

def test_under():
    assert validate("255.1.1.1") == True
    assert validate("255.255.1.1") == True
    assert validate("255.255.255.1") == True
    assert validate("255.255.255.255") == True

def test_invalid():
    assert validate("1.1.1") == False
    assert validate("1.1") == False
    assert validate("1") == False
    assert validate("") == False