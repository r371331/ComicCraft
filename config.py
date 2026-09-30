from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    app_env: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    demo_mode: bool = True

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    hf_token: str = ""
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"

    output_dir: str = "output"
    max_panels: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def output_path(self) -> Path:
        path = Path(self.output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
