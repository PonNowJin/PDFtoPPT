# PDFtoPPT — AI-powered Academic Presentation Generator

🌐 Language: [繁體中文](./README.zh-TW.md) | [Deutsch](./README.de.md)

Automatically convert academic PDF papers into well-structured PowerPoint slides with extracted images, summarized content, and clean layout.

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API key

* Create a `.env` file in the `Gemini/` folder (or rename `.env.example` to `.env`)
* Add the following line (no quotes needed):

```bash
GEMINI_API_KEY=your_api_key_here
```

### 3. Start the backend server

```bash
fastapi run app.py
```

### 4. Open the frontend in your browser and start converting!

---

## Custom Slide Template (Optional)

You can upload your own PowerPoint template (`.pptx`) for slide styling:

* **Recommended:** Use 4:3 slide ratio for optimal layout
* Save your custom theme in PowerPoint and upload it via the frontend
* If not uploaded, a default built-in template will be used

---

## Image Extraction from PDFs (YOLO Model)

The system uses a YOLO model to detect and extract figures, diagrams, and tables from PDF files:

* Script: `FetchImage/extracted_yolo.py`
* Output:

  * `Crop_imgs/`: Contains cropped figure images
  * `output_metadata.json`: Stores location and page index info for each image

### To run manually:

```bash
cd FetchImage
python3 extracted_yolo.py
```

---

## Gemini Integration

Google Gemini API is integrated to summarize paragraph-level content and structure slides accordingly.

### Configuration:

1. Get your API Key from [Google AI Studio](https://aistudio.google.com/u/3/prompts/new_chat)
2. Save the key in `Gemini/.env`
3. Modify `Gemini/prompt.txt` to customize generation prompts

---

## Project Structure

| Folder / File          | Description                        |
| ---------------------- | ---------------------------------- |
| `app.py`               | Main FastAPI backend entry point   |
| `Gemini/`              | Gemini API integration and prompts |
| `FetchImage/`          | YOLO image detection & cropping    |
| `pptx_api/`            | Logic for generating .pptx slides  |
| `Crop_imgs/`           | Stores cropped figure images       |
| `output_metadata.json` | Metadata for image-page mapping    |

---

## Best Use Cases

* Academic presentation prep (e.g., thesis defense)
* Journal paper slide generation
* Researchers needing fast visual summaries from PDFs

---

## Feedback & Collaboration

We welcome any suggestions or collaboration proposals. Please reach out to the development team for more information.
