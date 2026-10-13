
import pytest
from src.inventory import Inventory


def test_add_stock():
    inventory = Inventory()
    inventory.add_stock('pen', 10)
    assert inventory.stock['pen'] == 10


def test_remove_stock():
    inventory = Inventory()
    inventory.add_stock('pen', 10)
    inventory.remove_stock('pen', 3)
    assert inventory.stock['pen'] == 7


def test_remove_too_much():
    inventory = Inventory()
    inventory.add_stock('pen', 2)

    with pytest.raises(ValueError):
        inventory.remove_stock('pen', 5)
