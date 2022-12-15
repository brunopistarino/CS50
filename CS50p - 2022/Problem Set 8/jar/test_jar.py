from jar import Jar


def test_init():
    jar1 = Jar()
    assert jar1.capacity == 12
    jar2 = Jar(20)
    assert jar2.capacity == 20


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(2)
    assert str(jar) == "🍪🍪"
    jar.deposit(8)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar()
    assert jar.size == 0
    jar.deposit(2)
    assert jar.size == 2


def test_withdraw():
    jar = Jar()
    assert jar.size == 0
    jar.deposit(7)
    jar.withdraw(2)
    assert jar.size == 5