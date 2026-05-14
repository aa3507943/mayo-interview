import pytest
from fixtures.products import Products
from utils.helpers import get_price_value

@pytest.mark.smoke
def test_購物車內容跨頁面保存與金額驗證(logged_in_page, cart_page, test_info):
    """驗證加入商品後，進入購物車頁面資訊（名稱、價格）是否完全正確"""
    test_info["data"] = f"商品: {Products.BACKPACK.name}"
    test_info["expected"] = "購物車應正確顯示商品名稱，且價格應為 " + Products.BACKPACK.price
    
    logged_in_page.add_to_cart(Products.BACKPACK.name)
    logged_in_page.go_to_cart()
    
    # 驗證名稱
    item_name = cart_page.page.locator(".inventory_item_name").inner_text()
    assert item_name == Products.BACKPACK.name
    
    # 驗證價格
    item_price_text = cart_page.page.locator(".inventory_item_price").inner_text()
    assert get_price_value(item_price_text) == get_price_value(Products.BACKPACK.price)
    
    test_info["actual"] = f"驗證通過！購物車商品: {item_name}, 價格: {item_price_text}"

@pytest.mark.regression
def test_在購物車頁面移除商品後清單清空(logged_in_page, cart_page, test_info):
    """驗證在購物車頁面移除商品後，商品清單應即時消失"""
    test_info["data"] = f"商品: {Products.BACKPACK.name}"
    test_info["expected"] = "移除後商品清單應不含任何項目"
    
    logged_in_page.add_to_cart(Products.BACKPACK.name)
    logged_in_page.go_to_cart()
    cart_page.remove_item(Products.BACKPACK.name)
    
    # 檢查商品行數
    count = cart_page.get_items_count()
    assert count == 0
    test_info["actual"] = "確認商品已從清單中完全移除"
