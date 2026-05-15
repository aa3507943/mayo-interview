# SauceDemo (Swag Labs) 測試歸納

**網站網址**：https://www.saucedemo.com/  
**所有帳號密碼**：`secret_sauce`

**測試帳號列表**：
- standard_user
- locked_out_user
- problem_user
- performance_glitch_user
- error_user
- visual_user

---

## 1. 主要頁面流程

- Login Page (`/`)
- Inventory Page (`/inventory.html`)
- Product Detail
- Cart Page (`/cart.html`)
- Checkout Step 1 (Your Information)
- Checkout Step 2 (Overview)
- Checkout Complete
- Logout / Error States

---

## 2. 測試帳號特性與差異

| 帳號                    | 能否登入 | 主要特性                     | 測試重點類型                  |
|-------------------------|----------|------------------------------|-------------------------------|
| standard_user          | 是      | 完全正常                     | Happy Path、基準測試         |
| locked_out_user        | 否      | 帳號鎖定                     | 負向測試、錯誤訊息驗證       |
| problem_user           | 是      | 圖片損壞、About 頁跳轉異常    | UI 缺陷、導覽路徑驗證         |
| performance_glitch_user| 是      | 進入 inventory.html 時明顯延遲 | 效能測試、Timeout 處理        |
| error_user             | 是      | 結帳流程異常 (無法 Finish)    | 錯誤處理、流程邊界測試       |
| visual_user            | 是      | 首張圖片非預期 (sl-404)       | 視覺回歸測試、圖片屬性驗證   |

---

## 3. 依帳號組合測試案例

### 3.1 standard_user（基準帳號）
- 正常登入 → 商品列表驗證 → 排序 (4 種) → Add to Cart (單筆/多筆) → Cart 頁面操作 → 完整結帳流程
- Remove 商品 (列表頁 & Cart 頁)
- Checkout 必填欄位驗證 + 金額計算
- Logout 流程
- Responsive 測試 (Desktop / Mobile)

### 3.2 locked_out_user（鎖定帳號）
- 登入失敗 → 驗證錯誤訊息「Epic sadface: Sorry, this user has been locked out.」
- 錯誤後仍可嘗試其他帳號登入
- 多次錯誤登入後行為觀察

### 3.3 problem_user（問題帳號）
- 登入成功後檢查：
  - **資料一致性驗證**：以 `standard_user` 為基準 (Golden Sample)，比對所有商品的圖片、名稱、說明、售價。
  - 預期 `problem_user` 的圖片、名稱、說明、售價應存在多處異常。
  - **About 頁面導覽**：點擊側邊欄 About 應導向錯誤頁面 (404)
  - 商品細節頁與購物車頁面之資料一致性。
- 其他功能 (排序、結帳) 是否仍正常

### 3.4 performance_glitch_user（效能帳號）
- 登入後測量：
  - **Inventory Page 載入時間**：進入 `/inventory.html` 時會有明顯延遲 (約 5 秒)
  - 排序操作反應時間
  - Add to Cart 延遲
  - 結帳流程各步驟時間
- 設定 Timeout 測試是否能正確處理

### 3.5 error_user（錯誤帳號）
- 登入成功後測試：
  - Add to Cart 是否失敗或顯示錯誤
  - **結帳流程**：在 Checkout Step 2 點擊 Finish 應無法導向完成頁面
  - Remove 商品、Continue Shopping 等操作的錯誤處理
- 錯誤發生後的恢復能力

### 3.6 visual_user（視覺帳號）
- 與 standard_user 進行視覺比對：
  - **首張商品圖片**：驗證其 src 是否被錯誤替換為 sl-404 (應為 Backpack)
  - 商品列表排版、顏色、字型
  - Cart & Checkout 頁面元素位置
  - 按鈕、Badge、錯誤訊息樣式
- 使用視覺測試工具截圖比較

---

## 4. 跨帳號組合測試案例 (推薦)

### 登入相關
- 6 個帳號全部執行登入測試（含正向 + 負向）
- 登入失敗後切換其他帳號
- 空白 / 錯誤密碼 + 特殊字元輸入

### 商品與購物車
- standard_user：完整多商品加入、移除、排序
- problem_user：加入有破圖的商品到購物車
- performance_glitch_user：大量加入商品觀察延遲
- error_user：加入/移除時的錯誤處理

### 結帳流程 (Checkout)
- standard_user：完整 Happy Path 結帳 (含稅額、總額計算)
- problem_user：結帳時圖片顯示是否異常
- performance_glitch_user：結帳各步驟效能
- error_user：結帳過程中錯誤情境 (例如填入特殊字元)
- 所有帳號：必填欄位空白驗證

### 非功能測試
- **效能**：performance_glitch_user + 頁面載入 / 操作計時
- **視覺**：visual_user + standard_user 比對
- **相容性**：各帳號在 Desktop / Mobile 下的行為
- **安全性**：未登入直接訪問 `/inventory.html` 等頁面
- **重置**：使用「Reset App State」後再以不同帳號登入

### 邊界與負向案例
- 加入 6 件全部商品後結帳
- 清空購物車後結帳
- 極端輸入 (超長姓名、特殊符號)
- 登出後返回鍵行為
- 瀏覽器重新整理後狀態保持

---

## 5. 推薦測試策略

- **Smoke Test**：standard_user 完整登入 → 加 1 商品 → 結帳
- **E2E Regression**：standard_user 完整流程 + 主要負向案例
- **帳號專項測試**：problem / performance / error / visual 各自特性測試
- **資料驅動測試**：使用 6 個帳號參數化執行登入與基本流程

---

**最後更新**：2026-05-07  
**適用工具**：Selenium、Playwright、Cypress、Robot Framework、TestNG 等

---
