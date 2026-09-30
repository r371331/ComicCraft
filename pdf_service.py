from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

from app.schemas import Comic


def create_pdf(comic: Comic, image_files: list[Path], output_file: Path) -> None:
    page_w, page_h = A4
    pdf = canvas.Canvas(str(output_file), pagesize=A4)

    for index, (panel, image_file) in enumerate(zip(comic.panels, image_files), start=1):
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(40, page_h - 45, f"{comic.title} — Panel {index}")

        max_w = page_w - 80
        max_h = page_h * 0.62

        with Image.open(image_file) as img:
            iw, ih = img.size
        scale = min(max_w / iw, max_h / ih)
        draw_w, draw_h = iw * scale, ih * scale

        x = (page_w - draw_w) / 2
        y = page_h - 70 - draw_h
        pdf.drawImage(str(image_file), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True)

        text_y = y - 25
        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, text_y, panel.narration[:150])
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, text_y - 22, panel.dialogue[:180])
        pdf.showPage()

    pdf.save()
