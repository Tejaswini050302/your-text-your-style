import os
import io
import tempfile
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.pptx_generator import generate_presentation

app = FastAPI()

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request,
    text: str = Form(...),
    guidance: str = Form(""),
    api_key: str = Form(""),
    template_file: UploadFile = None
):
    # Save template to temp file
    template_path = None
    if template_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
            template_path = tmp.name
            tmp.write(await template_file.read())

    # Generate PPTX
    output_pptx = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
    generate_presentation(text, guidance, template_path, output_pptx.name)

    return FileResponse(output_pptx.name, filename="generated.pptx")
