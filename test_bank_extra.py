import pytest
from classes import BankAccount


@pytest.fixture
def two_accounts():
    a = BankAccount("A", 200)
    b = BankAccount("B", 50)
    return a, b


def test_transfer_full_balance(two_accounts):
    a, b = two_accounts
    a.transfer(b, 200)
    assert a.balance == 0
    assert b.balance == 250


def test_transfer_insufficient(two_accounts):
    a, b = two_accounts
    with pytest.raises(ValueError):
        a.transfer(b, 999)


@pytest.mark.usefixtures("empty_account")
class TestUsingFixtureMark:
    def test_placeholder(self, empty_account):
        assert empty_account.owner == "Alice"


def test_multiple_operations(funded_account):
    funded_account.deposit(50)
    funded_account.withdraw(30)
    funded_account.deposit(10)
    assert funded_account.balance == 130


@pytest.mark.parametrize("amount", [1, 10, 50, 100])
def test_withdraw_valid_amounts(funded_account, amount):
    before = funded_account.balance
    funded_account.withdraw(amount)
    assert funded_account.balance == before - amount
