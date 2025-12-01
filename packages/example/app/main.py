from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_vite_assets import ViteConfig, setup_vite

app = FastAPI()

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configure and setup Vite integration
vite_config = ViteConfig(
    assets_path="web/dist",
    manifest_path="web/dist/.vite/manifest.json",
    base_path=BASE_DIR.parent,  # example root (packages/example)
)
setup_vite(app, templates, vite_config)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})