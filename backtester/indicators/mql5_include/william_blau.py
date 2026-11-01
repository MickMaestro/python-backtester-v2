"""``WilliamBlau.mqh`` (MetaQuotes, 2010) — line-by-line port.

Helpers shared by MetaQuotes' William Blau indicator set (TSI, Ergodic,
CMI, SMI, …): an EMA that seeds on ``price[begin]`` and zero-fills the bars
before it, the applied-price buffer, and the price name used in short names.

Arrays are forward-indexed (bar 0 = oldest). The MQL5 originals temporarily
switch series-indexed arrays to forward indexing and back; numpy arrays have
no such flag, so callers pass forward-indexed arrays.
"""

from __future__ import annotations

from .mql_runtime import (
    PRICE_CLOSE, PRICE_HIGH, PRICE_LOW, PRICE_MEDIAN, PRICE_OPEN,
    PRICE_TYPICAL, PRICE_WEIGHTED,
)


def ExponentialMAOnBufferWB(rates_total, prev_calculated, begin, period, price, buffer) -> int:
    """EMA of ``price`` into ``buffer`` (modified in place).

    Unlike the standard library's ``ExponentialMAOnBuffer`` the bars before
    ``begin`` are set to 0.0 and the average starts at ``price[begin]`` with
    no SMA seed. Returns 0 (buffer untouched) when there is not enough data.
    """
    if period < 1 or rates_total - begin < period:
        return 0
    dSmoothFactor = 2.0 / (1.0 + period)
    if prev_calculated == 0:
        limit = period + begin
        for i in range(begin):
            buffer[i] = 0.0
        buffer[begin] = price[begin]
        for i in range(begin + 1, limit):
            buffer[i] = price[i] * dSmoothFactor + buffer[i - 1] * (1.0 - dSmoothFactor)
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        buffer[i] = price[i] * dSmoothFactor + buffer[i - 1] * (1.0 - dSmoothFactor)
    return rates_total


def PriceName(applied_price: int) -> str:
    return {
        PRICE_CLOSE: "close", PRICE_OPEN: "open", PRICE_HIGH: "high", PRICE_LOW: "low",
        PRICE_MEDIAN: "median", PRICE_TYPICAL: "typical", PRICE_WEIGHTED: "weighted",
    }.get(int(applied_price), "")


def CalculatePriceBuffer(applied_price, rates_total, prev_calculated, Open, High, Low, Close,
                         Price) -> int:
    """Fill ``Price`` (in place) with the applied price; unknown codes give 0.0."""
    pos = 0 if prev_calculated == 0 else prev_calculated - 1
    ap = int(applied_price)
    for i in range(pos, rates_total):
        if ap == PRICE_CLOSE:
            Price[i] = Close[i]
        elif ap == PRICE_OPEN:
            Price[i] = Open[i]
        elif ap == PRICE_HIGH:
            Price[i] = High[i]
        elif ap == PRICE_LOW:
            Price[i] = Low[i]
        elif ap == PRICE_MEDIAN:
            Price[i] = (High[i] + Low[i]) / 2.0
        elif ap == PRICE_TYPICAL:
            Price[i] = (High[i] + Low[i] + Close[i]) / 3.0
        elif ap == PRICE_WEIGHTED:
            Price[i] = (High[i] + Low[i] + Close[i] + Close[i]) / 4.0
        else:
            Price[i] = 0.0
    return rates_total
