import pytest
from fixtures.users import Users

@pytest.mark.smoke
@pytest.mark.parametrize("user", Users.ALL_USERS, ids=[u.username for u in Users.ALL_USERS])
def test_account_login_validation(login_page, inventory_page, user, test_info):
    """驗證不同權限與特性的帳號是否能按照預期行為登入系統"""
    test_info["data"] = f"帳號: {user.username}, 密碼: {user.password}"
    test_info["expected"] = "鎖定帳號應顯示錯誤訊息，其餘帳號應成功跳轉至商品頁"
    
    login_page.load()
    login_page.login(user.username, user.password)
    
    if user == Users.LOCKED_OUT_USER:
        error = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error
        test_info["actual"] = f"系統正確攔截鎖定帳號並顯示: {error}"
    else:
        assert "inventory.html" in login_page.page.url
        test_info["actual"] = "登入成功，已跳轉至 inventory.html"

@pytest.mark.negative
def test_invalid_credentials_login_failure(login_page, test_info):
    """驗證系統是否能正確阻擋錯誤的登入資訊"""
    test_info["data"] = "帳號: wrong_user, 密碼: wrong_pass"
    test_info["expected"] = "顯示 Username and password do not match 錯誤訊息"
    
    login_page.load()
    login_page.login("wrong_user", "wrong_pass")
    error = login_page.get_error_message()
    assert "Username and password do not match" in error
    test_info["actual"] = f"驗證成功，系統顯示錯誤: {error}"

@pytest.mark.regression
def test_user_logout_functionality(login_page, inventory_page, header, test_info):
    """驗證使用者在登入後可以安全登出系統"""
    test_info["data"] = f"帳號: {Users.STANDARD_USER.username}"
    test_info["expected"] = "登出後頁面應重導向至首頁 (/) 且無法再看到商品列表"
    
    login_page.load()
    login_page.login(Users.STANDARD_USER.username, Users.STANDARD_USER.password)
    header.logout()
    
    assert login_page.page.url == "https://www.saucedemo.com/"
    test_info["actual"] = "成功登出並返回登入頁面"
