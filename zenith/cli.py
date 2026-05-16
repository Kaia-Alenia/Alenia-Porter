import argparse
import sys
import subprocess
import json


def cmd_analyze(args: argparse.Namespace) -> None:
    from zenith.transformer.ast_rewriter import analyze_file, analyze_stdlib_only, analyze_third_party

    all_mods = analyze_file(args.file)
    stdlib = analyze_stdlib_only(args.file)
    third = analyze_third_party(args.file)

    print(f"\n\033[95m[Zenith Analyzer] {args.file}\033[0m")
    print(f"  Total imports : {len(all_mods)}")
    print(f"  Stdlib        : {len(stdlib)}")
    print(f"  Third-party   : {len(third)}")

    if args.verbose:
        if stdlib:
            print("\n\033[96mStdlib:\033[0m")
            for m in stdlib:
                print(f"  - {m}")
        if third:
            print("\n\033[93mThird-party:\033[0m")
            for m in third:
                print(f"  - {m}")


def cmd_status(args: argparse.Namespace) -> None:
    import zenith
    zenith.ignite(show_banner=False)
    info = zenith.status()
    print(f"\n\033[95m[Zenith Status] v{info['version']}\033[0m")
    print(f"  Initialized   : {info['initialized']}")
    print(f"  Workers       : {info['workers']}")
    print(f"  Preloaded     : {info['preloaded_count']}")
    print(f"  Failed        : {info['failed_count']}")
    print(f"  Cached modules: {len(info['cached_modules'])}")


def cmd_benchmark(args: argparse.Namespace) -> None:
    modules = args.modules or ["json", "sqlite3", "urllib.request", "xml.etree.ElementTree", "multiprocessing"]
    runs = args.runs

    def run_isolated(use_zenith: bool) -> float:
        mod_list = repr(modules)
        code = f"""
import sys, time
sys.path.insert(0, '.')
{'import zenith; zenith.ignite(show_banner=False)' if use_zenith else ''}
start = time.perf_counter()
for m in {mod_list}:
    __import__(m)
print(time.perf_counter() - start)
"""
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True,
        )
        try:
            return float(result.stdout.strip())
        except ValueError:
            return 0.0

    print(f"\n\033[95m[Zenith Benchmark] {runs} runs\033[0m")
    print("Running...\n")

    native_times = [run_isolated(False) for _ in range(runs)]
    zenith_times = [run_isolated(True) for _ in range(runs)]

    avg_n = sum(native_times) / runs
    avg_z = sum(zenith_times) / runs
    saved = avg_n - avg_z
    pct = (saved / avg_n * 100) if avg_n > 0 else 0

    print("-" * 45)
    print(f" {'METRIC':<16} | {'NATIVE':^10} | {'ZENITH':^10}")
    print("-" * 45)
    print(f" {'Avg Boot (s)':<16} | {avg_n:.5f}s  | {avg_z:.5f}s")
    print(f" {'Avg Boot (ms)':<16} | {avg_n*1000:.2f}ms  | {avg_z*1000:.2f}ms")
    print("-" * 45)
    label = f"Saved {saved*1000:.2f}ms ({pct:.1f}% faster)" if saved > 0 else f"Overhead {abs(saved)*1000:.2f}ms (cold cache — run again)"
    print(f" {label}")
    print("-" * 45)


def cmd_invalidate(args: argparse.Namespace) -> None:
    import zenith
    zenith.invalidate_cache()
    print("\033[92m[Zenith] Cache invalidated.\033[0m")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="zenith",
        description="Zenith — startup optimization toolkit for Python",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="Show imports in a Python file")
    p_analyze.add_argument("file", help="Path to Python file")
    p_analyze.add_argument("-v", "--verbose", action="store_true", help="List all imports")
    p_analyze.set_defaults(func=cmd_analyze)

    p_status = sub.add_parser("status", help="Show current Zenith cache status")
    p_status.set_defaults(func=cmd_status)

    p_bench = sub.add_parser("benchmark", help="Compare boot time with/without Zenith")
    p_bench.add_argument("--runs", type=int, default=5, help="Number of benchmark runs")
    p_bench.add_argument("--modules", nargs="+", help="Modules to benchmark")
    p_bench.set_defaults(func=cmd_benchmark)

    p_inv = sub.add_parser("invalidate", help="Clear the Zenith module cache")
    p_inv.set_defaults(func=cmd_invalidate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
