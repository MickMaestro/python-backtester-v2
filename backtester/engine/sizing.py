"""Position sizing: turn a risk intent into a lot size.

Pure math, no GUI — used by manual trading and available to strategies.
"""

from __future__ import annotations

import math
from enum import Enum

DEFAULT_LOT_STEP = 0.01
DEFAULT_MIN_LOTS = 0.01


class RiskMode(Enum):
    PERCENT_BALANCE = "percent"  # risk N% of the account balance
    CASH = "cash"                # risk a fixed cash amount
    LOTS = "lots"                # trade a fixed lot size


def risk_cash(mode: RiskMode, value: float, balance: float) -> float | None:
    """Cash the trade should put at risk, or None for fixed-lot sizing."""
    if mode is RiskMode.PERCENT_BALANCE:
        return balance * value / 100.0
    if mode is RiskMode.CASH:
        return value
    return None


def round_lots(
    lots: float, lot_step: float = DEFAULT_LOT_STEP, min_lots: float = DEFAULT_MIN_LOTS
) -> float:
    """Round *down* to the broker's lot step so risk is never overshot, with a
    floor at the minimum tradeable size."""
    if lot_step > 0:
        lots = math.floor(lots / lot_step + 1e-9) * lot_step
    return max(round(lots, 8), min_lots)


def compute_lots(
    mode: RiskMode,
    value: float,
    balance: float,
    entry: float | None,
    sl: float | None,
    contract_size: float,
    lot_step: float = DEFAULT_LOT_STEP,
    min_lots: float = DEFAULT_MIN_LOTS,
) -> float | None:
    """Lot size for the requested risk, or None if it can't be determined.

    Risk-based modes need a stop: the distance |entry - sl| is what defines how
    much a lot can lose. Without an SL there is nothing to size against, so the
    caller must fall back to fixed lots.

    Note the min-lots floor can mean the real risk exceeds the requested amount
    on very tight budgets — callers should show the *actual* cash at risk
    (see :func:`cash_at_risk`) rather than the requested figure.
    """
    if mode is RiskMode.LOTS:
        return round_lots(value, lot_step, min_lots) if value > 0 else None

    cash = risk_cash(mode, value, balance)
    if cash is None or cash <= 0:
        return None
    if entry is None or sl is None or contract_size <= 0:
        return None
    distance = abs(entry - sl)
    if distance <= 0:
        return None
    return round_lots(cash / (distance * contract_size), lot_step, min_lots)


def cash_at_risk(
    lots: float | None, entry: float | None, sl: float | None, contract_size: float
) -> float | None:
    """What the position actually loses if the stop is hit."""
    if lots is None or entry is None or sl is None:
        return None
    return lots * abs(entry - sl) * contract_size
