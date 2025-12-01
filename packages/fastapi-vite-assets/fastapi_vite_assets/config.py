"""Configuration for FastAPI Vite integration."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ViteConfig:
    """Configuration for Vite integration.

    Args:
        assets_path: Path to the Vite build output directory (default: "dist")
        manifest_path: Path to the Vite manifest.json file (default: "dist/.vite/manifest.json")
        dev_server_url: URL of the Vite dev server (default: "http://localhost:5173")
        static_url_prefix: URL prefix for serving static assets in production (default: "/static")
        auto_detect_dev: Automatically detect dev mode from ENV variable (default: True)
        force_dev_mode: Force development mode regardless of ENV (default: None)
        base_path: Base path to resolve relative paths from (default: current working directory)
    """

    assets_path: str = "dist"
    manifest_path: str = "dist/.vite/manifest.json"
    dev_server_url: str = "http://localhost:5173"
    static_url_prefix: str = "/static"
    auto_detect_dev: bool = True
    force_dev_mode: Optional[bool] = None
    base_path: Optional[Path] = None

    def __post_init__(self):
        """Initialize computed properties."""
        if self.base_path is None:
            self.base_path = Path.cwd()
        elif isinstance(self.base_path, str):
            self.base_path = Path(self.base_path)

    @property
    def is_dev_mode(self) -> bool:
        """Check if running in development mode."""
        if self.force_dev_mode is not None:
            return self.force_dev_mode

        if self.auto_detect_dev:
            return os.getenv("ENV", "development") == "development"

        return False

    @property
    def full_assets_path(self) -> Path:
        """Get the full path to assets directory."""
        assert self.base_path is not None  # Always set in __post_init__
        return self.base_path / self.assets_path

    @property
    def full_manifest_path(self) -> Path:
        """Get the full path to manifest file."""
        assert self.base_path is not None  # Always set in __post_init__
        return self.base_path / self.manifest_path

    def get_dev_server_host(self) -> str:
        """Get Vite dev server host from env or config."""
        if "VITE_HOST" in os.environ:
            host = os.getenv("VITE_HOST", "localhost")
            port = os.getenv("VITE_PORT", "5173")
            return f"http://{host}:{port}"
        return self.dev_server_url
