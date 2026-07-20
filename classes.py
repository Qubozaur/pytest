class Foo:
    def __init__(self, val) -> None:
        self.val = val

    def __eq__(self, other) -> bool:
        return self.val == other.val


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


class MailAdminClient:
    def create_user(self):
        return MailUser()

    def delete_user(self, user):
        pass


class MailUser:
    def __init__(self):
        self.inbox = []

    def send_email(self, email, other):
        other.inbox.append(email)

    def clear_mailbox(self):
        self.inbox.clear()


class Email:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body


class BankAccount:
    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("balance cannot be negative")
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdraw must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance

    def transfer(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, name, price, quantity=1):
        if price < 0:
            raise ValueError("price cannot be negative")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if name in self.items:
            old_price, old_qty = self.items[name]
            self.items[name] = (old_price, old_qty + quantity)
        else:
            self.items[name] = (price, quantity)

    def remove_item(self, name):
        if name not in self.items:
            raise KeyError(name)
        del self.items[name]

    def total(self):
        return sum(price * qty for price, qty in self.items.values())

    def count(self):
        return sum(qty for _, qty in self.items.values())


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)
