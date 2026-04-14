# PolyStack RESTful API 與框架實作指南

## 文件目的

本文件說明 PolyStack Kit 的 RESTful API 設計細節、各框架實作特性，以及日常需求變更時的修改方法與原理。  
本專案以 `api-spec/openapi.yaml` 為單一契約來源（single source of truth），由 Django / Laravel / Flask 三套後端共同實作，並由 Vue / React / Angular 三套前端共同消費。

## 一、RESTful API 設計細節

### 1) 共同契約

- **基底路徑**：`/api`
- **格式**：JSON + UTF-8
- **認證**：`Authorization: Bearer <JWT>`
- **回應封裝**：統一使用 envelope（`success/message/data/error`）

成功回應範例（HTTP 2xx）：

```json
{
  "success": true,
  "message": "OK",
  "data": {},
  "error": null
}
```

錯誤回應範例（HTTP 4xx/5xx）：

```json
{
  "success": false,
  "message": "Validation error",
  "data": null,
  "error": {
    "code": 400,
    "details": "Field email is required"
  }
}
```

### 2) 資源與端點

#### Auth

- `POST /api/auth/register`：註冊，回傳 user + token
- `POST /api/auth/login`：登入，回傳 user + token
- `GET /api/auth/me`：取得當前登入者（需 JWT）

#### Tasks

- `GET /api/tasks`：列表（支援 `page`, `per_page`）
- `POST /api/tasks`：建立
- `GET /api/tasks/{id}`：單筆
- `PUT /api/tasks/{id}`：更新
- `DELETE /api/tasks/{id}`：刪除

#### Executions

- `GET /api/executions`：列表（可依 `task_id` 篩選）
- `POST /api/executions`：建立執行紀錄

#### Ratings

- `GET /api/ratings`：列表（可依 `execution_id` 篩選）
- `POST /api/ratings`：建立評分（1~5）

### 3) RESTful 原理在本專案中的落地

- **資源導向命名**：以 `tasks`, `executions`, `ratings` 作為名詞集合。
- **HTTP 動詞語意**：`GET/POST/PUT/DELETE` 對應查詢/建立/更新/刪除。
- **狀態碼語意**：`200/201/401/404/422` 等與業務狀態對齊。
- **無狀態認證**：JWT 攜帶於 header，伺服器不依賴 session 狀態。
- **一致性高於框架差異**：不同語言框架共享同一契約，確保前端可替換後端。

## 二、後端框架特性與實作位置

### 1) Django（DRF + SimpleJWT）

**特性**

- 類別型視圖（`APIView`）結構清晰，適合分層擴充。
- Serializer 驗證整合度高，欄位錯誤訊息一致性佳。
- `IsAuthenticated` 權限機制明確，JWT 與 DRF 整合成熟。

**關鍵檔案**

- 路由：`backend/django/hub/urls.py`
- 控制器：`backend/django/hub/views.py`
- 序列化與驗證：`backend/django/hub/serializers.py`
- 統一回應：`backend/django/hub/response.py`

### 2) Laravel（Controller + Service）

**特性**

- 路由與中介層宣告直觀（`routes/api.php`）。
- Controller 處理輸入驗證，Service 封裝業務邏輯，職責分離清楚。
- 透過 `auth:api` middleware 保護路由，JWT 套件整合可維持一致行為。

**關鍵檔案**

- 路由：`backend/laravel/routes/api.php`
- 控制器：`backend/laravel/app/Http/Controllers/Api/*.php`
- 業務層：`backend/laravel/app/Services/*.php`
- 統一回應：`backend/laravel/app/Http/Support/ApiResponse.php`

### 3) Flask（Blueprint + Service）

**特性**

- Blueprint 模組化路由，易於按資源拆分。
- 函式型 endpoint 輕量、可快速迭代。
- `flask-jwt-extended`、`marshmallow`、service 模式組合，兼顧開發速度與結構化。

**關鍵檔案**

- App 組裝：`backend/flask/app/__init__.py`
- API 路由：`backend/flask/app/api/*.py`
- 業務層：`backend/flask/app/services/*.py`
- Schema 驗證：`backend/flask/app/schemas.py`
- 統一回應：`backend/flask/app/utils/response.py`

## 三、前端框架特性（API 消費層）

### 1) Vue

- API 封裝：`frontend/vue-template/src/api.js`
- 特色：Axios instance + request interceptor，自動帶入 `polystack_token`。

### 2) React

- API 封裝：`frontend/react-template/src/api.js`
- 特色：與 Vue 相同的 Axios + envelope `unwrap`，降低跨前端差異。

### 3) Angular

- API 封裝：`frontend/angular-template/src/app/services/api.service.ts`
- 特色：`HttpClient` + RxJS `map` 進行 envelope unwrap；搭配 interceptor 注入 token。

> 三個前端皆以 `VITE_API_BASE_URL` 或 `environment.apiBase` 指向後端，並固定拼接 `/api` 前綴，確保同契約下可直接切換後端。

## 四、如何修改（實務流程）

### 變更情境 A：新增 API 欄位（例如 Task 增加 `category`）

1. 更新契約：修改 `api-spec/openapi.yaml` schema 與相關 request/response。  
2. 更新資料模型：調整資料表（migration / schema）與 model。  
3. 更新驗證：Django serializer、Laravel validator、Flask schema 同步調整。  
4. 更新輸出：確保三套後端回傳 envelope 中 `data` 結構一致。  
5. 更新前端：三個前端表單與顯示欄位同步。  
6. 驗證：先跑 `scripts/test-matrix.py` 驗證 auth 鏈路，再補 endpoint 測試。

### 變更情境 B：新增資源（例如 `/api/tags`）

1. 契約先行：在 OpenAPI 加上 `Tag`, `TagInput`, 路徑與狀態碼。  
2. 三後端對齊新增：
   - Django：`urls.py` + `views.py` + serializer/model
   - Laravel：`routes/api.php` + Controller + Service + Model
   - Flask：Blueprint 路由 + schema + service + model
3. 三前端新增 API 呼叫與頁面/元件串接。  
4. 加入測試腳本或最小 smoke test，避免只在單框架成功。

### 變更情境 C：調整錯誤格式或狀態碼

1. 先更新 `common/response-format.md` 與 OpenAPI。  
2. 三後端的統一回應 helper 同步調整（`ok/fail` 或 `ApiResponse`）。  
3. 前端 `unwrap` / error handler 一次性對齊新規則。  
4. 驗證各端點錯誤分支（401/404/422）是否仍符合預期。

## 五、設計原理與維護準則

### 1) 契約優先（Contract-First）

先定義 OpenAPI，再實作三套後端與三套前端，可避免框架各自發散。

### 2) 跨框架一致性

所有變更都以「三後端行為一致、三前端可無痛切換」為驗收標準，不以單一框架可用作為完成條件。

### 3) 單一責任與分層

- 路由層：只負責 URL 與 middleware 入口
- 驗證層：只負責輸入合法性
- 服務層：承接業務規則
- 回應層：統一 envelope，隔離框架差異

### 4) 驗證策略

- **快速整合檢查**：`scripts/test-matrix.py`（登入 + `auth/me`）
- **功能驗證**：各資源端點測試（單元/整合）
- **前端驗證**：至少一套 E2E（建議 Playwright）覆蓋關鍵流程

## 六、常見修改入口索引

- API 契約：`api-spec/openapi.yaml`
- API 設計說明：`api-spec/api-design.md`
- 回應格式規範：`common/response-format.md`
- JWT 認證設計：`common/auth-design.md`
- 矩陣 smoke test：`scripts/test-matrix.py`
- 整合驗證文件：`docs/integration-matrix-validation.md`

