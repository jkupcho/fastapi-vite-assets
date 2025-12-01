"""FastAPI integration for Vite."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import ViteConfig
from .template_helpers import ViteTemplateHelpers


def setup_vite(
    app: FastAPI,
    templates: Jinja2Templates,
    config: ViteConfig | None = None,
) -> ViteTemplateHelpers:
    """Setup Vite integration with FastAPI.

    This function:
    1. Registers Jinja2 template functions for asset injection
    2. Mounts static file serving for production builds

    Args:
        app: FastAPI application instance
        templates: Jinja2Templates instance
        config: ViteConfig instance (uses defaults if None)

    Returns:
        ViteTemplateHelpers instance for advanced usage

    Example:
        ```python
        from fastapi import FastAPI
        from fastapi.templating import Jinja2Templates
        from fastapi_vite import ViteConfig, setup_vite

        app = FastAPI()
        templates = Jinja2Templates(directory="templates")

        vite = ViteConfig(
            assets_path="web/dist",
            manifest_path="web/dist/.vite/manifest.json"
        )

        setup_vite(app, templates, vite)
        ```
    """
    if config is None:
        config = ViteConfig()

    # Create template helpers
    helpers = ViteTemplateHelpers(config)

    # Register Jinja2 functions
    template_functions = helpers.create_jinja_functions()
    templates.env.globals.update(template_functions)

    # Mount static files for production
    if config.full_assets_path.exists():
        app.mount(
            config.static_url_prefix,
            StaticFiles(directory=str(config.full_assets_path)),
            name="static"
        )

    return helpers
