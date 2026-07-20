"""Grid-search parameter optimization, optionally across CPU cores.

``strategy_spec`` identifies the strategy in a picklable way so worker
processes can re-import it:

- ``("builtin", name)`` — a strategy from ``backtester.strategy.examples``
- ``("file", path, class_name)`` — a user strategy loaded from a .py file
- a Strategy class directly (only valid with ``workers=0``, in-process)

``workers=0`` runs serially in the current process (used by tests and small
grids); otherwise a ``ProcessPoolExecutor`` fans the grid out.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from itertools import product
from typing import Callable

import pandas as pd

from .backtester import BacktestConfig


@dataclass
class OptimizationResult:
    params: dict
    stats: dict = field(default_factory=dict)
    error: str | None = None


def build_grid(ranges: dict[str, list]) -> list[dict]:
    """{"fast": [5, 10], "slow": [20, 30]} → the 4 combinations."""
    keys = list(ranges)
    return [dict(zip(keys, combo)) for combo in product(*ranges.values())]


def steps(start: float, stop: float, step: float, as_int: bool = False) -> list:
    """Inclusive range with float-safe stepping."""
    if step <= 0:
        raise ValueError("step must be positive")
    values: list = []
    value = start
    while value <= stop + 1e-9:
        values.append(int(round(value)) if as_int else round(value, 10))
        value += step
    return values


# Worker-process globals, populated once per worker by _init_worker.
_G: dict = {}


def _init_worker(df, strategy_spec, config, intrabar_df) -> None:
    _G["df"] = df
    _G["spec"] = strategy_spec
    _G["config"] = config
    _G["intrabar"] = intrabar_df


def _resolve_strategy(spec):
    if isinstance(spec, type):
        return spec
    kind = spec[0]
    if kind == "builtin":
        from backtester.strategy.examples import STRATEGIES

        return STRATEGIES[spec[1]]
    if kind == "file":
        from backtester.strategy.loader import load_strategy_class

        return load_strategy_class(spec[1], spec[2])
    raise ValueError(f"Unknown strategy spec: {spec!r}")


def _run_one(params: dict) -> OptimizationResult:
    from backtester.engine.backtester import Backtester

    try:
        strategy = _resolve_strategy(_G["spec"])(**params)
        result = Backtester(
            _G["df"], strategy, _G["config"], intrabar_df=_G["intrabar"]
        ).run_all()
        return OptimizationResult(params=params, stats=result.stats)
    except Exception as exc:
        return OptimizationResult(params=params, error=f"{type(exc).__name__}: {exc}")


def optimize(
    df: pd.DataFrame,
    strategy_spec,
    grid: list[dict],
    config: BacktestConfig | None = None,
    workers: int | None = None,
    intrabar_df: pd.DataFrame | None = None,
    progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> list[OptimizationResult]:
    config = config or BacktestConfig()
    total = len(grid)
    results: list[OptimizationResult] = []

    if workers == 0:
        _init_worker(df, strategy_spec, config, intrabar_df)
        for i, params in enumerate(grid, start=1):
            if should_stop is not None and should_stop():
                break
            results.append(_run_one(params))
            if progress is not None:
                progress(i, total)
        return results

    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_init_worker,
        initargs=(df, strategy_spec, config, intrabar_df),
    ) as pool:
        futures = [pool.submit(_run_one, params) for params in grid]
        done = 0
        for future in as_completed(futures):
            if should_stop is not None and should_stop():
                pool.shutdown(wait=False, cancel_futures=True)
                break
            results.append(future.result())
            done += 1
            if progress is not None:
                progress(done, total)
    return results
