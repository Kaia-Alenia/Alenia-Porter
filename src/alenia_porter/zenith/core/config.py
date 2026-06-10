from dataclasses import dataclass, field


@dataclass
class ZenithConfig:
    workers: int = 4
    verbose: bool = False
    extra_exclusions: set[str] = field(default_factory=set)
    cache_path: str | None = None
