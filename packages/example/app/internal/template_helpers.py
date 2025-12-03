import os
from jinja2 import pass_context
from markupsafe import Markup
from .vite import get_vite_manifest


def is_dev_mode() -> bool:
    """Check if running in development mode."""
    return os.getenv("ENV", "development") == "development"


@pass_context
def vite_hmr_client(context):
    """Inject Vite HMR client in development mode."""
    if not is_dev_mode():
        return Markup("")

    vite_host = os.getenv("VITE_HOST", "localhost")
    vite_port = os.getenv("VITE_PORT", "5173")

    return Markup(
        f'<script type="module" src="http://{vite_host}:{vite_port}/@vite/client"></script>'
    )


@pass_context
def vite_asset(context, path: str):
    """
    Inject Vite asset tags (script or link).
    In development: points to Vite dev server
    In production: reads from manifest and injects built files
    """
    if is_dev_mode():
        vite_host = os.getenv("VITE_HOST", "localhost")
        vite_port = os.getenv("VITE_PORT", "5173")
        url = f"http://{vite_host}:{vite_port}/{path}"

        if path.endswith(".css"):
            return Markup(f'<link rel="stylesheet" href="{url}">')
        else:
            return Markup(f'<script type="module" src="{url}"></script>')
    else:
        # Production mode - read from manifest
        manifest = get_vite_manifest()
        chunk = manifest.get_chunk(path)

        if not chunk:
            return Markup("")

        tags = []
        file_path = chunk.get("file")

        if file_path:
            if path.endswith(".css") or file_path.endswith(".css"):
                tags.append(f'<link rel="stylesheet" href="/static/{file_path}">')
            else:
                tags.append(
                    f'<script type="module" src="/static/{file_path}"></script>'
                )

        # Include CSS files referenced by this chunk
        if "css" in chunk:
            for css_file in chunk["css"]:
                tags.append(f'<link rel="stylesheet" href="/static/{css_file}">')

        return Markup("\n    ".join(tags))
