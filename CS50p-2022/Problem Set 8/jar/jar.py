class Jar:
    def __init__(self, capacity=12):
        self.capacity = capacity
        self.cookies = 0

    def __str__(self):
        return "🍪" * self.cookies

    def deposit(self, n):
        if self.cookies + n > self._capacity:
            raise ValueError
        self.cookies += n

    def withdraw(self, n):
        if self.cookies - n < 0:
            raise ValueError
        self.cookies -= n

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, n):
        if n < 0:
            raise ValueError
        self._capacity = n

    @property
    def size(self):
        return self.cookies


def main():
    jar = Jar()
    jar.deposit(10)
    print(jar.size)
    print(jar)
    jar.withdraw(2)
    print(jar.size)
    print(jar)


if __name__ == "__main__":
    main()