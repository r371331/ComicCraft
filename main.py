from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.routes import router


app = FastAPI(
    title=settings.app_name,
    description="Generate illustrated comics with Gemini and optional Hugging Face image generation.",
    version="1.0.0",
)

Path(settings.output_dir).mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/output", StaticFiles(directory=settings.output_dir), name="output")
app.include_router(router)


@app.get("/download/{filename}")
async def download(filename: str):
    safe_name = Path(filename).name
    path = settings.output_path / safe_name
    if not path.exists():
        return {"error": "File not found"}
    return FileResponse(path, filename=safe_name)
