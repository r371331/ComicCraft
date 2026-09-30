import json
from typing import Any

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import ComicPanel


SYSTEM_INSTRUCTION = """You are a professional comic-book writer.
Create concise, visual, family-friendly comic panels.
Return ONLY valid JSON: an array of objects with these keys:
number, scene, narration, dialogue, image_prompt.
The image_prompt must describe a single comic panel illustration and must not
contain speech bubbles or written text because dialogue is rendered separately.
Keep character descriptions consistent across panels.
"""


def _extract_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text)


def demo_panels(request) -> list[ComicPanel]:
    panels = []
    for i in range(1, request.panel_count + 1):
        if i == 1:
            scene = f"{request.idea} begins."
            dialogue = "Something unexpected is about to happen!"
        elif i == request.panel_count:
            scene = "The characters reach a satisfying conclusion."
            dialogue = "That was quite an adventure!"
        else:
            scene = f"The heroes move the story forward in a {request.genre.lower()} setting."
            dialogue = f"Panel {i}: Keep going!"
        panels.append(
            ComicPanel(
                number=i,
                scene=scene,
                narration=f"Panel {i}.",
                dialogue=dialogue,
                image_prompt=(
                    f"Colorful {request.genre.lower()} comic-book panel, "
                    f"{scene} Visual storytelling, expressive characters, "
                    f"clean line art, cinematic composition."
                ),
            )
        )
    return panels


def generate_panels(request) -> list[ComicPanel]:
    if settings.demo_mode or not settings.gemini_api_key:
        return demo_panels(request)

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""
Create exactly {request.panel_count} connected comic panels.

Title: {request.title}
Idea: {request.idea}
Genre: {request.genre}
Tone: {request.tone}

Make the story coherent from panel 1 through the final panel.
"""
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.9,
            max_output_tokens=5000,
            response_mime_type="application/json",
        ),
    )

    raw = response.text or "[]"
    data = _extract_json(raw)

    if not isinstance(data, list):
        raise ValueError("Gemini returned JSON in an unexpected format.")

    panels = []
    for index, item in enumerate(data[: request.panel_count], start=1):
        panels.append(
            ComicPanel(
                number=index,
                scene=str(item.get("scene", "")),
                narration=str(item.get("narration", "")),
                dialogue=str(item.get("dialogue", "")),
                image_prompt=str(item.get("image_prompt", "")),
            )
        )

    if len(panels) != request.panel_count:
        raise ValueError("Gemini did not return the requested number of panels.")

    return panels
