import pytest
from classes import BankAccount, ShoppingCart, Stack, Foo


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "upper")


class TestBankAccount:
    def test_create_with_balance(self, funded_account):
        assert funded_account.owner == "Bob"
        assert funded_account.balance == 100

    def test_create_empty(self, empty_account):
        assert empty_account.balance == 0

    def test_negative_balance_raises(self):
        with pytest.raises(ValueError, match="balance cannot be negative"):
            BankAccount("Eve", balance=-10)

    def test_deposit(self, empty_account):
        assert empty_account.deposit(50) == 50
        assert empty_account.balance == 50

    def test_deposit_invalid(self, empty_account):
        with pytest.raises(ValueError):
            empty_account.deposit(0)
        with pytest.raises(ValueError):
            empty_account.deposit(-5)

    def test_withdraw(self, funded_account):
        assert funded_account.withdraw(40) == 60

    def test_withdraw_too_much(self, funded_account):
        with pytest.raises(ValueError, match="insufficient funds"):
            funded_account.withdraw(200)

    def test_transfer(self, funded_account, empty_account):
        funded_account.transfer(empty_account, 30)
        assert funded_account.balance == 70
        assert empty_account.balance == 30


class TestShoppingCart:
    def test_empty_total(self, empty_cart):
        assert empty_cart.total() == 0
        assert empty_cart.count() == 0

    def test_add_item(self, empty_cart):
        empty_cart.add_item("milk", 3.5, 2)
        assert empty_cart.count() == 2
        assert empty_cart.total() == pytest.approx(7.0)

    def test_add_same_item_twice(self, empty_cart):
        empty_cart.add_item("egg", 1.0, 2)
        empty_cart.add_item("egg", 1.0, 3)
        assert empty_cart.count() == 5
        assert empty_cart.total() == pytest.approx(5.0)

    def test_filled_cart(self, filled_cart):
        assert filled_cart.count() == 4
        assert filled_cart.total() == pytest.approx(11.5)

    def test_remove_item(self, filled_cart):
        filled_cart.remove_item("apple")
        assert "apple" not in filled_cart.items
        assert filled_cart.total() == pytest.approx(4.0)

    def test_remove_missing(self, empty_cart):
        with pytest.raises(KeyError):
            empty_cart.remove_item("ghost")

    def test_negative_price(self, empty_cart):
        with pytest.raises(ValueError):
            empty_cart.add_item("bad", -1)


class TestStack:
    def test_push_pop(self, stack):
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_peek(self, stack):
        stack.push("x")
        assert stack.peek() == "x"
        assert stack.size() == 1

    def test_empty(self, stack):
        assert stack.is_empty() is True
        with pytest.raises(IndexError):
            stack.pop()
        with pytest.raises(IndexError):
            stack.peek()

    def test_size(self, stack):
        for i in range(5):
            stack.push(i)
        assert stack.size() == 5


class TestFoo:
    def test_equal(self):
        assert Foo(10) == Foo(10)

    def test_not_equal(self):
        assert Foo(1) != Foo(2)


@pytest.mark.parametrize(
    "start,deposit,expected",
    [
        (0, 10, 10),
        (50, 25, 75),
        (100, 1, 101),
    ],
)
def test_deposit_parametrized(start, deposit, expected):
    account = BankAccount("Pat", balance=start)
    assert account.deposit(deposit) == expected
