import pytest
import time
from fixtures.users import Users
from fixtures.products import Products

@pytest.mark.account
def get_inventory_data(inventory_page):
    """取得當前頁面所有商品的詳細資料"""
    inventory_page.page.wait_for_selector(".inventory_item", state="visible")
    items = inventory_page.page.locator(".inventory_item").all()
    data = []
    for item in items:
        name = item.locator(".inventory_item_name").inner_text()
        desc = item.locator(".inventory_item_desc").inner_text()
        price = item.locator(".inventory_item_price").inner_text()
        img = item.locator(".inventory_item_img img").get_attribute("src")
        data.append({"name": name, "desc": desc, "price": price, "img": img})
    return data

@pytest.mark.account
def test_problem_user_data_consistency(login_page, inventory_page, header, test_info):
    """以 fixtures/products.py 中定義的真實資料為基準 (Golden Sample)，驗證 problem_user 的商品資料是否錯誤"""
    
    # 1. 取得 Golden Sample (來自 fixtures)
    golden_data = [
        Products.BACKPACK, Products.BIKE_LIGHT, Products.BOLT_TSHIRT,
        Products.FLEECE_JACKET, Products.ONESIE, Products.TEST_ALL_THE_THINGS_TSHIRT
    ]
    
    # 動態產生預期結果字串，將 Golden Sample 列出
    expected_str = "商品資料必須與基準資料 (Fixtures) 完全一致。基準資料如下：<br>"
    for i, item in enumerate(golden_data):
        desc_short = item.description[:40] + "..." if len(item.description) > 40 else item.description
        img_name = item.image_url.split('/')[-1]
        expected_str += f"<div style='margin-left: 15px; margin-bottom: 5px; font-size: 0.9em; display: flex; align-items: center;'>"
        expected_str += f"<img src='{item.image_url}' style='width: 40px; height: 50px; margin-right: 10px; border: 1px solid #ccc;' />"
        expected_str += f"<div><b>{i+1}. {item.name}</b> ({item.price})<br>"
        expected_str += f"說明: {desc_short}<br>"
        expected_str += f"圖片檔名: <code>{img_name}</code></div>"
        expected_str += "</div>"
    test_info["expected"] = expected_str
    
    # 2. 用 problem_user 進行比對
    login_page.load()
    login_page.login(Users.PROBLEM_USER.username, Users.PROBLEM_USER.password)
    inventory_page.page.wait_for_selector(".inventory_item", state="visible")
    problem_data = get_inventory_data(inventory_page)
    
    # 3. 比對差異
    diffs = []
    for i in range(len(golden_data)):
        std = golden_data[i]
        prob = problem_data[i]
        item_diffs = []
        if std.name != prob["name"]: item_diffs.append(f"名稱({prob['name']})")
        if std.description != prob["desc"]: item_diffs.append("說明文字")
        if std.price != prob["price"]: item_diffs.append(f"售價({prob['price']})")
        # 由於 get_attribute("src") 可能拿到相對路徑，這裡做彈性比對
        if std.image_url.split('/')[-1] not in prob["img"]: item_diffs.append("圖片路徑")
        
        if item_diffs:
            diffs.append(f"商品 {i+1} 異常項目: {', '.join(item_diffs)}")
    
    test_info["data"] = f"比對項目數: {len(golden_data)}"
    
    # 動態產生實際結果字串，將 problem_user 的資料列出
    actual_str = "實際抓取到的 problem_user 資料如下：<br>"
    for i, item in enumerate(problem_data):
        desc_short = item['desc'][:40] + "..." if len(item['desc']) > 40 else item['desc']
        img_name = item['img'].split('/')[-1]
        img_url = f"https://www.saucedemo.com{item['img']}" if item['img'].startswith("/") else item['img']
        actual_str += f"<div style='margin-left: 15px; margin-bottom: 5px; font-size: 0.9em; display: flex; align-items: center;'>"
        actual_str += f"<img src='{img_url}' style='width: 40px; height: 50px; margin-right: 10px; border: 1px solid #ccc;' />"
        actual_str += f"<div><b>{i+1}. {item['name']}</b> ({item['price']})<br>"
        actual_str += f"說明: {desc_short}<br>"
        actual_str += f"圖片檔名: <code>{img_name}</code></div>"
        actual_str += "</div>"
    
    if diffs:
        actual_str += "<br><b style='color:red;'>偵測到資料不一致項目：</b><br>" + "<br>".join(diffs)
        test_info["actual"] = actual_str
        assert len(diffs) == 0, f"商品資料與 standard_user 不一致，發現 {len(diffs)} 項差異"
    else:
        test_info["actual"] = actual_str + "<br><b style='color:green;'>資料完全一致</b>"

@pytest.mark.account
def test_problem_user_about_page_redirection(login_page, inventory_page, header, test_info):
    """驗證 problem_user 點擊側邊欄 About 後是否導向錯誤頁面 (404)"""
    test_info["data"] = f"帳號: {Users.PROBLEM_USER.username}"
    test_info["expected"] = "點擊 About 後不應導向 404 錯誤頁面"
    
    login_page.load()
    login_page.login(Users.PROBLEM_USER.username, Users.PROBLEM_USER.password)
    
    header.go_to_about()
    
    # 驗證是否導向 404 頁面 (根據 verify 腳本結果)
    current_url = inventory_page.page.url
    assert "404" not in current_url, f"頁面導航失敗，跳轉至錯誤頁面: {current_url}"
    test_info["actual"] = "成功跳轉至正確的 About 頁面"

@pytest.mark.account
def test_performance_glitch_user_inventory_loading(login_page, inventory_page, test_info):
    """驗證 performance_glitch_user 登入後進入 inventory.html 時是否存在明顯的效能異常 (約5秒)"""
    test_info["data"] = f"帳號: {Users.PERFORMANCE_GLITCH_USER.username}"
    test_info["expected"] = "進入 inventory.html 的載入過程應在 3 秒內完成"
    
    login_page.load()
    
    start_time = time.time()
    login_page.login(Users.PERFORMANCE_GLITCH_USER.username, Users.PERFORMANCE_GLITCH_USER.password)
    
    assert inventory_page.is_visible(".inventory_list")
    duration = time.time() - start_time
    assert duration < 3, f"載入時間過長，實際耗時: {duration:.2f} 秒"
    test_info["actual"] = f"載入順暢，實際耗時: {duration:.2f} 秒"

@pytest.mark.visual
def test_visual_user_layout_validation(login_page, inventory_page, test_info):
    """驗證 visual_user 登入後的頁面佈局是否存在異常偏移"""
    test_info["data"] = f"帳號: {Users.VISUAL_USER.username}"
    test_info["expected"] = f"首張商品圖片必須正常顯示 (預期為 {Products.BACKPACK.name} 的圖片)"
    
    login_page.load()
    login_page.login(Users.VISUAL_USER.username, Users.VISUAL_USER.password)
    
    # 驗證第一張圖片是否正常
    img_src = inventory_page.page.locator(".inventory_item_img img").first.get_attribute("src")
    expected_img_filename = Products.BACKPACK.image_url.split('/')[-1]
    assert expected_img_filename in img_src, f"首張圖片顯示異常: {img_src} (應包含 {expected_img_filename})"
    
    test_info["actual"] = "首張圖片正確載入 (符合 Fixtures 定義)"
