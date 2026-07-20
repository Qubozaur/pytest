import pytest
from classes import BankAccount, ShoppingCart, Stack


@pytest.fixture
def empty_account():
    return BankAccount("Alice")


@pytest.fixture
def funded_account():
    return BankAccount("Bob", balance=100)


@pytest.fixture
def empty_cart():
    return ShoppingCart()


@pytest.fixture
def filled_cart():
    cart = ShoppingCart()
    cart.add_item("apple", 2.5, 3)
    cart.add_item("bread", 4.0, 1)
    return cart


@pytest.fixture
def stack():
    return Stack()


@pytest.fixture(scope="module")
def sample_numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture(params=[1, 2, 3])
def small_int(request):
    return request.param
