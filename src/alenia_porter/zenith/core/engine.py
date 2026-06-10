import sys
import threading
import importlib
from concurrent.futures import ThreadPoolExecutor

_bypass_lazy = threading.local()

_BASE_EXCLUSIONS: set[str] = {
    "zenith", "sys", "builtins", "importlib", "_thread", "threading",
    "concurrent", "queue", "abc", "functools", "atexit", "io",
    "codecs", "encodings", "signal", "weakref", "operator", "types",
    "typing", "warnings", "traceback", "linecache", "re", "enum",
    "os", "os.path", "posixpath", "pathlib", "stat", "genericpath",
    "posix", "_io", "site", "ast", "copy", "copyreg",
}


class SpeculationEngine:
    def __init__(self) -> None:
        self._executor: ThreadPoolExecutor | None = None
        self._preloaded: set[str] = set()
        self._failed: set[str] = set()
        self._lock = threading.Lock()
        self._workers: int = 4
        self._verbose: bool = False
        self._exclusions: set[str] = set(_BASE_EXCLUSIONS)

    def start(self, workers: int = 4, verbose: bool = False) -> None:
        self._workers = workers
        self._verbose = verbose
        self._executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="zenith-worker",
        )

    def add_exclusions(self, modules: set[str]) -> None:
        self._exclusions.update(modules)

    def preload(self, fullname: str) -> None:
        if self._executor is None:
            return
        root = fullname.split(".")[0]
        if root in self._exclusions:
            return
        with self._lock:
            if fullname in self._preloaded or fullname in self._failed:
                return
            self._preloaded.add(fullname)
        self._executor.submit(self._load_module, fullname)

    def register_module(self, fullname: str) -> None:
        self.preload(fullname)

    def _load_module(self, fullname: str) -> None:
        try:
            existing = sys.modules.get(fullname)
            if existing is not None and hasattr(existing, "_zenith_load_module"):
                existing._zenith_load_module()
                if self._verbose:
                    print(f"\033[92m[Zenith] Forced proxy load: {fullname}\033[0m")
                return

            _bypass_lazy.active = True
            try:
                importlib.import_module(fullname)
            finally:
                _bypass_lazy.active = False

            if self._verbose:
                print(f"\033[92m[Zenith] Pre-loaded: {fullname}\033[0m")

        except Exception:
            with self._lock:
                self._preloaded.discard(fullname)
                self._failed.add(fullname)

    def get_stats(self) -> dict[str, int | list[str]]:
        with self._lock:
            return {
                "workers": self._workers,
                "preloaded_count": len(self._preloaded),
                "failed_count": len(self._failed),
                "preloaded": sorted(self._preloaded),
                "failed": sorted(self._failed),
            }

    def shutdown(self, wait: bool = False) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=wait)
