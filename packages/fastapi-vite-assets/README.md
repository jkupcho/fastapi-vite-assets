# FastAPI Vite Integration

Seamless Vite asset management for FastAPI applications with Jinja2 templates.

## Features

- 🔥 **Hot Module Replacement (HMR)** in development
- 📦 **Automatic manifest parsing** for production builds
- 🎯 **Simple API** - one function call to setup
- ⚡ **Fast** - leverages Vite's speed in development
- 🔧 **Configurable** - customize paths and behavior
- 🎨 **Framework agnostic** - works with any Vite frontend setup

## Installation

```bash
# Using uv
uv add fastapi-vite-assets

# Using pip
pip install fastapi-vite-assets
```

## Quick Start

### 1. Configure Vite

In your `vite.config.ts`:

```typescript
import { defineConfig } from "vite";

export default defineConfig({
  build: {
    manifest: true,
    rollupOptions: {
      input: ["src/main.ts", "src/style.css"],
    },
  },
});
```

### 2. Setup FastAPI

```python
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_vite_assets import ViteConfig, setup_vite

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure Vite integration
vite_config = ViteConfig(
    assets_path="web/dist",
    manifest_path="web/dist/.vite/manifest.json",
)
setup_vite(app, templates, vite_config)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

### 3. Create Templates

In `templates/base.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
    {{ vite_hmr_client() }}
    {{ vite_asset("src/style.css") }}
</head>
<body>
    {% block content %}{% endblock %}
    {{ vite_asset("src/main.ts") }}
</body>
</html>
```

## Configuration

### ViteConfig Options

```python
ViteConfig(
    # Path to Vite build output directory
    assets_path: str = "dist",

    # Path to Vite manifest.json
    manifest_path: str = "dist/.vite/manifest.json",

    # Vite dev server URL
    dev_server_url: str = "http://localhost:5173",

    # URL prefix for static assets in production
    static_url_prefix: str = "/static",

    # Auto-detect dev mode from ENV variable
    auto_detect_dev: bool = True,

    # Force dev/prod mode (overrides auto-detection)
    force_dev_mode: Optional[bool] = None,

    # Base path to resolve relative paths
    base_path: Optional[Path] = None,
)
```

### Environment Variables

- `ENV` - Set to `"production"` for production mode (default: `"development"`)
- `VITE_HOST` - Override Vite dev server host (default: from `dev_server_url`)
- `VITE_PORT` - Override Vite dev server port (default: from `dev_server_url`)

## Template Functions

### `vite_hmr_client()`

Injects the Vite HMR client script tag in development mode. Does nothing in production.

```html
{{ vite_hmr_client() }}
```

### `vite_asset(path)`

Injects the appropriate asset tag(s) for the given entry point.

**Development mode:** Points to Vite dev server
```html
<script type="module" src="http://localhost:5173/src/main.ts"></script>
```

**Production mode:** Reads from manifest and includes all dependencies
```html
<script type="module" src="/static/assets/main-abc123.js"></script>
<link rel="stylesheet" href="/static/assets/main-def456.css">
```

## Development vs Production

### Development
```bash
# Terminal 1 - Start Vite dev server
cd web && npm run dev

# Terminal 2 - Start FastAPI
fastapi dev app/main.py
```

### Production
```bash
# Build Vite assets
cd web && npm run build

# Run FastAPI with production environment
ENV=production uvicorn app.main:app
```

## Docker Deployment

See the example `Dockerfile` in the repository for a multistage build setup.

## Examples

Check out the `packages/example` directory for a complete working example.

## License

MIT
