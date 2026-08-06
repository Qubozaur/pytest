from main import (
    func,
    add,
    subtract,
    multiply,
    divide,
    is_even,
    greet,
    reverse_string,
    max_of_three,
    sum_list,
    find_in_list,
)
import pytest
from classes import *


def test_answer():
    assert func(4) == 5


def test_float():
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_set_comparison():
    set1 = set("1308")
    set2 = set("8031")
    assert set1 == set2


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing foo instances:",
            f"vals: {left.val} != {right.val}",
        ]


def test_foo_instances():
    x1 = Foo(1)
    x2 = Foo(1)
    assert x1 == x2


@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("pear")]


def test_fruit_salad(fruit_bowl):
    fruit_salad = FruitSalad(*fruit_bowl)
    assert all(fruit.cubed for fruit in fruit_salad.fruit)


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    order.append("b")
    assert order == ["a", "b"]


def test_int(order):
    order.append(2)
    assert order == ["a", 2]


@pytest.fixture
def mail_admin():
    return MailAdminClient()


@pytest.fixture
def sending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    mail_admin.delete_user(user)


@pytest.fixture
def receiving_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    user.clear_mailbox()
    mail_admin.delete_user(user)


def test_email_received(sending_user, receiving_user):
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    assert email in receiving_user.inbox


@pytest.fixture
def fixt(request):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        data = None
    else:
        data = marker.args[0]
    return data


@pytest.mark.fixt_data(42)
def test_fixt_data(fixt):
    assert fixt == 42


@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected


@pytest.mark.parametrize("n,expected", [(3, 4), (5, 6)])
class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_more_case(self, n, expected):
        assert (n * 1) + 1 == expected


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6


def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == pytest.approx(3.5)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_divide_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(5, 0)


def test_is_even():
    assert is_even(2) is True
    assert is_even(3) is False
    assert is_even(0) is True


def test_greet():
    assert greet("Anna") == "Hello, Anna!"


def test_greet_empty():
    with pytest.raises(ValueError, match="name cannot be empty"):
        greet("")


def test_reverse_string():
    assert reverse_string("abc") == "cba"
    assert reverse_string("") == ""
    assert reverse_string("kayak") == "kayak"


def test_max_of_three():
    assert max_of_three(1, 2, 3) == 3
    assert max_of_three(9, 2, 5) == 9
    assert max_of_three(-1, -5, -3) == -1


def test_sum_list():
    assert sum_list([1, 2, 3]) == 6
    assert sum_list([]) == 0
    assert sum_list([-1, 1]) == 0


def test_find_in_list():
    assert find_in_list(["a", "b", "c"], "b") == 1


def test_find_in_list_missing():
    with pytest.raises(LookupError):
        find_in_list([1, 2, 3], 99)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 1, 2),
        (0, 5, 5),
        (-3, 3, 0),
        (100, 200, 300),
    ],
    ids=["ones", "zero", "neg_pos", "large"],
)
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, True),
        (1, False),
        (2, True),
        (7, False),
        (-4, True),
    ],
)
def test_is_even_parametrized(n, expected):
    assert is_even(n) is expected


@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    assert False


@pytest.mark.skipif(True, reason="always skipped for now")
def test_skip_if_demo():
    assert 1 == 2


@pytest.mark.xfail(reason="known bug")
def test_known_bug():
    assert add(2, 2) == 5


def test_capsys_greet(capsys):
    print(greet("World"))
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out


def test_tmp_path_write(tmp_path):
    file = tmp_path / "note.txt"
    file.write_text("pytest rocks")
    assert file.read_text() == "pytest rocks"


def test_tmp_path_multiple_files(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    (d / "a.txt").write_text("aaa")
    (d / "b.txt").write_text("bbb")
    files = list(d.iterdir())
    assert len(files) == 2


def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")
    import os

    assert os.environ["APP_MODE"] == "test"


def test_monkeypatch_setattr(monkeypatch):
    monkeypatch.setattr("main.add", lambda a, b: 100)
    from main import add as patched_add

    assert patched_add(1, 2) == 100


def test_sample_numbers_fixture(sample_numbers):
    assert sum_list(sample_numbers) == 15
    assert len(sample_numbers) == 5


def test_small_int_fixture(small_int):
    assert small_int in (1, 2, 3)
    assert is_even(small_int) or not is_even(small_int)


from main import (
    is_palindrome,
    factorial,
    count_vowels,
    flatten_list,
    unique_items,
    merge_dicts,
    is_prime,
    chunk_list,
    safe_divide,
    Stack,
)


def test_is_palindrome_true():
    assert is_palindrome("kayak") is True
    assert is_palindrome("Was it a car or a cat I saw") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


@pytest.mark.parametrize(
    "text,expected",
    [
        ("madam", True),
        ("racecar", True),
        ("python", False),
        ("", True),
    ],
)
def test_is_palindrome_parametrized(text, expected):
    assert is_palindrome(text) is expected


def test_factorial_basic():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120


def test_factorial_negative_raises():
    with pytest.raises(ValueError, match="not defined for negative numbers"):
        factorial(-3)


def test_count_vowels():
    assert count_vowels("Hello World") == 3
    assert count_vowels("xyz") == 0
    assert count_vowels("AEIOU") == 5


def test_flatten_list_simple():
    assert flatten_list([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]


def test_flatten_list_already_flat():
    assert flatten_list([1, 2, 3]) == [1, 2, 3]


def test_flatten_list_empty():
    assert flatten_list([]) == []


def test_unique_items():
    assert unique_items([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]


def test_unique_items_empty():
    assert unique_items([]) == []


def test_merge_dicts_no_overlap():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_merge_dicts_overlap_second_wins():
    assert merge_dicts({"a": 1}, {"a": 2}) == {"a": 2}


@pytest.mark.parametrize(
    "n,expected",
    [
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (18, False),
        (0, False),
        (-5, False),
    ],
)
def test_is_prime(n, expected):
    assert is_prime(n) is expected


def test_chunk_list_even():
    assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_list_uneven():
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_list_invalid_size():
    with pytest.raises(ValueError, match="size must be positive"):
        chunk_list([1, 2, 3], 0)


def test_safe_divide_normal():
    assert safe_divide(10, 2) == 5


def test_safe_divide_by_zero_default_none():
    assert safe_divide(10, 0) is None


def test_safe_divide_by_zero_custom_default():
    assert safe_divide(10, 0, default=-1) == -1


@pytest.fixture
def stack():
    return Stack()


def test_stack_push_pop(stack):
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_stack_peek_does_not_remove(stack):
    stack.push(10)
    assert stack.peek() == 10
    assert len(stack) == 1


def test_stack_is_empty(stack):
    assert stack.is_empty() is True
    stack.push(1)
    assert stack.is_empty() is False


def test_stack_pop_empty_raises(stack):
    with pytest.raises(IndexError, match="pop from empty stack"):
        stack.pop()


def test_stack_peek_empty_raises(stack):
    with pytest.raises(IndexError, match="peek from empty stack"):
        stack.peek()


def test_stack_len(stack):
    for i in range(5):
        stack.push(i)
    assert len(stack) == 5