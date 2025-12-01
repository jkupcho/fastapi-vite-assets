# Example App

Example FastAPI application demonstrating the use of `fastapi-vite-assets` library.

## Project Structure

```
example/
├── app/                    # FastAPI application
│   ├── templates/         # Jinja2 templates
│   └── main.py           # Application entry point
├── web/                   # Vite frontend
│   ├── src/
│   │   ├── main.ts
│   │   └── style.css
│   ├── package.json
│   └── vite.config.ts
├── Dockerfile            # Production build
└── pyproject.toml        # Python dependencies
```

## Development

### Prerequisites

- Python 3.13+
- Node.js 24+
- uv (Python package manager)

### Setup

```bash
# From workspace root
uv sync

# Install frontend dependencies
cd packages/example/web
npm install
```

### Running Locally

Start both the Vite dev server and FastAPI:

```bash
# Terminal 1 - Vite dev server
cd packages/example/web
npm run dev

# Terminal 2 - FastAPI server
cd packages/example
uv run fastapi dev app/main.py
```

Visit `http://localhost:8000`

## Production

### Build and Run with Docker

```bash
# From workspace root
docker build -f packages/example/Dockerfile -t example .
docker run -p 8000:8000 example
```

### Manual Production Build

```bash
# Build frontend assets
cd packages/example/web
npm run build

# Run FastAPI with production env
cd ..
ENV=production uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Features Demonstrated

- ✅ FastAPI with Jinja2 templates
- ✅ Vite integration for frontend assets
- ✅ HMR (Hot Module Replacement) in development
- ✅ Optimized production builds
- ✅ Multistage Docker build
- ✅ TailwindCSS and HTMX integration
