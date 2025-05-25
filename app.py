import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

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
        return HTMLResponse(
            content="<h1>[Error] index.html not found</h1>", status_code=404
        )


@app.post("/uploadfile/")
async def create_upload_file(
    pdf_file: UploadFile = File(..., description="The PDF paper to process."),
    pptx_file: UploadFile = File(..., description="The PPTX theme template."),
):
    # Validate PDF
    if not pdf_file.filename or not pdf_file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type for paper. Only PDF files are accepted.",
        )

    # Validate PPTX
    if not pptx_file.filename or not pptx_file.filename.lower().endswith(".pptx"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type for theme. Only PPTX files are accepted.",
        )

    pdf_path = os.path.join(TEMP_DIR, f"paper_{pdf_file.filename}")
    theme_pptx_path = os.path.join(TEMP_DIR, f"theme_{pptx_file.filename}")

    base_pdf, _ = os.path.splitext(pdf_file.filename)
    output_pptx_path = os.path.join(TEMP_DIR, f"{base_pdf}_slides.pptx")

    try:
        # Save PDF
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)

        # Save PPTX Theme
        with open(theme_pptx_path, "wb") as buffer:
            shutil.copyfileobj(pptx_file.file, buffer)

        # --- ACTUAL LOGIC ---
        paper_to_slide(pdf_path, output_pptx_path, theme_pptx_path)

        if not os.path.exists(output_pptx_path):
            raise HTTPException(
                status_code=500, detail="PPTX conversion failed or file not found."
            )

        return FileResponse(
            path=output_pptx_path,
            filename=os.path.basename(output_pptx_path),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        for path in [pdf_path, theme_pptx_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)

                except Exception as e_remove:
                    print(f"Error removing temporary file {path}: {e_remove}")
