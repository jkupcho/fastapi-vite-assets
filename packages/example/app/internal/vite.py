import json
from pathlib import Path
from typing import Dict, Optional


class ViteManifest:
    """Handles reading and parsing the Vite manifest file."""

    def __init__(self, manifest_path: str):
        self.manifest_path = Path(manifest_path)
        self._manifest: Optional[Dict] = None

    def load(self) -> Dict:
        """Load and parse the manifest file."""
        if not self.manifest_path.exists():
            return {}

        with open(self.manifest_path, "r") as f:
            self._manifest = json.load(f)

        return self._manifest

    def get_chunk(self, entry: str) -> Optional[Dict]:
        """Get a specific chunk from the manifest."""
        if self._manifest is None:
            self.load()

        return self._manifest.get(entry) if self._manifest else None


def get_vite_manifest() -> ViteManifest:
    """Get the Vite manifest for production builds."""
    manifest_path = (
        Path(__file__).parent.parent.parent / "web" / "dist" / ".vite" / "manifest.json"
    )
    return ViteManifest(str(manifest_path))
