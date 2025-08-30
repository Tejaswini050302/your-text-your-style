from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai, os, json, tempfile
from pptx import Presentation
from typing import Optional

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_ppt(
    text: str = Form(...),
    guidance: Optional[str] = Form(None),
    provider: str = Form("openai"),
    api_key: str = Form(...),
    template: UploadFile = File(...)
):
    try:
        # Save uploaded template
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
            content = await template.read()
            tmp.write(content)
            template_path = tmp.name

        # Initialize OpenAI
        openai.api_key = api_key
        prompt = f"Summarize text into slides. Each slide JSON: title, bullets[], notes. Guidance: {guidance}\n\n{text}"
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        slides_json = resp["choices"][0]["message"]["content"]

        try:
            slides = json.loads(slides_json)
        except:
            # fallback
            slides = [{"title": "Slide 1", "bullets": [text[:100]], "notes": ""}]

        prs = Presentation(template_path)
        for slide_data in slides:
            layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(layout)
            slide.shapes.title.text = slide_data["title"]
            body = slide.placeholders[1].text_frame
            for b in slide_data["bullets"]:
                body.add_paragraph(b)
            if "notes" in slide_data:
                slide.notes_slide.notes_text_frame.text = slide_data["notes"]

        out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx").name
        prs.save(out_file)
        return FileResponse(out_file, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename="generated.pptx")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
