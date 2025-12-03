# fastapi-vite-assets Project - Development Guide

This project is a FastAPI + Vite monorepo workspace demonstrating the `fastapi-vite-assets` integration library.

## Project Structure

```
fastapi-vite-assets/
├── pyproject.toml              # Workspace configuration
├── uv.lock                     # Locked dependencies
├── packages/
│   ├── fastapi-vite-assets/          # Reusable library for Vite integration
│   │   ├── fastapi_vite_assets/
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # ViteConfig class
│   │   │   ├── manifest.py    # Manifest reader
│   │   │   ├── template_helpers.py
│   │   │   └── integration.py # setup_vite() function
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── example/               # Example FastAPI application
│       ├── app/
│       │   ├── templates/
│       │   └── main.py
│       ├── web/               # Vite frontend
│       │   ├── src/
│       │   ├── vite.config.ts
│       │   └── package.json
│       ├── Dockerfile
│       ├── pyproject.toml
│       └── README.md
└── CLAUDE.md                  # This file
```

## Technology Stack

- **Backend**: FastAPI, Uvicorn, Jinja2
- **Frontend**: Vite, TypeScript, TailwindCSS, HTMX
- **Package Manager**: uv (Python), npm (Node.js)
- **Container**: Docker (multistage build)
- **Python Version**: 3.13+
- **Node Version**: 22+

## Key Concepts

### UV Workspace

This is a uv monorepo workspace with two packages:

- `fastapi-vite-assets`: A publishable library
- `example`: An example application that uses the library

The workspace is configured in the root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["packages/fastapi-vite-assets", "packages/example"]
```

### Workspace Dependencies

The `example` package depends on `fastapi-vite-assets` as a workspace member:

```toml
# packages/example/pyproject.toml
[project]
dependencies = [
    "fastapi[standard]>=0.122.0",
    "fastapi-vite-assets",
]

[tool.uv.sources]
fastapi-vite-assets = { workspace = true }
```

### FastAPI Vite Integration

The library provides seamless Vite integration for FastAPI:

1. **Development Mode**: Assets served from Vite dev server with HMR
2. **Production Mode**: Assets served from built manifest

Usage in FastAPI:

```python
from fastapi_vite_assets import ViteConfig, setup_vite

# Simple configuration - manifest_path is auto-derived
vite_config = ViteConfig(
    assets_path="web/dist",
    base_path=BASE_DIR.parent,  # BASE_DIR = Path(__file__).resolve().parent
)
setup_vite(app, templates, vite_config)
```

The `manifest_path` is automatically derived as `{assets_path}/.vite/manifest.json`.

Template usage:

```html
{{ vite_hmr_client() }} {{ vite_asset("src/main.ts") }} {{
vite_asset("src/style.css") }}
```

### Vite Configuration

The Vite build must generate a manifest for production:

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    manifest: true,
    rollupOptions: {
      input: ["src/main.ts", "src/style.css"],
    },
  },
});
```

## Development Workflow

### Initial Setup

```bash
# From workspace root
# IMPORTANT: Use --all-extras to install test, linting, and formatting dependencies
uv sync --all-extras

# Install frontend dependencies
cd packages/example/web
npm install
```

### Running Locally

**Terminal 1 - Vite dev server:**

```bash
cd packages/example/web
npm run dev
```

**Terminal 2 - FastAPI server:**

```bash
cd packages/example
uv run fastapi dev app/main.py
```

Visit: `http://localhost:8000`

### Environment Variables

- `ENV`: Set to `"production"` for production mode (default: `"development"`)
- `VITE_HOST`: Override Vite dev server host (default: `"localhost"`)
- `VITE_PORT`: Override Vite dev server port (default: `"5173"`)

## Production Deployment

### Manual Production Build

```bash
# Build frontend assets
cd packages/example/web
npm run build

# Run FastAPI with production env
cd ..
ENV=production uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment

The Dockerfile uses a multistage build:

1. **Stage 1**: Build Vite assets with Node Alpine
2. **Stage 2**: Install Python dependencies with uv
3. **Stage 3**: Final runtime image with Python slim

**Build from workspace root:**

```bash
docker build -f packages/example/Dockerfile -t example .
docker run -p 8000:8000 example
```

**Important Docker Notes:**

- Build context is the workspace root (`.`)
- Dockerfile location: `packages/example/Dockerfile`
- Must copy both `fastapi-vite-assets` library source and `example` app
- Vite assets copied to `/workspace/packages/example/web/dist`
- Base path in container: `/workspace/packages/example`

## Path Resolution

### Development (Local)

```
BASE_DIR = packages/example/app
BASE_DIR.parent = packages/example
base_path = packages/example
→ web/dist resolves to: packages/example/web/dist
```

### Production (Docker)

```
BASE_DIR = /workspace/packages/example/app
BASE_DIR.parent = /workspace/packages/example
base_path = /workspace/packages/example
→ web/dist resolves to: /workspace/packages/example/web/dist
```

## Common Commands

### UV Commands

```bash
# Sync all workspace dependencies (including test/lint/format tools)
# IMPORTANT: Use --all-extras for development to get pytest, ruff, pre-commit, etc.
uv sync --all-extras

# Sync without extras (minimal install, for production)
uv sync

# Add a dependency to a specific package
cd packages/example
uv add package-name

# Run a command with uv
uv run fastapi dev app/main.py

# Run tests (requires --all-extras)
cd packages/fastapi-vite-assets
uv run pytest

# Run linters/formatters (requires --all-extras)
uv run ruff check
uv run ruff format
```

### Pre-commit Hooks

Pre-commit hooks automatically check code quality before commits:

```bash
# Install hooks (one-time setup after cloning)
uv run pre-commit install

# Run hooks manually on all files
uv run pre-commit run --all-files

# Run hooks on staged files only
uv run pre-commit run

# Skip hooks for a specific commit (emergencies only)
git commit --no-verify -m "emergency fix"
```

**What the hooks check:**
- Ruff format (auto-fixes formatting)
- Ruff lint (catches common errors)
- Trailing whitespace removal
- End-of-file fixes
- YAML/TOML syntax validation
- Large file detection

**Scope**: Hooks run on all packages in the workspace (library and example)

### Vite Commands

```bash
# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Docker Commands

```bash
# Build image
docker build -f packages/example/Dockerfile -t example .

# Run container
docker run -p 8000:8000 example

# Run with environment override
docker run -p 8000:8000 -e ENV=development example

# Inspect container filesystem
docker run --rm example ls -la /workspace/packages/example/web/dist
```

## Publishing the Library

When ready to publish `fastapi-vite-assets` to PyPI:

```bash
cd packages/fastapi-vite-assets
uv build
uv publish
```

## Troubleshooting

### Assets not loading in Docker

1. Check manifest exists:

   ```bash
   docker run --rm example cat /workspace/packages/example/web/dist/.vite/manifest.json
   ```

2. Verify path resolution:

   ```bash
   docker run --rm example python -c "from pathlib import Path; print((Path('/workspace/packages/example') / 'web/dist/.vite/manifest.json').exists())"
   ```

3. Check ENV variable is set to production:
   ```bash
   docker run --rm example env | grep ENV
   ```

### Module not found errors

- Ensure workspace dependencies are synced: `uv sync`
- Check `[tool.uv.sources]` is configured in dependent packages
- For Docker, ensure library source is copied to container

### Vite dev server connection issues

- Check CORS settings in `vite.config.ts`
- Verify `VITE_HOST` and `VITE_PORT` environment variables
- Ensure Vite dev server is running on the expected port

## Best Practices

1. **Always build from workspace root** when using Docker
2. **Use `uv run`** to execute commands with the correct environment
3. **Keep paths relative** to `base_path` for portability
4. **Test both development and production modes** before deployment
5. **Use `.dockerignore`** to exclude unnecessary files from builds

## Architecture Decisions

### Why workspace packages?

- Allows developing library and example together
- Simulates real-world usage of the library
- Easy to test changes across both packages

### Why copy library source in Dockerfile?

- Workspace dependencies are installed as editable/symlinks
- Virtual environment contains references, not actual code
- Production needs the actual source files

### Why `base_path` instead of hardcoded paths?

- Portability between development and production
- Flexibility for different project structures
- Easier to reuse library in other projects

## Additional Notes

- Use zod/v4 when creating zod schemas (per global CLAUDE.md)
- TailwindCSS v4 is used with the Vite plugin
- HTMX is included for frontend interactivity
- FastAPI standard extras include uvicorn with recommended dependencies
