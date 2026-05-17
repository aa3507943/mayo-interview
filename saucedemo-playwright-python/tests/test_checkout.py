import pytest
from fixtures.products import Products
from utils.helpers import get_price_value

@pytest.mark.smoke
def test_complete_checkout_flow_and_total_calculation(logged_in_page, cart_page, checkout_page, test_info):
    """驗證結帳流程，並精確計算 商品總額 + 稅金 = 總計金額"""
    test_info["data"] = f"結帳商品: {Products.BACKPACK.name}"
    test_info["expected"] = "結帳總額應等於 商品單價 + 稅金(約8%)"
    
    logged_in_page.add_to_cart(Products.BACKPACK.name)
    logged_in_page.go_to_cart()
    cart_page.checkout()
    checkout_page.fill_information("Test", "User", "104")
    
    # 獲取結帳摘要
    summary = checkout_page.get_summary_info()
    subtotal = get_price_value(summary["subtotal"])
    tax = get_price_value(summary["tax"])
    total = get_price_value(summary["total"])
    
    # 1. 驗證商品單價是否正確
    assert subtotal == get_price_value(Products.BACKPACK.price)
    
    # 2. 驗證總額計算邏輯 (Subtotal + Tax = Total)
    # 使用 round 處理浮點數運算誤差
    assert round(subtotal + tax, 2) == total
    
    checkout_page.finish_checkout()
    msg = checkout_page.get_complete_message()
    assert "Thank you for your order!" in msg
    
    test_info["actual"] = f"金額計算正確！(小計:{subtotal} + 稅金:{tax} = 總計:{total})"

@pytest.mark.negative
def test_checkout_required_fields_validation(logged_in_page, cart_page, checkout_page, test_info):
    """驗證未填寫姓名時應出現提示訊息"""
    test_info["data"] = "未填寫任何資訊點擊繼續"
    test_info["expected"] = "顯示 Error: First Name is required"
    
    logged_in_page.add_to_cart(Products.BACKPACK.name)
    logged_in_page.go_to_cart()
    cart_page.checkout()
    checkout_page._continue_button.click()
    
    error_msg = checkout_page.page.locator("[data-test='error']").inner_text()
    assert "First Name is required" in error_msg
    test_info["actual"] = f"系統正確攔截並顯示: {error_msg}"

@pytest.mark.negative
def test_error_user_checkout_flow(login_page, inventory_page, cart_page, checkout_page, test_info):
    """驗證 error_user 在結帳流程最後一步應無法正常完成"""
    from fixtures.users import Users
    test_info["data"] = f"帳號: {Users.ERROR_USER.username}"
    test_info["expected"] = "點擊 Finish 後應能成功進入完成頁面 (checkout-complete.html)"
    
    login_page.load()
    login_page.login(Users.ERROR_USER.username, Users.ERROR_USER.password)
    
    inventory_page.add_to_cart(Products.BACKPACK.name)
    inventory_page.go_to_cart()
    cart_page.checkout()
    checkout_page.fill_information("Test", "User", "123")
    
    # 到達 Step 2
    assert "checkout-step-two.html" in checkout_page.page.url
    
    # 嘗試完成結帳
    checkout_page.finish_checkout()
    
    # 驗證是否成功進入完成頁面
    current_url = checkout_page.page.url
    assert "checkout-complete.html" in current_url, f"結帳失敗，停留在: {current_url}"
    test_info["actual"] = "成功完成結帳流程"
