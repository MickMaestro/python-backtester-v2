"""Placeholder strategy for manual trading sessions.

It never trades on its own — the GUI injects the user's orders straight into
the broker. Running a manual session through the normal engine means fills,
SL/TP, spread, commission, swap, equity, and statistics behave exactly as they
do for an automated strategy.
"""

from __future__ import annotations

from backtester.strategy.base import Strategy


class ManualStrategy(Strategy):
    params: dict = {}

    def on_bar(self, bar) -> None:
        pass
