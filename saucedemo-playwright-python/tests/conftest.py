import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.components.header import Header
from datetime import datetime
from fixtures.users import Users
import os
import base64

# 用於儲存每個測試的詳細資訊
@pytest.fixture
def test_info():
    info = {
        "data": "N/A",
        "expected": "N/A",
        "actual": "待確認"
    }
    return info

# 獲取專案根目錄 (conftest.py 的上一層)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

def pytest_configure(config):
    # 如果使用者沒有在命令列指定 --html，我們幫他指定一個含時間戳記的預設路徑
    if not config.getoption("--html"):
        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR, exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        config.option.htmlpath = os.path.join(REPORT_DIR, f"report_{now}.html")
        config.option.self_contained_html = True

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720}
    }

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)

@pytest.fixture
def cart_page(page):
    return CartPage(page)

@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)

@pytest.fixture
def header(page):
    return Header(page)

@pytest.fixture
def logged_in_page(login_page, inventory_page):
    login_page.load()
    login_page.login(Users.STANDARD_USER.username, Users.STANDARD_USER.password)
    return inventory_page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # 獲取 test_info fixture 的資料
        info = item.funcargs.get("test_info")
        
        # 截圖處理 (不論成功失敗都截圖)
        page = item.funcargs.get("page")
        screenshot_html = ""
        if page:
            # 建立截圖子資料夾
            screenshot_dir = os.path.join(REPORT_DIR, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            # 檔名加入狀態，方便區分
            status = "PASS" if report.passed else "FAIL"
            file_name = f"{item.name}_{status}_{datetime.now().strftime('%H%M%S')}.png"
            file_path = os.path.join(screenshot_dir, file_name)
            
            # 等待 2 秒，確保畫面完全載入後再截圖 (因應登入或網頁渲染延遲)
            page.wait_for_timeout(2000)
            
            page.screenshot(path=file_path)
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            
            # 設定圖片標題顏色：成功用綠色，失敗用紅色
            border_color = "#2ecc71" if report.passed else "#e74c3c"
            label = "✅ 執行成功畫面" if report.passed else "❌ 執行失敗畫面"
            
            screenshot_html = f"""
            <div style="margin-top: 10px;">
                <b style="color: {border_color};">{label}:</b><br>
                <img src="data:image/png;base64,{encoded_string}" style="width:500px;border:2px solid {border_color};" onclick="window.open(this.src)"/>
            </div>
            """

        # 組合測試詳細資訊 HTML
        if info:
            test_details_html = f"""
            <div style="background-color: #f9f9f9; padding: 10px; border-left: 5px solid #3498db; margin-bottom: 5px;">
                <b>📋 測試說明:</b> {item.obj.__doc__ or '無'}<br>
                <b>🧪 測試資料:</b> <code style="color: #e67e22;">{info['data']}</code><br>
                <b>🎯 預期結果:</b> <span style="color: #27ae60;">{info['expected']}</span><br>
                <b>🔍 實際結果:</b> <span style="color: #2980b9;">{info['actual']}</span>
            </div>
            {screenshot_html}
            """
            extra.append(pytest_html.extras.html(test_details_html))
            
        report.extra = extra
