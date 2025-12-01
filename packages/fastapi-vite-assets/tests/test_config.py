"""Tests for ViteConfig."""

import os
from pathlib import Path

import pytest

from fastapi_vite_assets.config import ViteConfig


class TestViteConfig:
    """Test ViteConfig class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ViteConfig()

        assert config.assets_path == "dist"
        assert config.manifest_path == "dist/.vite/manifest.json"
        assert config.dev_server_url == "http://localhost:5173"
        assert config.static_url_prefix == "/static"
        assert config.auto_detect_dev is True
        assert config.force_dev_mode is None
        assert config.base_path == Path.cwd()

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ViteConfig(
            assets_path="web/dist",
            manifest_path="web/dist/.vite/manifest.json",
            dev_server_url="http://localhost:3000",
            static_url_prefix="/assets",
            base_path="/app",
        )

        assert config.assets_path == "web/dist"
        assert config.manifest_path == "web/dist/.vite/manifest.json"
        assert config.dev_server_url == "http://localhost:3000"
        assert config.static_url_prefix == "/assets"
        assert config.base_path == Path("/app")

    def test_is_dev_mode_default(self, monkeypatch):
        """Test is_dev_mode with default ENV."""
        config = ViteConfig()
        monkeypatch.delenv("ENV", raising=False)

        assert config.is_dev_mode is True  # Default is development

    def test_is_dev_mode_production(self, monkeypatch):
        """Test is_dev_mode with production ENV."""
        config = ViteConfig()
        monkeypatch.setenv("ENV", "production")

        assert config.is_dev_mode is False

    def test_is_dev_mode_forced(self, monkeypatch):
        """Test is_dev_mode with force_dev_mode."""
        monkeypatch.setenv("ENV", "production")

        config = ViteConfig(force_dev_mode=True)
        assert config.is_dev_mode is True

        config = ViteConfig(force_dev_mode=False)
        assert config.is_dev_mode is False

    def test_full_assets_path(self):
        """Test full_assets_path property."""
        config = ViteConfig(
            assets_path="web/dist",
            base_path="/app",
        )

        assert config.full_assets_path == Path("/app/web/dist")

    def test_full_manifest_path(self):
        """Test full_manifest_path property."""
        config = ViteConfig(
            manifest_path="web/dist/.vite/manifest.json",
            base_path="/app",
        )

        assert config.full_manifest_path == Path("/app/web/dist/.vite/manifest.json")

    def test_get_dev_server_host_from_env(self, monkeypatch):
        """Test get_dev_server_host with environment variables."""
        config = ViteConfig()

        monkeypatch.setenv("VITE_HOST", "0.0.0.0")
        monkeypatch.setenv("VITE_PORT", "8080")

        assert config.get_dev_server_host() == "http://0.0.0.0:8080"

    def test_get_dev_server_host_from_config(self, monkeypatch):
        """Test get_dev_server_host with config value."""
        monkeypatch.delenv("VITE_HOST", raising=False)
        monkeypatch.delenv("VITE_PORT", raising=False)

        config = ViteConfig(dev_server_url="http://localhost:3000")

        assert config.get_dev_server_host() == "http://localhost:3000"
