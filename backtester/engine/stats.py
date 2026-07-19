"""Performance metrics computed from closed trades and the equity curve."""

from __future__ import annotations

import numpy as np
import pandas as pd

_SECONDS_PER_YEAR = 365.25 * 24 * 3600


def compute_stats(trades: list, equity: pd.DataFrame, initial_balance: float) -> dict:
    nets = np.array([t.net for t in trades], dtype=float)
    wins = nets[nets > 0]
    losses = nets[nets <= 0]

    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(-losses.sum()) if len(losses) else 0.0
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    else:
        profit_factor = float("inf") if gross_profit > 0 else 0.0

    max_dd_abs, max_dd_pct = _max_drawdown(equity["equity"].to_numpy(dtype=float))

    return {
        "trades": len(trades),
        "net_profit": float(nets.sum()),
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor,
        "win_rate": len(wins) / len(trades) if trades else 0.0,
        "wins": int(len(wins)),
        "losses": int(len(losses)),
        "avg_win": float(wins.mean()) if len(wins) else 0.0,
        "avg_loss": float(losses.mean()) if len(losses) else 0.0,
        "largest_win": float(wins.max()) if len(wins) else 0.0,
        "largest_loss": float(losses.min()) if len(losses) else 0.0,
        "expectancy": float(nets.mean()) if len(nets) else 0.0,
        "max_consecutive_wins": _max_streak(nets, positive=True),
        "max_consecutive_losses": _max_streak(nets, positive=False),
        "max_drawdown": max_dd_abs,
        "max_drawdown_pct": max_dd_pct,
        "sharpe": _sharpe(equity),
        "return_pct": float(nets.sum()) / initial_balance * 100 if initial_balance else 0.0,
    }


def format_stats(stats: dict) -> str:
    pf = stats["profit_factor"]
    lines = [
        f"Trades:            {stats['trades']}   "
        f"(W {stats['wins']} / L {stats['losses']}, {stats['win_rate']:.1%})",
        f"Net profit:        {stats['net_profit']:,.2f}  ({stats['return_pct']:+.2f}%)",
        f"Gross profit/loss: {stats['gross_profit']:,.2f} / -{stats['gross_loss']:,.2f}",
        f"Profit factor:     {'∞' if pf == float('inf') else f'{pf:.2f}'}",
        f"Expectancy:        {stats['expectancy']:,.2f} per trade",
        f"Avg win / loss:    {stats['avg_win']:,.2f} / {stats['avg_loss']:,.2f}",
        f"Largest win/loss:  {stats['largest_win']:,.2f} / {stats['largest_loss']:,.2f}",
        f"Max consecutive:   {stats['max_consecutive_wins']} wins, "
        f"{stats['max_consecutive_losses']} losses",
        f"Max drawdown:      {stats['max_drawdown']:,.2f} ({stats['max_drawdown_pct']:.2f}%)",
        f"Sharpe (approx):   {stats['sharpe']:.2f}",
    ]
    return "\n".join(lines)


def _max_drawdown(equity: np.ndarray) -> tuple[float, float]:
    if len(equity) == 0:
        return 0.0, 0.0
    peaks = np.maximum.accumulate(equity)
    drawdowns = peaks - equity
    idx = int(np.argmax(drawdowns))
    max_abs = float(drawdowns[idx])
    max_pct = float(drawdowns[idx] / peaks[idx] * 100) if peaks[idx] > 0 else 0.0
    return max_abs, max_pct


def _max_streak(nets: np.ndarray, positive: bool) -> int:
    best = current = 0
    for net in nets:
        hit = net > 0 if positive else net <= 0
        current = current + 1 if hit else 0
        best = max(best, current)
    return best


def _sharpe(equity: pd.DataFrame) -> float:
    """Annualized Sharpe of per-bar equity returns (risk-free rate 0)."""
    values = equity["equity"].to_numpy(dtype=float)
    if len(values) < 3:
        return 0.0
    returns = np.diff(values) / values[:-1]
    std = returns.std(ddof=1)
    if std == 0 or np.isnan(std):
        return 0.0
    seconds = np.diff(equity["time"].to_numpy()).astype("timedelta64[s]").astype(float)
    median_dt = float(np.median(seconds)) or 3600.0
    bars_per_year = _SECONDS_PER_YEAR / median_dt
    return float(returns.mean() / std * np.sqrt(bars_per_year))
