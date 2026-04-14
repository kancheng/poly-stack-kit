# PolyStack 3x3 整合驗證說明

## 目的

本文件說明本專案如何透過 `scripts/test-matrix.py` 驗證「前端 API 需求」與「多後端實作」的一致性，作為跨技術棧整合的基準檢查（smoke test）。

驗證目標如下：

1. 三個前端模板（Vue / React / Angular）依賴的認證 API 契約一致。  
2. 三個後端模板（Django / Laravel / Flask）均可提供相同語意與回應格式。  
3. JWT 基本流程（登入、簽發 token、驗證 token）可在所有後端正常運作。  

## 驗證範圍

`test-matrix.py` 聚焦於以下兩個端點：

- `POST /api/auth/login`
- `GET /api/auth/me`（需 Bearer token）

選擇此組合的原因：

- `login` 可驗證帳號密碼校驗、token 簽發與回應 envelope。  
- `auth/me` 可驗證授權中介層、token 解析與目前登入使用者資訊。  

## 實作方式

### 1) 測試矩陣

腳本內建 3 個前端標籤與 3 個後端 URL，組成 3x3 測試矩陣：

- 前端：`vue`, `react`, `angular`
- 後端：  
  - `django -> http://127.0.0.1:8000`  
  - `laravel -> http://127.0.0.1:8100`  
  - `flask -> http://127.0.0.1:8200`

> 註：前端標籤主要用於矩陣報表呈現，HTTP 呼叫直接送往指定後端 URL；此腳本用來驗證契約相容性，而非瀏覽器 UI 行為。

### 2) 請求與錯誤處理

`request_json()` 封裝了通用 HTTP 行為：

- 預設 `Content-Type: application/json`
- 將 payload 序列化為 JSON
- 解析成功回應 JSON
- 在 `HTTPError` 與 `URLError` 時回傳結構化錯誤訊息，方便定位問題

### 3) 核心檢查流程

`login_and_me()` 依序執行：

1. 呼叫 `POST /api/auth/login` 並檢查 `status == 200` 與 `success == true`。  
2. 讀取 `data.tokens.access_token`，若不存在即判定失敗。  
3. 使用 `Authorization: Bearer <token>` 呼叫 `GET /api/auth/me`。  
4. 檢查 `status == 200`、`success == true`，且 `data.email` 存在。  

任一步驟失敗都會回傳明確原因（例如：連線錯誤、401、token 缺失、回應格式不符）。

### 4) 結果輸出

每組測試都會輸出：

- `PASS/FAIL`
- 前端標籤
- 後端名稱
- 後端 URL
- 詳細結果

最後彙總 `Result: x/9 passed`，並透過程式 exit code 回報整體狀態：

- 全部通過：`0`
- 任一失敗：`1`

## 使用方式

啟動三套後端後執行：

```bash
python scripts/test-matrix.py
```

必要時可覆蓋後端位址：

```bash
python scripts/test-matrix.py --backend django=http://127.0.0.1:8000 --backend laravel=http://127.0.0.1:8100 --backend flask=http://127.0.0.1:8200
```

也可指定測試帳號：

```bash
python scripts/test-matrix.py --email demo@polystack.local --password password
```

## 結果解讀

### 本測試可直接確認

- 多後端是否符合共同認證 API 契約
- JWT 登入與授權鏈路是否可用
- 後端是否具備被三個前端模板共用的基本條件

### 本測試不涵蓋

- 瀏覽器層 CORS 與前端路由守衛細節
- UI 互動與錯誤訊息呈現品質
- 非 auth 業務流程（例如 tasks CRUD）完整性

建議將本腳本作為「第一層整合檢查」，再搭配 E2E 測試與更完整的 API 測試覆蓋。

