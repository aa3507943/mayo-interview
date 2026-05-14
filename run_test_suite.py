import pytest
import os
import sys

# 將專案路徑加入系統搜尋路徑
PROJECT_ROOT = os.path.join(os.getcwd(), "saucedemo-playwright-python")
sys.path.append(PROJECT_ROOT)
os.environ["PYTHONPATH"] = PROJECT_ROOT

def run_all_tests():
    """跑全部測試"""
    print("\n🚀 正在執行：全部測試...")
    pytest.main([PROJECT_ROOT])

def run_smoke_only():
    """只跑冒煙測試 (最核心功能)"""
    print("\n🚀 正在執行：冒煙測試 (Smoke)...")
    pytest.main(["-m", "smoke", PROJECT_ROOT])

def run_login_category():
    """執行所有登入相關測試"""
    print("\n🚀 正在執行：登入模組測試...")
    pytest.main([os.path.join(PROJECT_ROOT, "tests/test_login.py")])

def run_inventory_and_cart():
    """執行商品與購物車測試"""
    print("\n🚀 正在執行：商品與購物車測試...")
    pytest.main([
        os.path.join(PROJECT_ROOT, "tests/test_inventory.py"),
        os.path.join(PROJECT_ROOT, "tests/test_cart.py")
    ])

def run_checkout_e2e():
    """執行完整結帳流程測試"""
    print("\n🚀 正在執行：結帳流程 E2E 測試...")
    pytest.main([os.path.join(PROJECT_ROOT, "tests/test_checkout.py")])

def run_special_accounts():
    """執行特殊帳號特性測試"""
    print("\n🚀 正在執行：特殊帳號 (Problem/Performance/Visual) 測試...")
    pytest.main([os.path.join(PROJECT_ROOT, "tests/test_accounts.py")])

if __name__ == "__main__":
    # --- 你可以在下方透過「註解」或「取消註解」來控制要執行的項目 ---
    
    run_all_tests()             # 全部跑
    # run_smoke_only()            # 只跑核心功能
    # run_login_category()        # 只跑登入
    # run_inventory_and_cart()    # 只跑購物車相關
    # run_checkout_e2e()          # 只跑結帳
    # run_special_accounts()      # 只跑特殊帳號
    
    print(f"\n✅ 測試執行完畢！報告將存放在專案內的 reports 資料夾中。")
