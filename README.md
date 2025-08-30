# Your Text, Your Style

A web app that turns bulk text, markdown, or prose into a styled PowerPoint presentation using your own template.

## Features
- Paste text and split into slides automatically
- Upload `.pptx` template to apply style
- Download generated presentation
- User API key is optional (not stored)

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000

Deploy on Render

1.Push this repo to GitHub.

2.Create a Render Web Service → Select repo.

3.Build Command: pip install -r requirements.txt

4.Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT


---

### `LICENSE`
(MIT License)

---

