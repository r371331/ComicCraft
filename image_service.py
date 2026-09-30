from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient

from app.config import settings


def _font(size: int):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                pass
    return ImageFont.load_default()


def create_demo_image(prompt: str, output_file: Path, panel_number: int) -> None:
    width, height = 1024, 768
    image = Image.new("RGB", (width, height), (245, 238, 218))
    draw = ImageDraw.Draw(image)

    # Simple deterministic artwork so the complete application works offline.
    margin = 45
    draw.rectangle(
        (margin, margin, width - margin, height - margin),
        outline=(25, 25, 25),
        width=8,
    )
    draw.ellipse((260, 180, 500, 420), outline=(25, 25, 25), width=8)
    draw.ellipse((335, 245, 360, 270), fill=(25, 25, 25))
    draw.ellipse((400, 245, 425, 270), fill=(25, 25, 25))
    draw.arc((330, 285, 430, 370), 10, 170, fill=(25, 25, 25), width=6)

    title_font = _font(42)
    small_font = _font(25)
    draw.text((80, 80), f"COMICCRAFT • PANEL {panel_number}", font=title_font, fill=(20, 20, 20))
    short_prompt = " ".join(prompt.split())
    if len(short_prompt) > 110:
        short_prompt = short_prompt[:107] + "..."
    draw.text((80, 650), short_prompt, font=small_font, fill=(40, 40, 40))

    image.save(output_file, "PNG")


def generate_image(prompt: str, output_file: Path, panel_number: int) -> None:
    if settings.demo_mode or not settings.hf_token:
        create_demo_image(prompt, output_file, panel_number)
        return

    client = InferenceClient(
        api_key=settings.hf_token,
        provider="auto",
    )
    image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
        width=1024,
        height=768,
    )
    image.save(output_file, "PNG")
