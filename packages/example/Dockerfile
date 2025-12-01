# Stage 1: Build Vite assets
FROM node:24-alpine AS vite-builder

WORKDIR /app

# Copy package files
COPY packages/example/web/package*.json ./

# Install dependencies
RUN npm ci

# Copy web source files
COPY packages/example/web/ ./

# Build Vite assets (creates dist/ with manifest.json)
RUN npm run build


# Stage 2: Build Python application with uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Set environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /workspace

# Copy workspace configuration and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=packages,target=packages \
    uv sync --frozen --no-dev


# Stage 3: Final runtime image
FROM python:3.13-slim-bookworm

# Set environment variables for production
ENV ENV=production \
    PYTHONUNBUFFERED=1 \
    PATH="/workspace/.venv/bin:$PATH"

WORKDIR /workspace

# Copy virtual environment from builder
COPY --from=builder /workspace/.venv /workspace/.venv

# Copy fastapi-vite-assets library source (workspace dependency)
COPY packages/fastapi-vite-assets /workspace/packages/fastapi-vite-assets

# Copy application code
COPY packages/example/app /workspace/packages/example/app

# Copy built Vite assets from vite-builder
# This matches the ViteConfig: assets_path="assets", base_path=BASE_DIR.parent
# Final path: /workspace/packages/example/assets/.vite/manifest.json
COPY --from=vite-builder /app/dist /workspace/packages/example/assets

# Expose port
EXPOSE 8000

# Run FastAPI application with uvicorn
CMD ["uvicorn", "packages.example.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
