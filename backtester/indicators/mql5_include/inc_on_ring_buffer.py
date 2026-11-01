"""``IncOnRingBuffer`` (Konstantin Gruzdev "Lizar", 2012) — line-by-line port of
the whole include folder:

``CArrayRing``, ``CArrayRing256``, ``CMAOnRingBuffer``, ``CEMAOnRingBuffer``
(an empty file in the Codebase download), ``CDEMAOnRingBuffer``,
``CTEMAOnRingBuffer``, ``CAMAOnRingBuffer``, ``CEROnRingBuffer``,
``CMomentumOnRingBuffer``, ``CRSIOnRingBuffer``, ``CMFIOnRingBuffer``,
``CMACDOnRingBuffer``, ``COsMAOnRingBuffer``, ``CATROnRingBuffer``,
``CADXOnRingBuffer``, ``CStochasticOnRingBuffer``, ``CFractalsOnRingBuffer``.

The library keeps only the newest ``size_buffer`` values of each indicator in
a ring, and its ``MainOnArray`` deliberately **starts calculating near the end
of the history** (``Begin()`` returns ``rates_total - Size() - BarsRequired``)
— the point of the library is cheap, bounded memory. Values are read back by
age: ``ring[0]`` (``At(0)``/``Last()``) is the newest, ``ring[1]`` the bar
before, and so on; anything older than the ring returns ``DBL_MAX``.

``MainOnValue`` is the per-bar entry point (one call per bar, oldest first,
``index`` forward-indexed unless the object was initialised ``as_series``).

All arrays passed to ``MainOnArray`` are forward-indexed (bar 0 = oldest);
the MQL5 originals flip series-indexed arrays to forward order themselves, so
this is the same thing.

Faithfully reproduced quirks of the source (worth knowing when a converted
indicator looks odd):

- ``CATROnRingBuffer.MainOnValue`` sets the "previous close" to the *current*
  close (``m_prev_close=close``), so after the first bar its true range is
  just ``high-low`` widened by nothing — the per-array path is unaffected.
- ``CDEMAOnRingBuffer.MainOnArray`` calls ``Last(EMPTY_VALUE)`` instead of
  ``Add`` while the second average warms up, so the ring does not advance
  during warm-up.
- ``CMACDOnRingBuffer.MainOnValue`` passes the member ``m_begin`` (only set by
  ``MainOnArray``) to its averages instead of its ``begin`` argument.
- An SMA/LWMA ring initialised with ``size_buffer <= period`` reads past its
  input ring and gets ``DBL_MAX`` (``CDEMAOnRingBuffer`` does this for its
  second average when ``method`` is SMA or LWMA).
- ``ArrayMaximum``/``ArrayMinimum`` return the first match in the array's
  logical order; for the series-ordered search in ``CFractalsOnRingBuffer``
  that means a tie resolves to the newer bar.

Not in the folder although indicators include it: ``CADXWOnRingBuffer.mqh``
(ADX Wilder). Indicators that need it are converted with the terminal's
Wilder ADX from :mod:`backtester.indicators.mql5` instead.
"""

from __future__ import annotations

from .mql_runtime import (
    DBL_MAX, EMPTY_VALUE, MODE_EMA, MODE_LWMA, MODE_SMA, MODE_SMMA,
    PRICE_CLOSE, PRICE_HIGH, PRICE_LOW, PRICE_MEDIAN, PRICE_OPEN,
    PRICE_TYPICAL, PRICE_WEIGHTED, UCHAR_MAX, idiv,
)

VOLUME_TICK, VOLUME_REAL = 0, 1

_MISSING = object()


def _array_maximum(array, start: int, count: int) -> int:
    best = start
    for i in range(start + 1, start + count):
        if array[i] > array[best]:
            best = i
    return best


def _array_minimum(array, start: int, count: int) -> int:
    best = start
    for i in range(start + 1, start + count):
        if array[i] < array[best]:
            best = i
    return best


def _first_valid(rates_total: int, *arrays) -> int:
    """``while(++i<rates_total) if(all non-zero, non-EMPTY) break;``"""
    i = -1
    while True:
        i += 1
        if i >= rates_total:
            return i
        if all(a[i] != 0 and a[i] != EMPTY_VALUE for a in arrays):
            return i


# ================================================================ CArrayRing


class CArrayRing:
    """A fixed-size ring of doubles; index 0 is the newest element."""

    def __init__(self):
        self.m_data: list = []
        self.m_last_pos = 0
        self.m_filling = EMPTY_VALUE
        self.m_size = len(self.m_data)

    def Init(self, size: int, volue: float = EMPTY_VALUE) -> bool:
        self.m_last_pos = 0
        self.m_filling = volue
        self.m_size = len(self.m_data)
        result = self.Resize(size)
        for i in range(self.m_size):
            self.m_data[i] = self.m_filling
        return result

    def Size(self) -> int:
        return self.m_size - 1

    def Resize(self, new_size: int) -> bool:
        new_size = int(new_size)
        if new_size < 0:
            return False
        if new_size > self.m_size:
            set_size = new_size
            self.m_data.extend([0.0] * (set_size - len(self.m_data)))
            if set_size > self.m_size:
                i, j = self.m_size - 1, set_size - 1
                while i > self.m_last_pos:
                    self.m_data[j] = self.m_data[i]
                    self.m_data[i] = self.m_filling
                    i -= 1
                    j -= 1
            self.m_size = set_size
            return True
        if new_size > self.m_last_pos + 1:
            i, j = self.m_size - 1, new_size - 1
            while j > self.m_last_pos:
                self.m_data[j] = self.m_data[i]
                i -= 1
                j -= 1
        else:
            i, j = self.m_last_pos + 1 - new_size, 0
            while i <= self.m_last_pos:
                self.m_data[j] = self.m_data[i]
                i += 1
                j += 1
            self.m_last_pos = new_size - 1
        self.m_size = new_size
        del self.m_data[new_size:]
        return True

    def Add(self, element: float) -> None:
        self.m_last_pos = (self.m_last_pos + 1) % self.m_size
        self.m_data[self.m_last_pos] = element

    def At(self, index: int) -> float:
        if idiv(index, self.m_size) == 0:
            return self.m_data[(self.m_size + self.m_last_pos - index) % self.m_size]
        return DBL_MAX

    def __getitem__(self, index: int) -> float:
        return self.At(index)

    def Last(self, element=_MISSING):
        """``Last()`` reads the newest element; ``Last(x)`` overwrites it."""
        if element is _MISSING:
            return self.m_data[self.m_last_pos]
        self.m_data[self.m_last_pos] = element
        return None

    def Update(self, element: float, index: int = 0) -> bool:
        if idiv(index, self.m_size) == 0:
            self.m_data[(self.m_size + self.m_last_pos - index) % self.m_size] = element
            return True
        return False


class CArrayRing256:
    """A 256-slot ring indexed by a wrapping ``uchar`` position."""

    def __init__(self):
        self.m_data: list = []
        self.m_size = 0
        self.m_last_pos = 0

    def Init(self, volue: float = EMPTY_VALUE) -> bool:
        self.m_last_pos = 0
        self.m_data = [volue] * (UCHAR_MAX + 1)
        self.m_size = UCHAR_MAX + 1
        return True

    def Size(self) -> int:
        return self.m_size - 1

    def Add(self, element: float) -> None:
        self.m_last_pos = (self.m_last_pos + 1) & 0xFF
        self.m_data[self.m_last_pos] = element

    def At(self, index: int) -> float:
        return self.m_data[(self.m_last_pos - (index & 0xFF)) & 0xFF]

    __getitem__ = At

    def Last(self, element=_MISSING):
        if element is _MISSING:
            return self.m_data[self.m_last_pos]
        self.m_data[self.m_last_pos] = element
        return None

    def Update(self, element: float, index: int = 0) -> None:
        self.m_data[(self.m_last_pos - (index & 0xFF)) & 0xFF] = element


# =========================================================== CMAOnRingBuffer


def _method_to_string(method: int) -> str:
    return {MODE_SMA: "SMA", MODE_EMA: "EMA", MODE_LWMA: "LWMA", MODE_SMMA: "SMMA"}.get(
        int(method), str(method))


class CMAOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.m_array_in: CArrayRing | None = None
        self.m_ma_period = 0
        self.m_ma_method = MODE_SMA
        self.m_as_series = False
        self.m_k1 = self.m_k2 = 0.0
        self.m_LK: list = []
        self.m_name = ""
        self.m_bars_required = 0
        self.m_start = 0
        self.m_index = 0

    def Init(self, ma_period: int = 14, ma_method: int = MODE_SMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        self.m_ma_period = 14 if ma_period <= 0 else int(ma_period)
        if size_buffer <= self.m_ma_period:
            size_buffer = self.m_ma_period
        if not CArrayRing.Init(self, size_buffer):
            return False
        coeff_required = 10
        self.m_as_series = as_series
        self.m_ma_method = int(ma_method)
        if self.m_ma_method == MODE_SMA:
            self.m_bars_required = self.m_ma_period
        elif self.m_ma_method == MODE_EMA:
            self.m_k1 = 2.0 / (self.m_ma_period + 1.0)
            self.m_k2 = 1.0 - self.m_k1
            self.m_bars_required = self.m_ma_period * coeff_required
        elif self.m_ma_method == MODE_SMMA:
            self.m_k1 = 1.0 / self.m_ma_period
            self.m_k2 = 1.0 - self.m_k1
            self.m_bars_required = self.m_ma_period * coeff_required
        elif self.m_ma_method == MODE_LWMA:
            self.m_LK = [float(self.m_ma_period - j) for j in range(self.m_ma_period)]
            total = sum(self.m_LK)
            self.m_LK = [w / total for w in self.m_LK]
            self.m_bars_required = self.m_ma_period
        self.m_name = f"{_method_to_string(self.m_ma_method)}({self.m_ma_period})"
        return True

    def BarsRequired(self) -> int:
        return self.m_bars_required

    def Name(self) -> str:
        return self.m_name

    def MAMethod(self) -> str:
        return _method_to_string(self.m_ma_method)

    def MAPeriod(self) -> int:
        return self.m_ma_period

    # ---------------------------------------------------------- on array

    def MainOnArray(self, rates_total: int, prev_calculated: int, array) -> int:
        if self.m_ma_method == MODE_SMA:
            self._sma_on_array(rates_total, prev_calculated, array)
        elif self.m_ma_method in (MODE_EMA, MODE_SMMA):
            self._ema_on_array(rates_total, prev_calculated, array)
        elif self.m_ma_method == MODE_LWMA:
            self._lwma_on_array(rates_total, prev_calculated, array)
        return rates_total

    def _begin(self, rates_total, array) -> int:
        i = _first_valid(rates_total, array)
        return max(i, rates_total - self.Size() - self.m_bars_required)

    def _sma_on_array(self, rates_total, prev_calculated, array):
        p = self.m_ma_period
        if prev_calculated == 0:
            self.m_start = self._begin(rates_total, array) + p - 1
            s = 0.0
            for i in range(self.m_start, self.m_start - p, -1):
                s += array[i]
            self.Last(s / p)
        else:
            self.m_start = prev_calculated - 1
            self.Last(self.At(1) - (array[self.m_start - p] - array[self.m_start]) / p)
        for i in range(self.m_start + 1, rates_total):
            self.Add(self.Last() - (array[i - p] - array[i]) / p)

    def _ema_on_array(self, rates_total, prev_calculated, array):
        if prev_calculated == 0:
            self.m_start = self._begin(rates_total, array)
            self.Last(array[self.m_start])
        else:
            self.m_start = prev_calculated - 1
            self.Last(self.m_k1 * array[self.m_start] + self.m_k2 * self.At(1))
        for i in range(self.m_start + 1, rates_total):
            self.Add(self.m_k1 * array[i] + self.m_k2 * self.Last())

    def _lwma_on_array(self, rates_total, prev_calculated, array):
        p = self.m_ma_period
        if prev_calculated == 0:
            self.m_start = self._begin(rates_total, array) + p - 1
        else:
            self.m_start = prev_calculated - 1
        volue = 0.0
        for j in range(p):
            volue += array[self.m_start - j] * self.m_LK[j]
        self.Last(volue)
        for i in range(self.m_start + 1, rates_total):
            volue = 0.0
            for j in range(p):
                volue += array[i - j] * self.m_LK[j]
            self.Add(volue)

    # ---------------------------------------------------------- on value

    def MainOnValue(self, rates_total: int, prev_calculated: int, begin: int, value: float,
                    index: int) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_ma_method == MODE_SMA:
            return self._sma_on_value(prev_calculated, begin, value, index)
        if self.m_ma_method in (MODE_EMA, MODE_SMMA):
            return self._ema_on_value(prev_calculated, begin, value, index)
        if self.m_ma_method == MODE_LWMA:
            return self._lwma_on_value(prev_calculated, begin, value, index)
        return EMPTY_VALUE

    def _fill_array_in(self, prev_calculated, value) -> bool:
        if self.m_array_in is None:
            self.m_array_in = CArrayRing()
            if not self.m_array_in.Init(self.Size()):
                return False
        if prev_calculated - 1 == self.m_index:
            self.m_array_in.Last(value)
        else:
            self.m_array_in.Add(value)
        return True

    def _sma_on_value(self, prev_calculated, begin, value, index):
        if not self._fill_array_in(prev_calculated, value):
            return EMPTY_VALUE
        p = self.m_ma_period
        self.m_start = begin + p - 1
        if self.m_index < self.m_start:
            return EMPTY_VALUE
        if self.m_index == self.m_start:
            s = 0.0
            for i in range(p):
                s += self.m_array_in[i]
            self.Last(s / p)
            return self.Last()
        if prev_calculated - 1 == self.m_index:
            self.Last(self.At(1) - (self.m_array_in[p] - value) / p)
        else:
            self.Add(self.Last() - (self.m_array_in[p] - value) / p)
        return self.Last()

    def _ema_on_value(self, prev_calculated, begin, value, index):
        if self.m_index == begin:
            self.Last(value)
            return value
        if prev_calculated - 1 == self.m_index:
            self.Last(self.m_k1 * value + self.m_k2 * self.At(1))
        else:
            self.Add(self.m_k1 * value + self.m_k2 * self.Last())
        return self.Last()

    def _lwma_on_value(self, prev_calculated, begin, value, index):
        if not self._fill_array_in(prev_calculated, value):
            return EMPTY_VALUE
        if self.m_index < begin + self.m_ma_period - 1:
            return EMPTY_VALUE
        volue = 0.0
        for j in range(self.m_ma_period):
            volue += self.m_array_in[j] * self.m_LK[j]
        if prev_calculated - 1 == self.m_index:
            self.Last(volue)
        else:
            self.Add(volue)
        return self.Last()


class CEMAOnRingBuffer(CMAOnRingBuffer):
    """``CEMAOnRingBuffer.mqh`` is empty in the Codebase download; nothing
    includes it. Kept as an EMA-defaulting alias of :class:`CMAOnRingBuffer`."""

    def Init(self, ma_period: int = 14, ma_method: int = MODE_EMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        return super().Init(ma_period, ma_method, size_buffer, as_series)


# ========================================================= CDEMA / CTEMA


class CDEMAOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.ma = CMAOnRingBuffer()
        self.m_ma2 = CMAOnRingBuffer()
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_begin1 = self.m_begin2 = 0
        self.m_start = self.m_index = 0

    def Init(self, period: int = 12, method: int = MODE_EMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        sizebuffer = 2 if size_buffer < 2 else size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.ma.Init(period, method, sizebuffer):
            return False
        if not self.m_ma2.Init(period, method, period + 1):
            return False
        self.m_name = f"DEMA({self.Period()},{self.Method()})"
        self.m_as_series = as_series
        self.m_bars_required = self.ma.BarsRequired() + self.m_ma2.BarsRequired()
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.ma.MAPeriod()

    def Method(self):
        return self.ma.MAMethod()

    def MA(self, index):
        return self.ma.At(index)

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_start = self.m_begin1 = max(i, rates_total - self.Size() - self.m_bars_required)
            self.m_begin2 = self.m_begin1 + self.ma.BarsRequired()
        else:
            self.m_start = prev_calculated - 1
        ma1 = self.ma.MainOnValue(rates_total, prev_calculated, self.m_begin1, array[self.m_start], self.m_start)
        ma2 = self.m_ma2.MainOnValue(rates_total, prev_calculated, self.m_begin2, ma1, self.m_start)
        if ma1 == EMPTY_VALUE or ma2 == EMPTY_VALUE:
            self.Last(EMPTY_VALUE)
        else:
            self.Last(2.0 * ma1 - ma2)
        for i in range(self.m_start + 1, rates_total):
            ma1 = self.ma.MainOnValue(rates_total, prev_calculated, self.m_begin1, array[i], i)
            ma2 = self.m_ma2.MainOnValue(rates_total, prev_calculated, self.m_begin2, ma1, i)
            if ma1 == EMPTY_VALUE or ma2 == EMPTY_VALUE:
                self.Last(EMPTY_VALUE)            # sic: Last, not Add
            else:
                self.Add(2.0 * ma1 - ma2)
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        if self.m_as_series:
            self.m_begin = rates_total - 1 - begin
            self.m_index = rates_total - 1 - index
        else:
            self.m_begin = begin
            self.m_index = index
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.m_begin1 = self.m_begin
            self.m_begin2 = self.m_begin + self.ma.BarsRequired()
        ma1 = self.ma.MainOnValue(rates_total, prev_calculated, self.m_begin1, value, self.m_index)
        ma2 = self.m_ma2.MainOnValue(rates_total, prev_calculated, self.m_begin2, ma1, self.m_index)
        if prev_calculated - 1 == self.m_index:
            self.Last(EMPTY_VALUE if ma1 == EMPTY_VALUE or ma2 == EMPTY_VALUE else 2.0 * ma1 - ma2)
        else:
            self.Add(EMPTY_VALUE if ma1 == EMPTY_VALUE or ma2 == EMPTY_VALUE else 2.0 * ma1 - ma2)
        return self.Last()


class CTEMAOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.dema = CDEMAOnRingBuffer()
        self.m_dema_err = CMAOnRingBuffer()
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin1 = self.m_begin2 = self.m_start = self.m_index = 0

    def Init(self, period: int = 12, method: int = MODE_EMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        sizebuffer = 2 if size_buffer < 2 else size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.dema.Init(period, method, sizebuffer):
            return False
        if not self.m_dema_err.Init(period, method, sizebuffer):
            return False
        self.m_name = f"TEMA({self.Period()},{self.Method()})"
        self.m_as_series = as_series
        self.m_bars_required = self.dema.BarsRequired() + self.m_dema_err.BarsRequired()
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.dema.Period()

    def Method(self):
        return self.dema.Method()

    def MA(self, index):
        return self.dema.ma.At(index)

    def DEMA(self, index):
        return self.dema.At(index)

    def _combine(self, demavalue, dema_err):
        if demavalue == EMPTY_VALUE or dema_err == EMPTY_VALUE:
            return EMPTY_VALUE
        return demavalue + dema_err

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_start = self.m_begin1 = max(i, rates_total - self.Size() - self.m_bars_required)
            self.m_begin2 = self.m_begin1 + self.dema.BarsRequired()
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        d = self.dema.MainOnValue(rates_total, prev_calculated, self.m_begin1, array[s], s)
        e = self.m_dema_err.MainOnValue(rates_total, prev_calculated, self.m_begin2, array[s] - d, s)
        self.Last(self._combine(d, e))
        for i in range(s + 1, rates_total):
            d = self.dema.MainOnValue(rates_total, prev_calculated, self.m_begin1, array[i], i)
            e = self.m_dema_err.MainOnValue(rates_total, prev_calculated, self.m_begin2, array[i] - d, i)
            self.Add(self._combine(d, e))
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_begin1 = begin
            self.m_begin2 = begin + self.dema.BarsRequired()
        d = self.dema.MainOnValue(rates_total, prev_calculated, self.m_begin1, value, self.m_index)
        e = self.m_dema_err.MainOnValue(rates_total, prev_calculated, self.m_begin2, value - d, self.m_index)
        if prev_calculated - 1 == self.m_index:
            self.Last(self._combine(d, e))
        else:
            self.Add(self._combine(d, e))
        return self.Last()


# ============================================================ CER / CAMA


class CEROnRingBuffer(CArrayRing):
    """Kaufman's efficiency ratio."""

    def __init__(self):
        super().__init__()
        self.m_array_in = CArrayRing()
        self.m_dnoise = CArrayRing()
        self.m_period = 0
        self.m_noise = 0.0
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, period: int = 34, size_buffer: int = 256, as_series: bool = False) -> bool:
        self.m_period = 34 if period <= 0 else int(period)
        sizebuffer = size_buffer
        if size_buffer < period + 1:
            sizebuffer = self.m_period + 1
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_dnoise.Init(self.m_period + 1):
            return False
        if not self.m_array_in.Init(self.m_period + 1):
            return False
        self.m_name = f"ER({self.m_period})"
        self.m_as_series = as_series
        self.m_bars_required = self.m_period + 1
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.m_period

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        p = self.m_period
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_start = max(i, rates_total - self.Size() - self.m_bars_required) + p
            self.m_noise = 0.0
            for i in range(self.m_start - p + 1, self.m_start + 1):
                self.m_dnoise.Add(abs(array[i] - array[i - 1]))
                self.m_noise += self.m_dnoise.Last()
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        self.m_noise -= self.m_dnoise.Last()
        self.m_dnoise.Last(abs(array[s] - array[s - 1]))
        self.m_noise += self.m_dnoise.Last()
        self.Last(0.0 if self.m_noise == 0 else abs(array[s] - array[s - p]) / self.m_noise)
        for i in range(s + 1, rates_total):
            self.m_dnoise.Add(abs(array[i] - array[i - 1]))
            self.m_noise += self.m_dnoise.Last() - self.m_dnoise[p]
            self.Add(0.0 if self.m_noise == 0 else abs(array[i] - array[i - p]) / self.m_noise)
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        p = self.m_period
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if prev_calculated - 1 == self.m_index:
            self.m_array_in.Last(value)
        else:
            self.m_array_in.Add(value)
        self.m_begin = begin + p
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.m_noise = 0.0
            for i in range(p - 1, -1, -1):
                self.m_dnoise.Add(abs(self.m_array_in[i] - self.m_array_in[i + 1]))
                self.m_noise += self.m_dnoise.Last()
            self.Add(0.0 if self.m_noise == 0 else abs(value - self.m_array_in[p]) / self.m_noise)
            return self.Last()
        if prev_calculated - 1 == self.m_index:
            self.m_noise -= self.m_dnoise.Last()
            self.m_dnoise.Last(abs(value - self.m_array_in[1]))
            self.m_noise += self.m_dnoise.Last()
            self.Last(0.0 if self.m_noise == 0 else abs(value - self.m_array_in[p]) / self.m_noise)
        else:
            self.m_dnoise.Add(abs(value - self.m_array_in[1]))
            self.m_noise += self.m_dnoise.Last() - self.m_dnoise[p]
            self.Add(0.0 if self.m_noise == 0 else abs(value - self.m_array_in[p]) / self.m_noise)
        return self.Last()


class CAMAOnRingBuffer(CArrayRing):
    """Kaufman's AMA (squared smoothing constant), on the ER above."""

    def __init__(self):
        super().__init__()
        self.m_er = CEROnRingBuffer()
        self.m_period = self.m_fast_period = self.m_slow_period = 0
        self.m_name = ""
        self.m_fc = self.m_sc = 0.0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, period: int = 10, fast_period: int = 2, slow_period: int = 30,
             size_buffer: int = 256, as_series: bool = False) -> bool:
        self.m_period = 10 if period <= 0 else int(period)
        self.m_fast_period = 2 if fast_period <= 0 else int(fast_period)
        self.m_slow_period = 30 if slow_period <= 0 else int(slow_period)
        sizebuffer = self.m_period if size_buffer < self.m_period else size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_er.Init(self.m_period, self.m_period + 1):
            return False
        self.m_name = f"AMA({self.m_period},{self.m_fast_period},{self.m_slow_period})"
        self.m_fc = 2.0 / (self.m_fast_period + 1.0)
        self.m_sc = 2.0 / (self.m_slow_period + 1.0)
        self.m_as_series = as_series
        m = 10
        self.m_bars_required = m * max(self.m_fast_period, self.m_slow_period) + self.m_period - 1
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.m_period

    def FastPeriod(self):
        return self.m_fast_period

    def SlowPeriod(self):
        return self.m_slow_period

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_begin = max(i, rates_total - self.Size() - self.m_bars_required)
            self.m_start = self.m_begin + self.m_period
            for i in range(self.m_begin, self.m_start):
                self.m_er.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            self.Update(array[self.m_start - 1], 1)
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        self.m_er.MainOnValue(rates_total, prev_calculated, self.m_begin, array[s], s)
        ssc = (self.m_er.Last() * (self.m_fc - self.m_sc)) + self.m_sc
        prev_ama = self.At(1)
        self.Last(ssc ** 2 * (array[s] - prev_ama) + prev_ama)
        for i in range(s + 1, rates_total):
            self.m_er.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            ssc = (self.m_er.Last() * (self.m_fc - self.m_sc)) + self.m_sc
            prev_ama = self.Last()
            self.Add(ssc ** 2 * (array[i] - prev_ama) + prev_ama)
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        self.m_er.MainOnValue(rates_total, prev_calculated, begin, value, self.m_index)
        self.m_begin = begin + self.m_er.BarsRequired()
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.Update(self.m_er.m_array_in[1], 1)
            self.Update(self.m_er.m_array_in[0], 0)
        ssc = (self.m_er.Last() * (self.m_fc - self.m_sc)) + self.m_sc
        if prev_calculated - 1 == self.m_index:
            self.Last(ssc ** 2 * (value - self.At(1)) + self.At(1))
        else:
            self.Add(ssc ** 2 * (value - self.Last()) + self.Last())
        return self.Last()


# ============================================================== CMomentum


class CMomentumOnRingBuffer(CArrayRing):
    """MetaTrader's momentum: 100 · price / price[period]."""

    def __init__(self):
        super().__init__()
        self.m_value_in = CArrayRing()
        self.m_name = ""
        self.m_period = 0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, period: int = 14, size_buffer: int = 256, as_series: bool = False) -> bool:
        self.m_period = 14 if period < 0 else int(period)
        sizebuffer = period if size_buffer < period else size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_value_in.Init(self.m_period + 1):
            return False
        self.m_as_series = as_series
        self.m_bars_required = self.m_period + 1
        self.m_name = f"Momentum({self.m_period})"
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.m_period

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        p = self.m_period
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_start = max(i, rates_total - self.Size() - self.m_bars_required) + p
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        self.Last(array[s] * 100.0 / array[s - p] if array[s - p] != 0 else EMPTY_VALUE)
        j = s + 1 - p
        for i in range(s + 1, rates_total):
            self.Add(array[i] * 100.0 / array[j] if array[j] != 0 else EMPTY_VALUE)
            j += 1
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        p = self.m_period
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if prev_calculated - 1 == self.m_index:
            self.m_value_in.Last(value)
        else:
            self.m_value_in.Add(value)
        if self.m_index < begin + p:
            return EMPTY_VALUE
        old = self.m_value_in[p]
        v = value * 100.0 / old if old != 0 else EMPTY_VALUE
        if prev_calculated - 1 == self.m_index:
            self.Last(v)
        else:
            self.Add(v)
        return self.Last()


# ======================================================== CRSI / CMFI


def _rsi_from(pma, nma):
    if pma == EMPTY_VALUE or nma == EMPTY_VALUE:
        return EMPTY_VALUE
    if nma != 0:
        return 100.0 - 100.0 / (1 + pma / nma)
    if pma != 0.0:
        return 100.0
    return 50.0


class CRSIOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.m_pma = CMAOnRingBuffer()
        self.m_nma = CMAOnRingBuffer()
        self.m_name = ""
        self.m_prev_value = self.m_cur_value = 0.0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, period: int = 14, method: int = MODE_SMMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        sizebuffer = period if size_buffer < period else size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_pma.Init(period, method, sizebuffer):
            return False
        if not self.m_nma.Init(period, method, sizebuffer):
            return False
        self.m_name = f"RSI({self.Period()},{self.Method()})"
        self.m_as_series = as_series
        self.m_bars_required = self.m_pma.BarsRequired() + 1
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.m_pma.MAPeriod()

    def Method(self):
        return self.m_pma.MAMethod()

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_start = self.m_begin = max(i, rates_total - self.Size() - self.m_bars_required) + 1
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        diff = array[s] - array[s - 1]
        pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, diff if diff > 0 else 0, s)
        nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, -diff if diff < 0 else 0, s)
        self.Last(_rsi_from(pma, nma))
        for i in range(s + 1, rates_total):
            diff = array[i] - array[i - 1]
            pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, diff if diff > 0 else 0, i)
            nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, -diff if diff < 0 else 0, i)
            self.Add(_rsi_from(pma, nma))
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_prev_value = value
            self.m_cur_value = value
            return EMPTY_VALUE
        if prev_calculated - 1 != self.m_index:
            self.m_prev_value = self.m_cur_value
        self.m_cur_value = value
        diff = value - self.m_prev_value
        pma = self.m_pma.MainOnValue(rates_total, prev_calculated, begin + 1, diff if diff > 0 else 0, self.m_index)
        nma = self.m_nma.MainOnValue(rates_total, prev_calculated, begin + 1, -diff if diff < 0 else 0, self.m_index)
        if prev_calculated - 1 == self.m_index:
            self.Last(_rsi_from(pma, nma))
        else:
            self.Add(_rsi_from(pma, nma))
        return self.Last()


class CMFIOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.m_pma = CMAOnRingBuffer()
        self.m_nma = CMAOnRingBuffer()
        self.m_name = ""
        self.m_prev_price = self.m_cur_price = 0.0
        self.m_applied_price = PRICE_TYPICAL
        self.m_applied_volume = VOLUME_TICK
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, period: int = 14, method: int = MODE_SMA, applied_price: int = PRICE_TYPICAL,
             applied_volume: int = VOLUME_TICK, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        sizebuffer = period if size_buffer < period else size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_pma.Init(period, method, sizebuffer):
            return False
        if not self.m_nma.Init(period, method, sizebuffer):
            return False
        self.m_name = f"MFI({self.Period()},{self.Method()})"
        self.m_applied_price = int(applied_price)
        self.m_applied_volume = int(applied_volume)
        self.m_as_series = as_series
        self.m_bars_required = self.m_pma.BarsRequired() + 1
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def Period(self):
        return self.m_pma.MAPeriod()

    def Method(self):
        return self.m_pma.MAMethod()

    def _price(self, open_, high, low, close):
        ap = self.m_applied_price
        if ap == PRICE_OPEN:
            return open_
        if ap == PRICE_CLOSE:
            return close
        if ap == PRICE_HIGH:
            return high
        if ap == PRICE_LOW:
            return low
        if ap == PRICE_MEDIAN:
            return (high + low) / 2.0
        if ap == PRICE_TYPICAL:
            return (high + low + close) / 3.0
        if ap == PRICE_WEIGHTED:
            return (high + low + close + close) / 4.0
        return EMPTY_VALUE

    def _volume(self, tick_volume, volume):
        if self.m_applied_volume == VOLUME_TICK:
            return float(tick_volume)
        if self.m_applied_volume == VOLUME_REAL:
            return float(volume)
        return EMPTY_VALUE

    def _flows(self, tick_volume, volume):
        vol = self._volume(tick_volume, volume)
        positive = self.m_cur_price * vol if self.m_cur_price > self.m_prev_price else 0
        negative = self.m_cur_price * vol if self.m_cur_price < self.m_prev_price else 0
        return positive, negative

    def MainOnArray(self, rates_total, prev_calculated, open_, high, low, close, tick_volume,
                    volume) -> int:
        if prev_calculated == 0:
            i = _first_valid(rates_total, open_, high, low, close)
            self.m_start = max(i, rates_total - self.Size() - self.m_bars_required)
            s = self.m_start
            self.m_prev_price = self.m_cur_price = self._price(open_[s], high[s], low[s], close[s])
            self.m_start = self.m_begin = self.m_start + 1
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        if prev_calculated - 1 != s:
            self.m_prev_price = self.m_cur_price
        self.m_cur_price = self._price(open_[s], high[s], low[s], close[s])
        positive, negative = self._flows(tick_volume[s], volume[s])
        pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, positive, s)
        nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, negative, s)
        self.Last(_rsi_from(pma, nma))
        for i in range(s + 1, rates_total):
            self.m_prev_price = self.m_cur_price
            self.m_cur_price = self._price(open_[i], high[i], low[i], close[i])
            positive, negative = self._flows(tick_volume[i], volume[i])
            pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, positive, i)
            nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, negative, i)
            self.Add(_rsi_from(pma, nma))
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, open_, high, low, close,
                    tick_volume, volume, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_prev_price = self.m_cur_price = self._price(open_, high, low, close)
            return EMPTY_VALUE
        if prev_calculated - 1 != self.m_index:
            self.m_prev_price = self.m_cur_price
        self.m_cur_price = self._price(open_, high, low, close)
        positive, negative = self._flows(tick_volume, volume)
        pma = self.m_pma.MainOnValue(rates_total, prev_calculated, begin + 1, positive, self.m_index)
        nma = self.m_nma.MainOnValue(rates_total, prev_calculated, begin + 1, negative, self.m_index)
        if prev_calculated - 1 == self.m_index:
            self.Last(_rsi_from(pma, nma))
        else:
            self.Add(_rsi_from(pma, nma))
        return self.Last()


# ========================================================= CMACD / COsMA


class CMACDOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.signal = CMAOnRingBuffer()
        self.m_fast = CMAOnRingBuffer()
        self.m_slow = CMAOnRingBuffer()
        self.m_name = self.m_name_main = self.m_name_signal = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9,
             fast_method: int = MODE_EMA, slow_method: int = MODE_EMA,
             signal_method: int = MODE_SMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        fastperiod = 12 if fast_period <= 0 else fast_period
        slowperiod = 26 if slow_period <= 0 else slow_period
        signalperiod = 9 if signal_period <= 0 else signal_period
        sizebuffer = max(fastperiod, max(slowperiod, signalperiod))
        if size_buffer >= sizebuffer:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_fast.Init(fastperiod, fast_method, sizebuffer):
            return False
        if not self.m_slow.Init(slowperiod, slow_method, sizebuffer):
            return False
        if not self.signal.Init(signalperiod, signal_method, sizebuffer):
            return False
        self.m_name = f"MACD({self.m_fast.Name()},{self.m_slow.Name()},{self.signal.Name()})"
        self.m_name_main = f"Main({self.m_fast.Name()},{self.m_slow.Name()})"
        self.m_name_signal = f"Signal({self.signal.Name()})"
        self.m_as_series = as_series
        self.m_bars_required = (max(self.m_fast.BarsRequired(), self.m_slow.BarsRequired())
                                + self.signal.BarsRequired() - 1)
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def NameMain(self):
        return self.m_name_main

    def NameSignal(self):
        return self.m_name_signal

    def FastMethod(self):
        return self.m_fast.MAMethod()

    def SlowMethod(self):
        return self.m_slow.MAMethod()

    def SignalMethod(self):
        return self.signal.MAMethod()

    def FastPeriod(self):
        return self.m_fast.MAPeriod()

    def SlowPeriod(self):
        return self.m_slow.MAPeriod()

    def SignalPeriod(self):
        return self.signal.MAPeriod()

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        if prev_calculated == 0:
            i = _first_valid(rates_total, array)
            self.m_start = self.m_begin = max(i, rates_total - self.Size() - self.m_bars_required)
        else:
            self.m_start = prev_calculated - 1
        s = self.m_start
        self.m_fast.MainOnValue(rates_total, prev_calculated, self.m_begin, array[s], s)
        self.m_slow.MainOnValue(rates_total, prev_calculated, self.m_begin, array[s], s)
        self.Last(self.m_fast.Last() - self.m_slow.Last())
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.Last(), s)
        for i in range(s + 1, rates_total):
            self.m_fast.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            self.m_slow.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            self.Add(self.m_fast.Last() - self.m_slow.Last())
            self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.Last(), i)
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        # sic: the member m_begin, not the argument.
        self.m_fast.MainOnValue(rates_total, prev_calculated, self.m_begin, value, self.m_index)
        self.m_slow.MainOnValue(rates_total, prev_calculated, self.m_begin, value, self.m_index)
        if prev_calculated - 1 == self.m_index:
            self.Last(self.m_fast.Last() - self.m_slow.Last())
        else:
            self.Add(self.m_fast.Last() - self.m_slow.Last())
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.Last(), self.m_index)
        return self.Last()


class COsMAOnRingBuffer(CArrayRing):
    def __init__(self):
        super().__init__()
        self.m_macd = CMACDOnRingBuffer()
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9,
             fast_method: int = MODE_EMA, slow_method: int = MODE_EMA,
             signal_method: int = MODE_SMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        fastperiod = 12 if fast_period <= 0 else fast_period
        slowperiod = 26 if slow_period <= 0 else slow_period
        signalperiod = 9 if signal_period <= 0 else signal_period
        sizebuffer = max(fastperiod, max(slowperiod, signalperiod))
        if size_buffer >= sizebuffer:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        # sic: the source passes the unchecked signal_period here.
        if not self.m_macd.Init(fastperiod, slowperiod, signal_period, fast_method, slow_method,
                                signal_method, sizebuffer):
            return False
        self.m_name = f"OsMA({self.m_macd.Name()})"
        self.m_as_series = as_series
        self.m_bars_required = self.m_macd.BarsRequired()
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def MainOnArray(self, rates_total, prev_calculated, array) -> int:
        self.m_macd.MainOnArray(rates_total, prev_calculated, array)
        if prev_calculated == 0:
            i = self.Size()
            while True:
                i -= 1
                if i <= 0:
                    break
                if self.m_macd[i] != 0 and self.m_macd[i] != EMPTY_VALUE:
                    break
            self.m_start = i
        else:
            self.m_start = rates_total - prev_calculated
        self.Last(self.m_macd[self.m_start] - self.m_macd.signal[self.m_start])
        for i in range(self.m_start - 1, -1, -1):
            self.Add(self.m_macd[i] - self.m_macd.signal[i])
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, value, index) -> float:
        self.m_macd.MainOnValue(rates_total, prev_calculated, begin, value, index)
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if prev_calculated - 1 == self.m_index:
            self.Last(self.m_macd.Last() - self.m_macd.signal.Last())
        else:
            self.Add(self.m_macd.Last() - self.m_macd.signal.Last())
        return self.Last()


# ================================================================ CATR


class CATROnRingBuffer:
    def __init__(self):
        self.m_ma = CMAOnRingBuffer()
        self.m_tr = self.m_atr = 0.0
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0
        self.m_close = self.m_prev_close = 0.0

    def Init(self, ma_period: int = 14, ma_method: int = MODE_SMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        if not self.m_ma.Init(ma_period, ma_method, size_buffer):
            return False
        self.m_as_series = as_series
        self.m_bars_required = self.m_ma.BarsRequired() + 1
        self.m_name = f"ATR({ma_period},{self.MAMethod()})"
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def MAMethod(self):
        return self.m_ma.MAMethod()

    def MAPeriod(self):
        return self.m_ma.MAPeriod()

    def Size(self):
        return self.m_ma.Size()

    def __getitem__(self, index):
        return self.m_ma.At(index)

    def MainOnArray(self, rates_total, prev_calculated, high, low, close) -> int:
        if prev_calculated == 0:
            for i in range(rates_total):
                if all(a[i] != 0 and a[i] != EMPTY_VALUE for a in (high, low, close)):
                    self.m_start = max(i + 1, rates_total - self.Size() - self.m_bars_required)
                    break
            self.m_begin = self.m_start
        else:
            self.m_start = prev_calculated - 1
        for i in range(self.m_start, rates_total):
            self.m_tr = max(high[i], close[i - 1]) - min(low[i], close[i - 1])
            self.m_ma.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_tr, i)
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, high, low, close, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_close = close
            return EMPTY_VALUE
        if prev_calculated - 1 != self.m_index:
            self.m_prev_close = close            # sic: the current close
        self.m_close = close
        self.m_tr = max(high, self.m_prev_close) - min(low, self.m_prev_close)
        self.m_ma.MainOnValue(rates_total, prev_calculated, begin + 1, self.m_tr, self.m_index)
        return self.m_ma.Last()


# ================================================================ CADX


class CADXOnRingBuffer:
    def __init__(self):
        self.pdi = CMAOnRingBuffer()
        self.ndi = CMAOnRingBuffer()
        self.m_adx = CMAOnRingBuffer()
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0
        self.m_high = self.m_low = self.m_close = 0.0
        self.m_phigh = self.m_plow = self.m_pclose = 0.0
        self.m_PD = self.m_ND = 0.0

    def Init(self, ma_period: int = 14, ma_method: int = MODE_EMA, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        if not self.pdi.Init(ma_period, ma_method, size_buffer):
            return False
        if not self.ndi.Init(ma_period, ma_method, size_buffer):
            return False
        if not self.m_adx.Init(ma_period, ma_method, size_buffer):
            return False
        self.m_name = f"({ma_period},{self.MAMethod()})"
        self.m_as_series = as_series
        self.m_bars_required = self.m_adx.BarsRequired() + 1
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def NameADX(self):
        return "ADX" + self.m_name

    def NameNDI(self):
        return "-DI" + self.m_name

    def NamePDI(self):
        return "+DI" + self.m_name

    def MAMethod(self):
        return self.m_adx.MAMethod()

    def MAPeriod(self):
        return self.m_adx.MAPeriod()

    def Size(self):
        return self.m_adx.Size()

    def __getitem__(self, index):
        return self.m_adx.At(index)

    def MainOnArray(self, rates_total, prev_calculated, high, low, close) -> int:
        if prev_calculated == 0:
            for i in range(rates_total):
                if all(a[i] != 0 and a[i] != EMPTY_VALUE for a in (high, low, close)):
                    self.m_start = max(i + 1, rates_total - self.Size() - self.m_bars_required)
                    break
            self.m_begin = self.m_start
        else:
            self.m_start = prev_calculated - 1
        for idx in range(self.m_start, rates_total):
            self.m_index = idx
            self.m_phigh = high[idx - 1]
            self.m_plow = low[idx - 1]
            self.m_pclose = close[idx - 1]
            self.m_high = high[idx]
            self.m_low = low[idx]
            self._adx(rates_total, prev_calculated)
        self.m_index = rates_total
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, high, low, close, index) -> float:
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_high = high
            self.m_low = low
            self.m_close = close
            self.m_begin = begin + 1
            return EMPTY_VALUE
        if prev_calculated - 1 != self.m_index:
            self.m_phigh = self.m_high
            self.m_plow = self.m_low
            self.m_pclose = self.m_close
        self.m_high = high
        self.m_low = low
        self.m_close = close
        self._adx(rates_total, prev_calculated)
        return self.m_adx.Last()

    def _adx(self, rates_total, prev_calculated):
        dTmpP = self.m_high - self.m_phigh
        dTmpN = self.m_plow - self.m_low
        if dTmpP < 0.0:
            dTmpP = 0.0
        if dTmpN < 0.0:
            dTmpN = 0.0
        if dTmpP > dTmpN:
            dTmpN = 0.0
        elif dTmpP < dTmpN:
            dTmpP = 0.0
        else:
            dTmpP = 0.0
            dTmpN = 0.0
        tr = max(max(abs(self.m_high - self.m_low), abs(self.m_high - self.m_pclose)),
                 abs(self.m_low - self.m_pclose))
        if tr != 0.0:
            self.m_PD = 100.0 * dTmpP / tr
            self.m_ND = 100.0 * dTmpN / tr
        else:
            self.m_PD = 0.0
            self.m_ND = 0.0
        self.pdi.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_PD, self.m_index)
        self.ndi.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_ND, self.m_index)
        dTmp = self.pdi.Last() + self.ndi.Last()
        if dTmp != 0.0:
            dTmp = 100.0 * abs((self.pdi.Last() - self.ndi.Last()) / dTmp)
        else:
            dTmp = 0.0
        self.m_adx.MainOnValue(rates_total, prev_calculated, self.m_begin, dTmp, self.m_index)


# ========================================================== CStochastic


class CStochasticOnRingBuffer:
    """Stochastic %K slowed by summing ``period_s`` bars of (close−min) and
    (max−min), with a %D signal average."""

    def __init__(self):
        self.signal = CMAOnRingBuffer()
        self.m_main = CArrayRing()
        self.m_max = CArrayRing()
        self.m_min = CArrayRing()
        self.m_close = CArrayRing()
        self.m_high = CArrayRing()
        self.m_low = CArrayRing()
        self.m_period_k = self.m_period_d = self.m_period_s = 0
        self.m_sumlow = self.m_sumhigh = 0.0
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, period_k: int = 5, period_d: int = 3, period_s: int = 3,
             method: int = MODE_SMA, size_buffer: int = 256, as_series: bool = False) -> bool:
        self.m_period_k = 5 if period_k <= 0 else int(period_k)
        self.m_period_d = 3 if period_d <= 0 else int(period_d)
        self.m_period_s = 3 if period_s <= 0 else int(period_s)
        sizebuffer = max(self.m_period_k, max(self.m_period_d, self.m_period_s))
        if size_buffer >= sizebuffer:
            sizebuffer = size_buffer
        for ring, size in ((self.m_max, self.m_period_s + 1), (self.m_min, self.m_period_s + 1),
                           (self.m_close, self.m_period_k + 1), (self.m_high, self.m_period_k + 1),
                           (self.m_low, self.m_period_k + 1), (self.m_main, sizebuffer)):
            if not ring.Init(size):
                return False
        if not self.signal.Init(self.m_period_d, method, sizebuffer):
            return False
        self.m_name = f"Stoch({self.m_period_k},{self.signal.Name()},{self.m_period_s})"
        self.m_as_series = as_series
        self.m_bars_required = self.signal.BarsRequired() + self.m_period_k + self.m_period_s - 2
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return "Main" + self.m_name

    def NameSignal(self):
        return "Signal" + self.m_name

    def Method(self):
        return self.signal.MAMethod()

    def PeriodK(self):
        return self.m_period_k

    def PeriodS(self):
        return self.m_period_s

    def PeriodD(self):
        return self.m_period_d

    def Size(self):
        return self.m_main.Size()

    def __getitem__(self, index):
        return self.m_main.At(index)

    def _max(self):
        mx = -DBL_MAX
        for i in range(self.m_period_k):
            mx = max(mx, self.m_high[i])
        return mx

    def _min(self):
        mn = DBL_MAX
        for i in range(self.m_period_k):
            mn = min(mn, self.m_low[i])
        return mn

    def MainOnArray(self, rates_total, prev_calculated, high, low, close) -> int:
        k, s_ = self.m_period_k, self.m_period_s
        if prev_calculated == 0:
            for i in range(rates_total):
                if all(a[i] != 0 and a[i] != EMPTY_VALUE for a in (high, low, close)):
                    self.m_start = max(i + 1, rates_total - self.Size() - self.m_bars_required)
                    break
            self.m_sumlow = 0.0
            self.m_sumhigh = 0.0
            self.m_start += k - 1
            for i in range(self.m_start, self.m_start + s_):
                self.m_max.Add(high[_array_maximum(high, i - k + 1, k)])
                self.m_min.Add(low[_array_minimum(low, i - k + 1, k)])
                self.m_close.Add(close[i])
                self.m_sumlow += close[i] - self.m_min.Last()
                self.m_sumhigh += self.m_max.Last() - self.m_min.Last()
            self.m_start = self.m_begin = self.m_start + s_ - 1
        else:
            self.m_start = prev_calculated - 1
        st = self.m_start
        self.m_sumlow -= self.m_close.Last() - self.m_min.Last()
        self.m_sumhigh -= self.m_max.Last() - self.m_min.Last()
        self.m_max.Last(high[_array_maximum(high, st - k + 1, k)])
        self.m_min.Last(low[_array_minimum(low, st - k + 1, k)])
        self.m_close.Last(close[st])
        self.m_sumlow += close[st] - self.m_min.Last()
        self.m_sumhigh += self.m_max.Last() - self.m_min.Last()
        self.m_main.Last(100.0 if self.m_sumhigh == 0.0 else self.m_sumlow / self.m_sumhigh * 100.0)
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_main.Last(), st)
        for idx in range(st + 1, rates_total):
            self.m_index = idx
            self.m_max.Add(high[_array_maximum(high, idx - k + 1, k)])
            self.m_min.Add(low[_array_minimum(low, idx - k + 1, k)])
            self.m_close.Add(close[idx])
            self.m_sumlow += close[idx] - self.m_min.Last() - close[idx - s_] + self.m_min[s_]
            self.m_sumhigh += self.m_max.Last() - self.m_min.Last() - self.m_max[s_] + self.m_min[s_]
            self.m_main.Add(100.0 if self.m_sumhigh == 0.0 else self.m_sumlow / self.m_sumhigh * 100.0)
            self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_main.Last(), idx)
        return rates_total

    def MainOnValue(self, rates_total, prev_calculated, begin, high, low, close, index) -> float:
        s_ = self.m_period_s
        self.m_index = rates_total - 1 - index if self.m_as_series else index
        if self.m_index < begin:
            return EMPTY_VALUE
        self.m_begin = begin + self.m_period_k - 1
        if self.m_index < self.m_begin:
            self.m_high.Add(high)
            self.m_low.Add(low)
            self.m_close.Add(close)
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.m_sumlow = 0.0
            self.m_sumhigh = 0.0
        self.m_begin += s_
        if self.m_index < self.m_begin:
            self.m_high.Add(high)
            self.m_low.Add(low)
            self.m_close.Add(close)
            self.m_max.Add(self._max())
            self.m_min.Add(self._min())
            self.m_sumlow += close - self.m_min.Last()
            self.m_sumhigh += self.m_max.Last() - self.m_min.Last()
            return EMPTY_VALUE
        if prev_calculated - 1 == self.m_index:
            self.m_sumlow -= self.m_close.Last() - self.m_min.Last()
            self.m_sumhigh -= self.m_max.Last() - self.m_min.Last()
            self.m_high.Last(high)
            self.m_low.Last(low)
            self.m_close.Last(close)
            self.m_max.Last(self._max())
            self.m_min.Last(self._min())
            self.m_sumlow += close - self.m_min.Last()
            self.m_sumhigh += self.m_max.Last() - self.m_min.Last()
            self.m_main.Last(100.0 if self.m_sumhigh == 0.0 else self.m_sumlow / self.m_sumhigh * 100.0)
        else:
            self.m_high.Add(high)
            self.m_low.Add(low)
            self.m_close.Add(close)
            self.m_max.Add(self._max())
            self.m_min.Add(self._min())
            self.m_sumlow += close - self.m_min.Last() - self.m_close[s_] + self.m_min[s_]
            self.m_sumhigh += self.m_max.Last() - self.m_min.Last() - self.m_max[s_] + self.m_min[s_]
            self.m_main.Add(100.0 if self.m_sumhigh == 0.0 else self.m_sumlow / self.m_sumhigh * 100.0)
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_main.Last(), self.m_index)
        return self.m_main.Last()


# =========================================================== CFractals


class CFractalsOnRingBuffer:
    """Bill Williams fractals with configurable left/right bar counts. The
    ``upper``/``lower`` rings hold the fractal value at its own bar
    (``m_bars_right`` bars before the newest), EMPTY_VALUE elsewhere."""

    def __init__(self):
        self.upper = CArrayRing()
        self.lower = CArrayRing()
        self.m_high_in = CArrayRing()
        self.m_low_in = CArrayRing()
        self.m_name = ""
        self.m_bars_right = self.m_bars_left = self.m_bars_total = 0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = self.m_start = self.m_index = 0

    def Init(self, bars_right: int = 2, bars_left: int = 2, size_buffer: int = 256,
             as_series: bool = False) -> bool:
        self.m_bars_right = 1 if bars_right < 1 else int(bars_right)
        self.m_bars_left = 1 if bars_left < 1 else int(bars_left)
        self.m_bars_total = self.m_bars_right + self.m_bars_left + 1
        sizebuffer = self.m_bars_total + 1
        if size_buffer >= sizebuffer:
            sizebuffer = size_buffer
        for ring in (self.upper, self.lower, self.m_high_in, self.m_low_in):
            if not ring.Init(sizebuffer):
                return False
        self.m_name = f"Fractals({self.m_bars_left},{self.m_bars_right})"
        self.m_as_series = as_series
        self.m_bars_required = self.m_bars_total
        return True

    def BarsRequired(self):
        return self.m_bars_required

    def Name(self):
        return self.m_name

    def NameUpper(self):
        return "Upper " + self.m_name

    def NameLower(self):
        return "Lower " + self.m_name

    def BarsRight(self):
        return self.m_bars_right

    def BarsLeft(self):
        return self.m_bars_left

    def Size(self):
        return self.upper.Size()

    def MainOnArray(self, rates_total, prev_calculated, high, low) -> int:
        # The source works on series-ordered views (index 0 = newest).
        h = list(high)[::-1]
        l = list(low)[::-1]
        total = self.m_bars_total
        right = self.m_bars_right
        if prev_calculated == 0:
            i = rates_total
            while True:
                i -= 1
                if i < 0:
                    break
                if h[i] != 0 and h[i] != EMPTY_VALUE and l[i] != 0 and l[i] != EMPTY_VALUE:
                    break
            self.m_start = min(i, self.upper.Size() + self.m_bars_required)
            self.m_start -= total
        else:
            self.m_start = rates_total - (prev_calculated - 1)
        self.m_index = self.m_start + right
        if _array_maximum(h, self.m_start, total) == self.m_index:
            self.upper.Update(h[self.m_index], right)
        else:
            self.upper.Update(EMPTY_VALUE, right)
        if _array_minimum(l, self.m_start, total) == self.m_index:
            self.lower.Update(l[self.m_index], right)
        else:
            self.lower.Update(EMPTY_VALUE, right)
        for i in range(self.m_start - 1, -1, -1):
            self.m_index -= 1
            self.upper.Add(EMPTY_VALUE)
            if _array_maximum(h, i, total) == self.m_index:
                self.upper.Update(h[self.m_index], right)
            else:
                self.upper.Update(EMPTY_VALUE, right)
            self.lower.Add(EMPTY_VALUE)
            if _array_minimum(l, i, total) == self.m_index:
                self.lower.Update(l[self.m_index], right)
            else:
                self.lower.Update(EMPTY_VALUE, right)
        return rates_total

    def _on(self, rates_total, prev_calculated, begin, value, index, ring_in, out, better):
        if self.m_as_series:
            self.m_begin = rates_total - 1 - begin
            self.m_index = rates_total - 1 - index
        else:
            self.m_begin = begin
            self.m_index = index
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if prev_calculated - 1 == self.m_index:
            ring_in.Last(value)
        else:
            ring_in.Add(value)
        if self.m_index < self.m_begin + self.m_bars_required:
            return EMPTY_VALUE
        if prev_calculated - 1 != self.m_index:
            out.Add(EMPTY_VALUE)
        best = 0
        for i in range(1, self.m_bars_total):
            if better(ring_in[i], ring_in[best]):
                best = i
        if best == self.m_bars_right:
            out.Update(ring_in[best], self.m_bars_right)
        else:
            out.Update(EMPTY_VALUE, self.m_bars_right)
        return out.At(self.m_bars_right)

    def MainOnHigh(self, rates_total, prev_calculated, begin, high, index) -> float:
        return self._on(rates_total, prev_calculated, begin, high, index, self.m_high_in,
                        self.upper, lambda a, b: b < a)

    def MainOnLow(self, rates_total, prev_calculated, begin, low, index) -> float:
        return self._on(rates_total, prev_calculated, begin, low, index, self.m_low_in,
                        self.lower, lambda a, b: b > a)
