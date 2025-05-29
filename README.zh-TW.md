# PDFtoPPT — AI 輔助的學術簡報產生器

🌐 語言選擇：[English](./README.md) | [Deutsch](./README.de.md)

自動將學術 PDF 論文轉換為結構清晰的 PowerPoint 投影片，包含圖像擷取、段落摘要與簡潔排版。

---

## 🚀 快速開始

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定 Gemini API 金鑰

* 在 `Gemini/` 資料夾中建立 `.env` 檔案（或將 `.env.example` 改名為 `.env`）
* 加入以下內容（不需加上引號）：

```bash
GEMINI_API_KEY=your_api_key_here
```

### 3. 啟動後端伺服器

```bash
fastapi run app.py
```

### 4. 使用瀏覽器開啟前端網站，即可開始轉換！

---

## 自訂簡報樣式（選用）

你可以上傳自訂的 PowerPoint 主題模板（`.pptx` 檔案）來套用投影片風格：

* **建議比例：** 使用 4:3 投影片比例以獲得最佳排版效果
* 在 PowerPoint 儲存你的主題樣式並透過前端介面上傳
* 若未上傳，系統會使用內建預設樣板

---

## PDF 圖像擷取（YOLO 模型）

本系統利用 YOLO 模型從 PDF 中擷取圖表、示意圖及表格：

* 程式腳本：`FetchImage/extracted_yolo.py`
* 輸出內容：

  * `Crop_imgs/`：擷取後的圖像儲存位置
  * `output_metadata.json`：紀錄圖像頁數與位置等中繼資料

### 手動執行方式：

```bash
cd FetchImage
python3 extracted_yolo.py
```

---

## Gemini 整合

本系統整合 Google Gemini API，自動將段落內容摘要並產生簡報文字。

### 設定方式：

1. 前往 [Google AI Studio](https://aistudio.google.com/u/3/prompts/new_chat) 申請 API 金鑰
2. 將金鑰儲存於 `Gemini/.env`
3. 如需修改生成風格，可調整 `Gemini/prompt.txt`

---

## 專案結構說明

| 資料夾 / 檔案               | 說明                          |
| ---------------------- | --------------------------- |
| `app.py`               | FastAPI 後端主程式               |
| `Gemini/`              | 與 Gemini API 的整合與 prompt 設定 |
| `FetchImage/`          | 圖像偵測與裁切邏輯（使用 YOLO）          |
| `pptx_api/`            | PowerPoint 投影片生成邏輯          |
| `Crop_imgs/`           | 儲存裁切後的圖像                    |
| `output_metadata.json` | 儲存圖像位置與頁面資訊的中繼資料            |

---

## 適用場景

* 學術簡報準備（如論文口試）
* 學術期刊投影片自動生成
* 研究人員快速整理 PDF 重點內容

---

## 意見回饋與合作邀請

歡迎提供任何建議或合作提案，請聯繫開發團隊以了解更多資訊。
