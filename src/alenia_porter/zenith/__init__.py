import atexit
from typing import Sequence

from .core.engine import SpeculationEngine
from .hooks.loader import install_hook, STRICT_EXCLUSIONS
from .speculation.predictor import ImportPredictor
from .transformer.ast_rewriter import analyze_file

__version__ = "1.2.0"
__all__ = ["ignite", "warm", "exclude", "status", "analyze", "invalidate_cache"]

_engine = SpeculationEngine()
_predictor = ImportPredictor()
_initialized: bool = False


def _print_banner() -> None:
    banner = """\033[95m
      _   _ _____ _   _ ___ _____ _   _
     / \\ | | ____| \\ | |_ _|_   _| | | |
    / _ \\| |  _| |  \\| || |  | | | |_| |
   / ___ \\ | |___| |\\  || |  | | |  _  |
  /_/   \\_\\_____|_| \\_|___|  |_| |_| |_|
         S T U D I O S   X   Z E N I T H
\033[0m"""
    print(banner)


def ignite(
    file: str | None = None,
    workers: int = 4,
    verbose: bool = False,
    exclude: Sequence[str] | None = None,
    cache_path: str | None = None,
    show_banner: bool = True,
) -> None:
    global _initialized
    if _initialized:
        return
    _initialized = True

    if show_banner:
        _print_banner()

    if cache_path:
        _predictor.set_cache_path(cache_path)

    extra_exclusions: set[str] = set(exclude) if exclude else set()

    _engine.start(workers=workers, verbose=verbose)
    _engine.add_exclusions(extra_exclusions)

    predictions = _predictor.load_predictions()
    for mod in predictions:
        _engine.preload(mod)

    install_hook(_engine, _predictor, extra_exclusions=extra_exclusions)

    if file:
        discovered = analyze_file(file)
        known = set(predictions)
        for mod in discovered:
            if mod not in known:
                _engine.preload(mod)

    atexit.register(_predictor.persist_cache)
    atexit.register(lambda: _engine.shutdown(wait=False))

    if verbose:
        n = len(predictions)
        print(f"\033[96m[Zenith] v{__version__} | workers={workers} | cached={n}\033[0m")


def warm(*modules: str) -> None:
    for mod in modules:
        _engine.preload(mod)


def exclude(*modules: str) -> None:
    STRICT_EXCLUSIONS.update(modules)
    _engine.add_exclusions(set(modules))


def analyze(file: str) -> list[str]:
    return analyze_file(file)


def status() -> dict:
    stats = _engine.get_stats()
    return {
        "version": __version__,
        "initialized": _initialized,
        "cached_modules": _predictor.load_predictions(),
        **stats,
    }


def invalidate_cache() -> None:
    _predictor.invalidate()
