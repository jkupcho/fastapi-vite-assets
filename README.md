# FastAPI Vite Assets

A monorepo workspace providing seamless Vite integration for FastAPI applications with hot module replacement in development and optimized builds for production.

## Overview

This project consists of two packages:

1. **[fastapi-vite-assets](packages/fastapi-vite-assets/)** - A reusable library for integrating Vite with FastAPI and Jinja2 templates
2. **[example](packages/example/)** - A complete working example demonstrating the library in action

## What is this?

`fastapi-vite-assets` bridges the gap between FastAPI's backend and Vite's modern frontend tooling. It provides:

- **Development**: Hot Module Replacement (HMR) with live reload as you edit your TypeScript/CSS
- **Production**: Automatic manifest parsing and optimized asset serving with fingerprinted filenames
- **Simplicity**: One function call to setup, two template helpers to use

Perfect for building server-rendered FastAPI applications with modern frontend tooling.

## Quick Start

### 1. Install the library

```bash
# Using uv
uv add fastapi-vite-assets

# Using pip
pip install fastapi-vite-assets
```

### 2. Configure your FastAPI app

```python
from pathlib import Path
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi_vite_assets import ViteConfig, setup_vite

app = FastAPI()
templates = Jinja2Templates(directory="templates")

vite_config = ViteConfig(
    assets_path="assets",  # Where Vite builds to
    base_path=Path(__file__).resolve().parent,
)
setup_vite(app, templates, vite_config)
```

### 3. Use in templates

```html
<!DOCTYPE html>
<html>
<head>
    {{ vite_hmr_client() }}
    {{ vite_asset("src/style.css") }}
</head>
<body>
    <h1>Hello, Vite!</h1>
    {{ vite_asset("src/main.ts") }}
</body>
</html>
```

### 4. Run in development

```bash
# Terminal 1 - Vite dev server
cd web && npm run dev

# Terminal 2 - FastAPI
fastapi dev app/main.py
```

That's it! Your app now has HMR in development and optimized builds for production.

## Repository Structure

```
fastapi-vite-assets/
├── pyproject.toml              # Workspace configuration
├── uv.lock                     # Locked dependencies
├── packages/
│   ├── fastapi-vite-assets/    # Library package
│   │   ├── fastapi_vite_assets/
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # ViteConfig with validation
│   │   │   ├── manifest.py     # Manifest reader
│   │   │   ├── template_helpers.py # Jinja2 helpers
│   │   │   ├── integration.py  # setup_vite() function
│   │   │   └── logger.py       # Logging infrastructure
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md           # Library documentation
│   └── example/                # Example application
│       ├── app/
│       │   ├── templates/
│       │   └── main.py
│       ├── web/                # Vite frontend
│       │   ├── src/
│       │   ├── vite.config.ts
│       │   └── package.json
│       ├── Dockerfile
│       └── README.md           # Example documentation
├── CLAUDE.md                   # Development guide
└── README.md                   # This file
```

## Package: fastapi-vite-assets

The core library providing Vite integration for FastAPI.

**Key Features:**
- Hot Module Replacement (HMR) in development
- Automatic manifest parsing for production
- Production validation with configurable error handling
- Comprehensive logging for debugging
- Simple, intuitive API
- Highly configurable with sensible defaults

**Documentation:** See [packages/fastapi-vite-assets/README.md](packages/fastapi-vite-assets/README.md)

**Installation:**
```bash
uv add fastapi-vite-assets
# or
pip install fastapi-vite-assets
```

## Package: example

A complete working example application demonstrating best practices for using `fastapi-vite-assets`.

**Features:**
- FastAPI backend with Jinja2 templates
- Vite frontend with TypeScript
- TailwindCSS v4 for styling
- HTMX for interactivity
- Docker multistage build for production
- Development and production configurations

**Documentation:** See [packages/example/README.md](packages/example/README.md)

**Running the example:**
```bash
# From workspace root
uv sync --all-extras

# Install frontend dependencies
cd packages/example/web
npm install

# Terminal 1 - Vite dev server
npm run dev

# Terminal 2 - FastAPI
cd ..
uv run fastapi dev app/main.py
```

Visit `http://localhost:8000`

## Development

This is a UV workspace (monorepo) with Python package management via uv.

### Setup

```bash
# Clone the repository
git clone https://github.com/jkupcho/fastapi-vite-assets.git
cd fastapi-vite-assets

# Install all dependencies (including dev tools)
uv sync --all-extras

# Install frontend dependencies for example
cd packages/example/web
npm install
```

### Running Tests

```bash
cd packages/fastapi-vite-assets
uv run pytest --cov=fastapi_vite_assets
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Type checking
uv run mypy fastapi_vite_assets tests
```

## Production Deployment

### Docker

The example package includes a production-ready Dockerfile with multistage build:

```bash
# Build from workspace root
docker build -f packages/example/Dockerfile -t my-app .

# Run
docker run -p 8000:8000 my-app
```

### Manual Build

```bash
# Build Vite assets
cd packages/example/web
npm run build

# Run FastAPI in production mode
cd ..
ENV=production uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## How It Works

### Development Mode
When `ENV=development` (default):
- Template helpers point to Vite dev server (e.g., `http://localhost:5173/src/main.ts`)
- HMR client script is injected for live reloading
- No manifest file needed

### Production Mode
When `ENV=production`:
- Reads `.vite/manifest.json` to map source files to built assets
- Serves fingerprinted files with cache-friendly headers
- Includes all dependencies (CSS imports, dynamic imports, etc.)
- Validates that assets exist and warns if missing

## Contributing

Contributions are welcome! This project uses:
- **uv** for Python package management
- **pytest** for testing
- **ruff** for linting and formatting
- **mypy** for type checking
- **commitizen** for conventional commits

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## License

MIT License - see LICENSE file for details

## Links

- **Documentation**: [Library README](packages/fastapi-vite-assets/README.md)
- **Example App**: [Example README](packages/example/README.md)
- **Repository**: https://github.com/jkupcho/fastapi-vite-assets
- **Issues**: https://github.com/jkupcho/fastapi-vite-assets/issues

## Changelog

See [CHANGELOG.md](packages/fastapi-vite-assets/CHANGELOG.md) for version history.
