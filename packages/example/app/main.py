from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_vite_assets import ViteConfig, setup_vite

# Optional: Configure logging to see Vite integration logs
# import logging
# logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configure and setup Vite integration
# manifest_path is auto-derived as "assets/.vite/manifest.json"
vite_config = ViteConfig(
    assets_path="assets",
    base_path=BASE_DIR.parent,  # Points to packages/example
)
setup_vite(app, templates, vite_config)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})