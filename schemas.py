from pydantic import BaseModel, Field, field_validator


class ComicRequest(BaseModel):
    title: str = Field(default="Untitled Comic", min_length=1, max_length=100)
    idea: str = Field(min_length=5, max_length=2000)
    genre: str = Field(default="Adventure", max_length=50)
    tone: str = Field(default="Fun", max_length=50)
    panel_count: int = Field(default=6, ge=2, le=8)

    @field_validator("title", "idea", "genre", "tone")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return " ".join(value.strip().split())


class ComicPanel(BaseModel):
    number: int
    scene: str
    narration: str = ""
    dialogue: str = ""
    image_prompt: str
    image_url: str = ""


class Comic(BaseModel):
    title: str
    genre: str
    tone: str
    panels: list[ComicPanel]
    pdf_url: str = ""
