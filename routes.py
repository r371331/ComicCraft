from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.schemas import ComicRequest
from app.services.comic_service import build_comic

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@router.post("/api/generate")
async def generate_api(payload: ComicRequest):
    comic = build_comic(payload)
    return JSONResponse(comic.model_dump())


@router.post("/generate")
async def generate_form(request: Request):
    form = await request.form()
    payload = ComicRequest(
        title=form.get("title", "Untitled Comic"),
        idea=form.get("idea", ""),
        genre=form.get("genre", "Adventure"),
        tone=form.get("tone", "Fun"),
        panel_count=int(form.get("panel_count", 6)),
    )
    comic = build_comic(payload)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name, "comic": comic},
    )


@router.get("/health")
async def health():
    return {"status": "ok", "demo_mode": settings.demo_mode}


@router.get("/generate-comic/json")
async def legacy_generate_json(
    title: str = "Untitled Comic",
    idea: str = "A friendly robot finds a hidden garden.",
    genre: str = "Adventure",
    tone: str = "Fun",
    panel_count: int = 6,
):
    payload = ComicRequest(
        title=title,
        idea=idea,
        genre=genre,
        tone=tone,
        panel_count=panel_count,
    )
    return build_comic(payload).model_dump()
