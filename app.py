import os
import shutil
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import FastAPI, File, UploadFile, HTTPException

from .utils import paper_to_slide


# App setup
app = FastAPI()

# CORS setup
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for temporary files
TEMP_DIR = "tmp"
os.makedirs(TEMP_DIR, exist_ok=True)


# Routes
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    html_file_path = "index.html"
    if os.path.exists(html_file_path):
        return FileResponse(html_file_path, media_type="text/html")

    else:
        # Fallback
        return HTMLResponse(
            content="<h1>[Error] index.html not found</h1>",
            status_code=404,
        )


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are accepted."
        )

    pdf_path = os.path.join(TEMP_DIR, file.filename)
    base, ext = os.path.splitext(file.filename)
    pptx_path = os.path.join(TEMP_DIR, f"{base}.pptx")

    try:
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ------ ACTUAL LOGIC GOES HERE... ------
        paper_to_slide(pdf_path, pptx_path)

        if not os.path.exists(pptx_path):
            print(f"PPTX file was not found after attempted creation: {pptx_path}")
            raise HTTPException(
                status_code=500, detail="PPTX conversion failed or file not found."
            )

        return FileResponse(
            path=pptx_path,
            filename=os.path.basename(pptx_path),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    except Exception as e:
        print(f"Error during file processing: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Clean up the temporary files
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)

            except Exception as e_remove_pdf:
                print(f"Error removing temporary PDF {pdf_path}: {e_remove_pdf}")
