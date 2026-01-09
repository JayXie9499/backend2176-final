# Final — 網頁程式設計期末報告專題

## 目錄概覽

```
backend2176-final/
├─ backend/           # 後端程式
├─ frontend/          # 前端程式
├─ .env.example
├─ docker-compose.yml
├─ DEVELOPMENT.md
└─ README.md
```

## 架構與技術棧說明

### 整體架構

本專案採用**前後端分離**架構，並以 **Docker / Docker Compose** 作為主要開發與部署方式。

* **Frontend（Svelte）**

  * 負責使用者介面與前端互動邏輯。
  * 透過設定的 API URL 與後端 FastAPI 進行 HTTP 通訊。

* **Backend（FastAPI）**

  * 提供 RESTful API。
  * 處理身分驗證（JWT）、業務邏輯與資料存取。

* **Container / Network**

  * 使用 `docker-compose.yml` 管理前後端服務。
  * 透過環境變數控制前後端連線位址、CORS 與安全設定。

### 使用技術

* 前端：Svelte
* 後端：FastAPI
* API 通訊：HTTP / JSON
* 驗證機制：JWT
* 部署與開發：Docker / Docker Compose

## 快速啟動

### 使用 Docker（推薦）

```bash
# 在專案根目錄
docker compose up --build -d
```

### 手動部屬 — 後端

```bash
# 在專案 backend 目錄
uv sync
uv run -m app.main
# 或：
pip install .
python -m app.main
```

### 手動部屬 — 前端

```bash
# 在專案 frontend 目錄
pnpm install
pnpm build
node build/index.js
# 或：
npm install
npm build
node build/index.js
```

## 環境變數說明（`.env.example`）

以下環境變數由 `docker compose` 讀取並注入各服務容器：

### 前端相關

* `PUBLIC_API_URL`
  前端對外呼叫後端 API 的完整 URL。

* `FRONTEND_HOST_PORT`
  前端在主機上對外開放的連接埠。

* `FRONTEND_INTERNAL_PORT`
  前端容器內部監聽的連接埠。

* `ORIGIN` (可選)
  前端實際存取來源，供 CORS 與安全設定使用。

### 後端相關

* `BACKEND_PORT`
  FastAPI 對外監聽的連接埠。

* `JWT_SECRET`
  用於簽署與驗證 JWT 的密鑰。

* `ALLOWED_ORIGINS`
  允許存取後端 API 的來源清單（CORS 設定）。
