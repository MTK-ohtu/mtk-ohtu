import mtk_ohtu.database.db_listings as db_list


def test_get_all_listings_correct_amount(datapool):
    prodlist = db_list.db_get_product_list(datapool)
    assert len(prodlist) == 13
