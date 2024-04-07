import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    b = Budget(amount=100, limit=1000, period='week', pk=1)
    assert 100 == b.amount
    assert 1000 == b.limit
    assert 'week' == b.period
    assert 1 == b.pk


def test_create_brief():
    b = Budget(100, 1000)
    assert 100 == b.amount
    assert 1000 == b.limit


def test_can_add_to_repo(repo):
    b = Budget(100, 1000)
    pk = repo.add(b)
    assert b.pk == pk
