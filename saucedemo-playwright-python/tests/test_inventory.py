import pytest
from fixtures.products import Products
from utils.helpers import get_price_value

@pytest.mark.smoke
def test_加入購物車與圖示數量更新(logged_in_page, test_info):
    """驗證在列表頁點擊 Add to Cart 後，購物車圖示能即時反應數量"""
    test_info["data"] = f"商品: {Products.BACKPACK.name}, {Products.BIKE_LIGHT.name}"
    test_info["expected"] = "點擊兩件商品後，購物車圖示數字應顯示為 2"
    
    logged_in_page.add_to_cart(Products.BACKPACK.name)
    logged_in_page.add_to_cart(Products.BIKE_LIGHT.name)
    count = logged_in_page.get_cart_count()
    
    assert count == 2
    test_info["actual"] = f"購物車圖示成功更新為 {count}"

@pytest.mark.regression
@pytest.mark.parametrize("sort_option, label", [
    ("hilo", "價格高到低"),
    ("lohi", "價格低到高"),
    ("az", "字母 A-Z"),
    ("za", "字母 Z-A")
], ids=["Price_HiLo", "Price_LoHi", "Name_AZ", "Name_ZA"])
def test_商品全方位排序驗證(logged_in_page, sort_option, label, test_info):
    """驗證所有排序選項（名稱與價格）是否完全符合邏輯"""
    test_info["data"] = f"排序方式: {label}"
    test_info["expected"] = f"列表內容應嚴格符合 {label} 的順序"
    
    logged_in_page.sort_by(sort_option)
    
    if sort_option in ["hilo", "lohi"]:
        # 價格驗證
        price_texts = logged_in_page.page.locator(".inventory_item_price").all_inner_texts()
        prices = [get_price_value(p) for p in price_texts]
        expected = sorted(prices, reverse=(sort_option == "hilo"))
        assert prices == expected
        test_info["actual"] = f"價格排序驗證通過: {prices}"
    else:
        # 名稱字母驗證
        name_elements = logged_in_page.page.locator(".inventory_item_name").all_inner_texts()
        expected = sorted(name_elements, reverse=(sort_option == "za"))
        assert name_elements == expected
        test_info["actual"] = f"名稱排序驗證通過: {name_elements[:2]}..."
