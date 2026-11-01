"""``CalcFrac.mqh`` — fractal tests over a user array — line-by-line port.

``values`` is whatever array the indicator fills (the source uses it
series-ordered or not depending on the indicator; the test is symmetric in
that ``after_period`` looks at ``bar+i`` and ``before_period`` at ``bar-i``).
A bar is a lower fractal when no neighbour within the windows is lower
(ties allowed), an upper fractal when none is higher.
"""

from __future__ import annotations


class CalcFrac:
    def __init__(self, before_period: int = 2, after_period: int = 2, values=None):
        self.before_period = before_period
        self.after_period = after_period
        self.values = values if values is not None else []

    def CountMax(self) -> int:
        return int(max(self.before_period, self.after_period))

    def is_lower_fr(self, bar: int) -> bool:
        v = self.values
        for i in range(1, self.CountMax() + 1):
            if i <= self.after_period and v[bar] > v[bar + i]:
                return False
            if i <= self.before_period and v[bar] > v[bar - i]:
                return False
        return True

    def is_upper_fr(self, bar: int) -> bool:
        v = self.values
        for i in range(1, self.CountMax() + 1):
            if i <= self.after_period and v[bar] < v[bar + i]:
                return False
            if i <= self.before_period and v[bar] < v[bar - i]:
                return False
        return True
