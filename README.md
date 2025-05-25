# PDFtoPPT

## 安裝專題依賴
```bash
pip install -r requirements.txt
```

## 直接開始
1. 設定 API key: 在 `Gemini/.env` 中 (將.env.example 檔名尾部拿掉即可)
2. 執行以下指令
```bash
fastapi run app.py
```
3. 使用瀏覽器開啟前端網站，**開始體驗！**
### 簡報主題上傳區使用方式：
開啟PowerPoint選定主題（選擇4:3大小，目前主要以此設計效果較佳）
儲存pptx檔案，然後直接上傳
若未上傳會使用預設版本

## front-end
dummy logic 在 utils.py
```bash
fastapi run app.py
```

## 論文pdf圖片擷取
FetchImage/extracted_yolo 中有 api 使用
產出結果圖片在 **Crop_imgs** 中
並產出 **output_metadata.json** 提供後續做進一步分析與 mapping

單獨測試
```bash
cd FetchImage
python3 extracted_yolo.py
```


## Gemini使用方式

1. 先去[Google AI Studio](https://aistudio.google.com/u/3/prompts/new_chat)申請API key，可[參考](https://ai.google.dev/gemini-api/docs?hl=zh-tw)
2. 在Gemini資料夾內創建.env檔案，檔案內寫入你的api key，不用加引號
```bash
GEMINI_API_KEY=key
```
3. prompt.txt可以改prompt