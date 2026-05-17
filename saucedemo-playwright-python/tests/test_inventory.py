import pytest
from fixtures.products import Products
from utils.helpers import get_price_value

@pytest.mark.smoke
def test_add_to_cart_and_badge_update(logged_in_page, test_info):
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
def test_product_sorting_all_options(logged_in_page, sort_option, label, test_info):
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

@pytest.mark.smoke
def test_inventory_page_products_data_validation(logged_in_page, test_info):
    """驗證商品列表頁上的所有商品名稱、描述、價格、圖片是否與系統預設資料(Fixtures)完全一致"""
    
    golden_data = [
        Products.BACKPACK, Products.BIKE_LIGHT, Products.BOLT_TSHIRT,
        Products.FLEECE_JACKET, Products.ONESIE, Products.TEST_ALL_THE_THINGS_TSHIRT
    ]
    
    test_info["data"] = f"商品總數: {len(golden_data)}"
    test_info["expected"] = "列表商品資訊(名稱、描述、價格、圖片)應與預期完全一致"
    
    logged_in_page.page.wait_for_selector(".inventory_item", state="visible")
    items = logged_in_page.page.locator(".inventory_item").all()
    
    assert len(items) == len(golden_data), f"預期 {len(golden_data)} 項商品，實際顯示 {len(items)} 項"
    
    diffs = []
    for i, expected_item in enumerate(golden_data):
        item = items[i]
        actual_name = item.locator(".inventory_item_name").inner_text()
        actual_desc = item.locator(".inventory_item_desc").inner_text()
        actual_price = item.locator(".inventory_item_price").inner_text()
        actual_img = item.locator(".inventory_item_img img").get_attribute("src")
        
        item_diffs = []
        if actual_name != expected_item.name: item_diffs.append("名稱")
        if actual_desc != expected_item.description: item_diffs.append("描述")
        if actual_price != expected_item.price: item_diffs.append("價格")
        if expected_item.image_url.split('/')[-1] not in actual_img: item_diffs.append("圖片")
        
        if item_diffs:
            diffs.append(f"商品 {i+1} ({expected_item.name}) 差異: {', '.join(item_diffs)}")
            
    if diffs:
        test_info["actual"] = "<br>".join(diffs)
        pytest.fail(f"商品資訊驗證失敗: {diffs}")
    else:
        test_info["actual"] = "所有商品資訊驗證無誤"

