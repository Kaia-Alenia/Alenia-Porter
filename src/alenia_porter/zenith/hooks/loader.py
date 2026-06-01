import sys
import types
import importlib.abc
import importlib.machinery
from typing import Any

from alenia_porter.zenith.core.engine import _bypass_lazy

STRICT_EXCLUSIONS: set[str] = {
    "zenith", "sys", "builtins", "importlib", "_thread", "threading",
    "concurrent", "queue", "abc", "functools", "atexit", "io",
    "codecs", "encodings", "signal", "weakref", "operator", "types",
    "typing", "warnings", "traceback", "linecache", "re", "enum",
    "os", "os.path", "posixpath", "pathlib", "stat",
    "posix", "_io", "site", "ast",
    "PIL", "Pillow", "tkinter", "_tkinter", "webview", "clr", "ctypes", "_ctypes", "gi", "pkg_resources", "pkgutil",
}


class ZenithLazyModule(types.ModuleType):
    def __init__(
        self,
        spec: importlib.machinery.ModuleSpec,
        real_loader: importlib.abc.Loader,
        engine: Any,
        predictor: Any,
    ) -> None:
        super().__init__(spec.name)
        object.__setattr__(self, "_zenith_spec", spec)
        object.__setattr__(self, "_zenith_loader", real_loader)
        object.__setattr__(self, "_zenith_engine", engine)
        object.__setattr__(self, "_zenith_predictor", predictor)
        object.__setattr__(self, "_zenith_loaded", False)
        object.__setattr__(self, "_zenith_lock", __import__("threading").RLock())

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_zenith_") or (name.startswith("__") and name.endswith("__")):
            return object.__getattribute__(self, name)
        object.__getattribute__(self, "_zenith_load_module")()
        module_dict = object.__getattribute__(self, "__dict__")
        if name in module_dict:
            return module_dict[name]
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_zenith_") or (name.startswith("__") and name.endswith("__")):
            object.__setattr__(self, name, value)
            return
        object.__getattribute__(self, "_zenith_load_module")()
        object.__setattr__(self, name, value)

    def _zenith_load_module(self) -> None:
        lock = object.__getattribute__(self, "_zenith_lock")
        with lock:
            if object.__getattribute__(self, "_zenith_loaded"):
                return
            
            object.__setattr__(self, "_zenith_loaded", True)
            
            spec = object.__getattribute__(self, "_zenith_spec")
            loader = object.__getattribute__(self, "_zenith_loader")
            predictor = object.__getattribute__(self, "_zenith_predictor")
            engine = object.__getattribute__(self, "_zenith_engine")

            import sys as _sys
            _bypass_lazy.active = True
            try:
                loader.exec_module(self)
            except Exception:
                object.__setattr__(self, "_zenith_loaded", False)
                raise
            finally:
                _bypass_lazy.active = False

            _sys.modules[spec.name] = self
            if predictor is not None:
                predictor.save_module(spec.name)
            if engine is not None:
                engine.register_module(spec.name)



class ZenithLazyLoader(importlib.abc.Loader):
    def __init__(
        self,
        real_loader: importlib.abc.Loader,
        engine: Any,
        predictor: Any,
    ) -> None:
        self.real_loader = real_loader
        self.engine = engine
        self.predictor = predictor

    def create_module(
        self, spec: importlib.machinery.ModuleSpec
    ) -> types.ModuleType | None:
        return ZenithLazyModule(spec, self.real_loader, self.engine, self.predictor)

    def exec_module(self, module: types.ModuleType) -> None:
        pass


class ZenithLazyFinder(importlib.abc.MetaPathFinder):
    _active_searches: set[str] = set()

    def __init__(
        self,
        engine: Any,
        predictor: Any,
        ignored_packages: set[str] | None = None,
    ) -> None:
        self.engine = engine
        self.predictor = predictor
        self.ignored_packages: set[str] = ignored_packages or STRICT_EXCLUSIONS

    def find_spec(
        self,
        fullname: str,
        path: list[str | bytes] | None = None,
        target: types.ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        if getattr(_bypass_lazy, "active", False):
            return None

        if fullname in self._active_searches:
            return None

        root_pkg = fullname.split(".")[0]
        
        # SENIOR SAFETY RULE: Ignore stdlib, internal modules, and already ignored packages
        if root_pkg in self.ignored_packages or root_pkg.startswith("_") or root_pkg in sys.stdlib_module_names:
            return None

        self._active_searches.add(fullname)
        try:
            spec = None
            for finder in sys.meta_path:
                if finder is self:
                    continue
                try:
                    spec = finder.find_spec(fullname, path, target)
                    if spec is not None:
                        break
                except Exception:
                    continue

            if spec is not None and spec.loader is not None:
                if not isinstance(spec.loader, ZenithLazyLoader) and hasattr(
                    spec.loader, "exec_module"
                ):
                    spec.loader = ZenithLazyLoader(spec.loader, self.engine, self.predictor)
            return spec
        finally:
            self._active_searches.discard(fullname)


def install_hook(
    engine: Any,
    predictor: Any,
    extra_exclusions: set[str] | None = None,
) -> None:
    ignored = set(STRICT_EXCLUSIONS)
    if extra_exclusions:
        ignored.update(extra_exclusions)
    hook = ZenithLazyFinder(engine, predictor, ignored)
    sys.meta_path.insert(0, hook)
