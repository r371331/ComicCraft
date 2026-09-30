from pathlib import Path

from app.config import settings
from app.schemas import Comic, ComicRequest
from app.services.gemini_service import generate_panels
from app.services.image_service import generate_image
from app.services.pdf_service import create_pdf


def build_comic(request: ComicRequest) -> Comic:
    panels = generate_panels(request)

    image_files: list[Path] = []
    for panel in panels:
        filename = f"panel_{panel.number}.png"
        path = settings.output_path / filename
        generate_image(panel.image_prompt, path, panel.number)
        image_files.append(path)
        panel.image_url = f"/output/{filename}"

    comic = Comic(
        title=request.title,
        genre=request.genre,
        tone=request.tone,
        panels=panels,
    )

    pdf_name = "comic.pdf"
    pdf_path = settings.output_path / pdf_name
    create_pdf(comic, image_files, pdf_path)
    comic.pdf_url = f"/download/{pdf_name}"
    return comic
