"""``MovingAverages.mqh`` — the MetaTrader 5 standard-library include
(``MQL5/Include/MovingAverages.mqh``, MetaQuotes) — line-by-line port.

It is not in the codebase's ``MQL5 Include`` folder because it ships with the
terminal, but 233 codebase indicators include it. This port was made from the
copy in the user's own terminal (10,737 bytes), so it matches the build they
run — including the two ``LinearWeightedMAOnBuffer`` overloads (the newer
6-argument one keeps running sums; the 7-argument one recomputes each bar and
returns the weight sum through ``weight_sum``).

Arrays
    ``price`` / ``buffer`` are forward-indexed (index 0 = oldest bar), which
    is what the ``*OnBuffer`` functions switch to internally with
    ``ArraySetAsSeries(..., false)``. ``buffer`` must be a mutable sequence of
    length ``rates_total`` (numpy array or list) and is written in place.
    If the MQL caller had set its arrays as series, pass ``price[::-1]`` /
    ``buffer[::-1]`` numpy views — writes go through to the original array,
    exactly as the include's temporary ``ArraySetAsSeries`` does.

Return values and empty slots follow the source: ``*OnBuffer`` return
``rates_total`` (or 0 when ``period <= 1`` or there are too few bars) and
fill the warm-up bars with 0.0, not EMPTY_VALUE. Faithfully kept quirks:

- ``SmoothedMA``: on the first bar (``position == period-1``) the SMA it
  computes is overwritten by the recursive formula with the caller's
  ``prev_value`` — so callers must seed ``prev_value`` themselves;
- ``*OnBuffer`` with ``period == 1`` returns 0 and leaves ``buffer`` as is;
- 7-argument ``LinearWeightedMAOnBuffer`` with ``prev_calculated > 0``
  divides by the ``weight_sum`` the caller kept from the first call
  (pass it back in; ``weight_sum`` is returned as the second value).
"""

from __future__ import annotations

from .mql_runtime import fdiv


def SimpleMA(position: int, period: int, price) -> float:
    result = 0.0
    if period > 0 and period <= (position + 1):
        for i in range(period):
            result += price[position - i]
        result /= period
    return result


def ExponentialMA(position: int, period: int, prev_value: float, price) -> float:
    result = 0.0
    if period > 0:
        pr = 2.0 / (period + 1.0)
        result = price[position] * pr + prev_value * (1 - pr)
    return result


def SmoothedMA(position: int, period: int, prev_value: float, price) -> float:
    result = 0.0
    if period > 0 and period <= (position + 1):
        if position == period - 1:
            for i in range(period):
                result += price[position - i]
            result /= period
        result = (prev_value * (period - 1) + price[position]) / period
    return result


def LinearWeightedMA(position: int, period: int, price) -> float:
    result = 0.0
    if period > 0 and period <= (position + 1):
        s = 0.0
        wsum = 0
        for i in range(period, 0, -1):
            wsum += i
            s += price[position - i + 1] * (period - i + 1)
        result = s / wsum
    return result


def _floats(price):
    return price.tolist() if hasattr(price, "tolist") else list(price)


def SimpleMAOnBuffer(rates_total: int, prev_calculated: int, begin: int, period: int,
                     price, buffer) -> int:
    if period <= 1 or period > (rates_total - begin):
        return 0
    p = _floats(price)
    b = _floats(buffer)
    if prev_calculated == 0:
        start_position = period + begin
        for i in range(start_position - 1):
            b[i] = 0.0
        first_value = 0.0
        for i in range(begin, start_position):
            first_value += p[i]
        b[start_position - 1] = first_value / period
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        b[i] = b[i - 1] + (p[i] - p[i - period]) / period
    buffer[:] = b
    return rates_total


def ExponentialMAOnBuffer(rates_total: int, prev_calculated: int, begin: int, period: int,
                          price, buffer) -> int:
    if period <= 1 or period > (rates_total - begin):
        return 0
    p = _floats(price)
    b = _floats(buffer)
    smooth_factor = 2.0 / (1.0 + period)
    if prev_calculated == 0:
        for i in range(begin):
            b[i] = 0.0
        start_position = period + begin
        b[begin] = p[begin]
        for i in range(begin + 1, start_position):
            b[i] = p[i] * smooth_factor + b[i - 1] * (1.0 - smooth_factor)
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        b[i] = p[i] * smooth_factor + b[i - 1] * (1.0 - smooth_factor)
    buffer[:] = b
    return rates_total


def LinearWeightedMAOnBuffer(rates_total: int, prev_calculated: int, begin: int, period: int,
                             price, buffer, weight_sum=None):
    """Both MQL overloads. Without ``weight_sum`` (6 arguments) returns
    ``rates_total``/0; with it (7 arguments, ``int &weight_sum``) returns
    ``(rates_total or 0, weight_sum)``."""
    if weight_sum is not None:
        return _lwma_on_buffer_ws(rates_total, prev_calculated, begin, period, price, buffer, weight_sum)
    if period <= 1 or period > (rates_total - begin):
        return 0
    p = _floats(price)
    b = _floats(buffer)
    if prev_calculated <= period + begin + 2:
        start_position = period + begin
        for i in range(start_position):
            b[i] = 0.0
    else:
        start_position = prev_calculated - 2
    s = 0.0
    lsum = 0.0
    weight = 0
    l = 1
    for i in range(start_position - period, start_position):
        s += p[i] * l
        lsum += p[i]
        weight += l
        l += 1
    b[start_position - 1] = s / weight
    for i in range(start_position, rates_total):
        s = s - lsum + p[i] * period
        lsum = lsum - p[i - period] + p[i]
        b[i] = s / weight
    buffer[:] = b
    return rates_total


def _lwma_on_buffer_ws(rates_total, prev_calculated, begin, period, price, buffer, weight_sum):
    if period <= 1 or period > (rates_total - begin):
        return 0, weight_sum
    p = _floats(price)
    b = _floats(buffer)
    if prev_calculated == 0:
        start_position = period + begin
        for i in range(start_position):
            b[i] = 0.0
        first_value = 0.0
        wsum = 0
        k = 1
        for i in range(begin, start_position):
            first_value += k * p[i]
            wsum += k
            k += 1
        b[start_position - 1] = first_value / wsum
        weight_sum = wsum
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        s = 0.0
        for j in range(period):
            s += (period - j) * p[i - j]
        b[i] = fdiv(s, weight_sum)           # weight_sum 0 → inf/nan, as MT5's float division
    buffer[:] = b
    return rates_total, weight_sum


def SmoothedMAOnBuffer(rates_total: int, prev_calculated: int, begin: int, period: int,
                       price, buffer) -> int:
    if period <= 1 or period > (rates_total - begin):
        return 0
    p = _floats(price)
    b = _floats(buffer)
    if prev_calculated == 0:
        start_position = period + begin
        for i in range(start_position - 1):
            b[i] = 0.0
        first_value = 0.0
        for i in range(begin, start_position):
            first_value += p[i]
        b[start_position - 1] = first_value / period
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        b[i] = (b[i - 1] * (period - 1) + p[i]) / period
    buffer[:] = b
    return rates_total
