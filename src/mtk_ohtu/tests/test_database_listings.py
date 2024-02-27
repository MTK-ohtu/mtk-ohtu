"""Tests for listing funcitons in database"""
import mtk_ohtu.database.db_listings as db_list
from mtk_ohtu.database import db_enums as dbe


def test_get_all_listings_correct_amount(datapool):
    prodlist = db_list.db_get_product_list(datapool)
    assert len(prodlist) == 13

def test_product_by_id_returns_correct_product_with_id(datapool):
    product_id = 1
    product = db_list.db_get_product_by_id(product_id, datapool)
    assert product.category == dbe.CategoryType.DIGESTION

def test_product_by_id_returns_none_for_nonexistant_product(datapool):
    product_id = 2000
    product = db_list.db_get_product_by_id(product_id, datapool)
    assert product is None
