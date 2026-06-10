import json
import threading
from pathlib import Path

_DEFAULT_CACHE = ".zenith_cache.json"


class ImportPredictor:
    def __init__(self, cache_path: str | None = None) -> None:
        self.history: set[str] = set()
        self.lock = threading.Lock()
        self._cache_path = Path(cache_path or _DEFAULT_CACHE)

    def set_cache_path(self, path: str) -> None:
        self._cache_path = Path(path)

    def load_predictions(self) -> list[str]:
        if not self._cache_path.exists():
            return []
        try:
            with self._cache_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            modules = data.get("modules", [])
            return [m for m in modules if isinstance(m, str) and m.strip()]
        except Exception:
            return []

    def save_module(self, fullname: str) -> None:
        with self.lock:
            self.history.add(fullname)

    def persist_cache(self) -> None:
        try:
            with self.lock:
                saved = set(self.load_predictions())
                merged = list(saved.union(self.history))

            with self._cache_path.open("w", encoding="utf-8") as f:
                json.dump({"modules": sorted(merged)}, f, indent=4)
        except Exception:
            pass

    def invalidate(self) -> None:
        try:
            if self._cache_path.exists():
                self._cache_path.unlink()
        except Exception:
            pass


predictor = ImportPredictor()
