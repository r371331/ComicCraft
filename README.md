# ComicCraft — AI Comic Story Creator

ComicCraft is a complete FastAPI web application that turns a short idea into a multi-panel comic.

## Features
- FastAPI backend + Jinja2 frontend
- Gemini-powered story/panel generation
- Optional Hugging Face text-to-image generation
- Demo/offline mode that works without API keys
- Comic preview in the browser
- PNG panel generation
- PDF export
- JSON API
- Health endpoint
- Automated tests

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py
│   │   ├── image_service.py
│   │   ├── comic_service.py
│   │   └── pdf_service.py
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── tests/
│   └── test_app.py
├── output/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. VS Code setup

Install:
- Python 3.11 or newer
- VS Code
- VS Code Python extension

Open the `ComicCraft` folder in VS Code.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Configure environment

Copy `.env.example` to `.env`.

For an immediate local test, keep:

```env
DEMO_MODE=true
```

For real Gemini generation:

```env
DEMO_MODE=false
GEMINI_API_KEY=your_key_here
```

For Hugging Face images:

```env
HF_TOKEN=your_hugging_face_token
```

You can use Gemini for text and Hugging Face Inference Providers for images. The image service is optional; without `HF_TOKEN`, ComicCraft automatically creates deterministic demo artwork.

## 3. Run

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 4. Test

```powershell
python -m pytest -q
```

Health check:

```text
http://127.0.0.1:8000/health
```

## 5. API

### Generate a comic

`POST /api/generate`

Example JSON:

```json
{
  "title": "The Last Robot",
  "idea": "A small robot discovers a lonely garden on Mars.",
  "genre": "Sci-Fi",
  "tone": "Hopeful",
  "panel_count": 6
}
```

### JSON response

The API returns the comic title, panel descriptions, dialogue, image paths, and PDF download path.

### Browser form

The home page uses the same API and renders the result directly.

## Notes

- `.env` is intentionally ignored by Git.
- Generated files are stored under `output/`.
- Demo mode requires no paid service and is useful for testing the complete UI/backend pipeline.
- Real Gemini requests require a valid Gemini API key.
- Real image generation requires a Hugging Face token with the appropriate inference permissions.
