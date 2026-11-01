"""MQL5 runtime — technical indicator handles.

``iMA``, ``iWPR``, ``iStochastic``, ``iRVI``, ``iChaikin`` and ``iBWMFI`` are
computed here with MetaTrader's algorithms. The other built-ins (``iRSI``,
``iATR``, ``iBands``, ``iMACD``, ``iADX``, ...) run the MetaQuotes example
indicators from the codebase (converted like any other indicator), so their
values are those of the terminal's own sources. ``iCustom`` runs another
converted indicator by name.
"""

from __future__ import annotations

from . import rt_term as T
from .rt_core import EMPTY_VALUE, MqlRuntimeError

# builtin -> (example source stem, folder, input order builder)
EXAMPLES = {
    "ATR": ("atr", "Average True Range (ATR)"),
    "RSI": ("rsi", "Relative Strength Index (RSI)"),
    "BANDS": ("bb", "Bollinger Bands ®"),
    "MACD": ("macd", "MACD"),
    "OSMA": ("osma", "Moving Average of Oscillator (OsMA)"),
    "CCI": ("cci", "Commodity Channel Index (CCI)"),
    "ADX": ("adx", "Average Directional Movement Index (ADX)"),
    "ADXW": ("adxw", "Average Directional Movement Index Wilder"),
    "SAR": ("parabolicsar", "Parabolic SAR"),
    "MOMENTUM": ("momentum", "Momentum"),
    "DEMARKER": ("demarker", "DeMarker (DeM)"),
    "MFI": ("mfi", "Money Flow Index (MFI)"),
    "TRIX": ("trix", "Triple Exponential Average (TRIX)"),
    "BEARS": ("bears", "Bears Power"),
    "BULLS": ("bulls", "Bulls Power"),
    "FORCE": ("force_index", "Force Index  (FRC)"),
    "AO": ("awesome_oscillator", "Awesome Oscillator (AO)"),
    "AC": ("accelerator", "Accelerator Oscillator (AC)"),
    "ALLIGATOR": ("alligator", "Alligator"),
    "GATOR": ("gator", "Gator Oscillator"),
    "ENVELOPES": ("envelopes", "Envelopes"),
    "FRACTALS": ("fractals", "Fractals"),
    "ICHIMOKU": ("ichimoku", "Ichimoku Kinko Hyo"),
    "OBV": ("obv", "On Balance Volume (OBV)"),
    "AD": ("ad", "Accumulation_Distribution"),
    "VOLUMES": ("volumes", "Volumes"),
    "DEMA": ("dema", "Double Exponential Moving Average (DEMA)"),
    "TEMA": ("tema", "Triple Exponential Moving Average (TEMA)"),
    "FRAMA": ("frama", "Fractal Adaptive Moving Average (FrAMA)"),
    "AMA": ("ama", "Adaptive Moving Average (AMA)"),
    "VIDYA": ("vidya", "Variable Index Dynamic Average (VIDYA)"),
    "STDDEV": ("stddev", "Standard Deviation (StdDev)"),
}


def _series_for(h):
    s = T.ctx().market.series(h.symbol, h.tf)
    if s is None:
        raise MqlRuntimeError("no history for " + h.symbol)
    return s


def _price_of(h, applied):
    s = _series_for(h)
    a = int(applied) if applied is not None else 1
    if a >= 10:
        sub = T._handle(a)
        if sub is not None:
            bufs, n = sub.data()
            return list(bufs.get(0, [0.0] * s.n)), s
    from .indicator import _applied
    return _applied(s, a), s


# ---------------------------------------------------------------- native MA

def ma_on(price: list, period: int, method: int, begin: int = 0) -> list:
    """MetaTrader's MA (Custom Moving Average.mq5 / MovingAverages.mqh), zeros before it starts."""
    n = len(price)
    out = [0.0] * n
    period = max(int(period), 1)
    method = int(method)
    if n == 0:
        return out
    if method == 1:   # EMA
        if begin >= n:
            return out
        k = 2.0 / (period + 1.0)
        out[begin] = price[begin]
        for i in range(begin + 1, n):
            out[i] = price[i] * k + out[i - 1] * (1.0 - k)
        return out
    start = begin + period - 1
    if start >= n:
        return out
    if method == 2:   # SMMA
        s = sum(price[begin:start + 1])
        out[start] = s / period
        for i in range(start + 1, n):
            out[i] = (out[i - 1] * (period - 1) + price[i]) / period
        return out
    if method == 3:   # LWMA
        wsum = period * (period + 1) / 2.0
        for i in range(start, n):
            acc = 0.0
            for j in range(period):
                acc += (period - j) * price[i - j]
            out[i] = acc / wsum
        return out
    # SMA
    s = sum(price[begin:start + 1])
    out[start] = s / period
    for i in range(start + 1, n):
        s += price[i] - price[i - period]
        out[i] = s / period
    return out


def _shifted(vals, shift):
    shift = int(shift)
    if not shift:
        return vals
    n = len(vals)
    out = [EMPTY_VALUE] * n
    if shift > 0:
        out[shift:] = vals[:n - shift]
    else:
        out[:n + shift] = vals[-shift:]
    return out


def _native(kind, symbol, tf, fn):
    h = T.Handle(kind, T._sym(symbol), T._tf(tf), (), lambda hh: fn(hh))
    return T._register(h)


def iMA(symbol, tf, period, ma_shift, method, applied):
    def run(h):
        price, s = _price_of(h, applied)
        return {0: _shifted(ma_on(price, period, method), ma_shift)}, s.n
    return _native("MA", symbol, tf, run)


def iWPR(symbol, tf, period):
    def run(h):
        s = _series_for(h)
        n = s.n
        p = max(int(period), 1)
        out = [0.0] * n
        for i in range(p - 1, n):
            hh = max(s.high[i - p + 1:i + 1])
            ll = min(s.low[i - p + 1:i + 1])
            out[i] = -(hh - s.close[i]) * 100.0 / (hh - ll) if hh != ll else (out[i - 1] if i else 0.0)
        return {0: out}, n
    return _native("WPR", symbol, tf, run)


def iStochastic(symbol, tf, k_period, d_period, slowing, method=0, price_field=0):
    def run(h):
        s = _series_for(h)
        n = s.n
        kp, dp, sl = max(int(k_period), 1), max(int(d_period), 1), max(int(slowing), 1)
        if int(price_field) == 1:
            hi_src = lo_src = s.close
        else:
            hi_src, lo_src = s.high, s.low
        hh = [0.0] * n
        ll = [0.0] * n
        for i in range(kp - 1, n):
            hh[i] = max(hi_src[i - kp + 1:i + 1])
            ll[i] = min(lo_src[i - kp + 1:i + 1])
        main = [0.0] * n
        start = kp - 1 + sl - 1
        for i in range(start, n):
            sh = sum(s.close[i - j] - ll[i - j] for j in range(sl))
            sd = sum(hh[i - j] - ll[i - j] for j in range(sl))
            main[i] = 100.0 if sd == 0 else sh / sd * 100.0
        sig = ma_on(main, dp, method, begin=start)
        return {0: main, 1: sig}, n
    return _native("STOCHASTIC", symbol, tf, run)


def iRVI(symbol, tf, period):
    def run(h):
        s = _series_for(h)
        n = s.n
        p = max(int(period), 1)
        rvi = [0.0] * n
        sig = [0.0] * n
        o, hi, lo, c = s.open, s.high, s.low, s.close
        for i in range(p + 3, n):
            num = den = 0.0
            for j in range(i, i - p, -1):
                vn = ((c[j] - o[j]) + 2 * (c[j - 1] - o[j - 1]) + 2 * (c[j - 2] - o[j - 2]) + (c[j - 3] - o[j - 3])) / 6
                vd = ((hi[j] - lo[j]) + 2 * (hi[j - 1] - lo[j - 1]) + 2 * (hi[j - 2] - lo[j - 2]) + (hi[j - 3] - lo[j - 3])) / 6
                num += vn
                den += vd
            rvi[i] = num / den if den != 0 else num
        for i in range(p + 6, n):
            sig[i] = (rvi[i] + 2 * rvi[i - 1] + 2 * rvi[i - 2] + rvi[i - 3]) / 6
        return {0: rvi, 1: sig}, n
    return _native("RVI", symbol, tf, run)


def iChaikin(symbol, tf, fast, slow, method, volume):
    def run(h):
        s = _series_for(h)
        n = s.n
        vol = s.tick_volume if int(volume) == 0 else s.volume
        ad = [0.0] * n
        for i in range(n):
            rng = s.high[i] - s.low[i]
            v = 0.0 if rng == 0 else ((s.close[i] - s.low[i]) - (s.high[i] - s.close[i])) / rng * vol[i]
            ad[i] = v + (ad[i - 1] if i else 0.0)
        f = ma_on(ad, fast, method)
        sl = ma_on(ad, slow, method)
        return {0: [a - b for a, b in zip(f, sl)]}, n
    return _native("CHAIKIN", symbol, tf, run)


def iBWMFI(symbol, tf, volume=0):
    def run(h):
        s = _series_for(h)
        n = s.n
        vol = s.tick_volume if int(volume) == 0 else s.volume
        out = [0.0] * n
        col = [0.0] * n
        for i in range(n):
            out[i] = (s.high[i] - s.low[i]) / vol[i] / T.Point() if vol[i] else (out[i - 1] if i else 0.0)
            if i:
                up_m, up_v = out[i] > out[i - 1], vol[i] > vol[i - 1]
                col[i] = 0 if (up_m and up_v) else 1 if (not up_m and not up_v) else 2 if up_m else 3
        return {0: out, 1: col}, n
    return _native("BWMFI", symbol, tf, run)


# ---------------------------------------------------------------- example-backed

def _example(kind, symbol, tf, params, applied=None):
    from .indicator import custom_handle_runner, library_index, map_icustom_params
    stem, folder = EXAMPLES[kind]
    items = library_index().get(stem, [])
    it = next((x for x in items if x.get("folder") == folder), None)
    if it is None:
        raise MqlRuntimeError(f"built-in indicator i{kind.title()} needs the converted example '{folder}/{stem}'")
    inputs, extra = map_icustom_params(it["module"], list(params))
    runner = custom_handle_runner(it["module"], folder, inputs, applied)
    h = T.Handle(kind, T._sym(symbol), T._tf(tf), params, runner)
    return T._register(h)


def iATR(symbol, tf, period):
    return _example("ATR", symbol, tf, [period])


def iRSI(symbol, tf, period, applied):
    return _example("RSI", symbol, tf, [period], applied)


def iBands(symbol, tf, period, shift, deviation, applied):
    return _example("BANDS", symbol, tf, [period, shift, deviation], applied)


def iMACD(symbol, tf, fast, slow, signal, applied):
    if isinstance(applied, int) and applied >= 10:
        return _example("MACD", symbol, tf, [fast, slow, signal, 1], applied)
    return _example("MACD", symbol, tf, [fast, slow, signal, applied])


def iOsMA(symbol, tf, fast, slow, signal, applied):
    return _example("OSMA", symbol, tf, [fast, slow, signal, applied])


def iCCI(symbol, tf, period, applied):
    return _example("CCI", symbol, tf, [period], applied)


def iADX(symbol, tf, period):
    return _example("ADX", symbol, tf, [period])


def iADXWilder(symbol, tf, period):
    return _example("ADXW", symbol, tf, [period])


def iSAR(symbol, tf, step, maximum):
    return _example("SAR", symbol, tf, [step, maximum])


def iMomentum(symbol, tf, period, applied):
    return _example("MOMENTUM", symbol, tf, [period], applied)


def iDeMarker(symbol, tf, period):
    return _example("DEMARKER", symbol, tf, [period])


def iMFI(symbol, tf, period, volume):
    return _example("MFI", symbol, tf, [period, volume])


def iTriX(symbol, tf, period, applied):
    return _example("TRIX", symbol, tf, [period], applied)


def iBearsPower(symbol, tf, period):
    return _example("BEARS", symbol, tf, [period])


def iBullsPower(symbol, tf, period):
    return _example("BULLS", symbol, tf, [period])


def iForce(symbol, tf, period, method, volume):
    return _example("FORCE", symbol, tf, [period, method, 1, volume])


def iAO(symbol, tf):
    return _example("AO", symbol, tf, [])


def iAC(symbol, tf):
    return _example("AC", symbol, tf, [])


def iAlligator(symbol, tf, jp, js, tp, ts, lp, ls, method, applied):
    return _example("ALLIGATOR", symbol, tf, [jp, js, tp, ts, lp, ls, method, applied])


def iGator(symbol, tf, jp, js, tp, ts, lp, ls, method, applied):
    return _example("GATOR", symbol, tf, [jp, js, tp, ts, lp, ls, method, applied])


def iEnvelopes(symbol, tf, period, shift, method, applied, deviation):
    return _example("ENVELOPES", symbol, tf, [period, shift, method, applied, deviation])


def iFractals(symbol, tf):
    return _example("FRACTALS", symbol, tf, [])


def iIchimoku(symbol, tf, tenkan, kijun, senkou):
    return _example("ICHIMOKU", symbol, tf, [tenkan, kijun, senkou])


def iOBV(symbol, tf, volume):
    return _example("OBV", symbol, tf, [volume])


def iAD(symbol, tf, volume):
    return _example("AD", symbol, tf, [volume])


def iVolumes(symbol, tf, volume):
    return _example("VOLUMES", symbol, tf, [volume])


def iDEMA(symbol, tf, period, shift, applied):
    return _example("DEMA", symbol, tf, [period, shift], applied)


def iTEMA(symbol, tf, period, shift, applied):
    return _example("TEMA", symbol, tf, [period, shift], applied)


def iFrAMA(symbol, tf, period, shift, applied):
    return _example("FRAMA", symbol, tf, [period, shift], applied)


def iAMA(symbol, tf, period, fast, slow, shift, applied):
    return _example("AMA", symbol, tf, [period, fast, slow, shift], applied)


def iVIDyA(symbol, tf, cmo, ema, shift, applied):
    return _example("VIDYA", symbol, tf, [cmo, ema, shift], applied)


def iStdDev(symbol, tf, period, shift, method, applied):
    return _example("STDDEV", symbol, tf, [period, shift, method], applied)


def iCustom(symbol, tf, name, *params):
    from .indicator import custom_handle_runner, map_icustom_params, resolve_indicator
    c = T.ctx()
    it = resolve_indicator(name, getattr(c, "folder", ""))
    if it is None:
        T._set_error(4802)
        _ = name
        return -1
    inputs, applied = map_icustom_params(it["module"], list(params))
    runner = custom_handle_runner(it["module"], it.get("folder", ""), inputs, applied)
    h = T.Handle("CUSTOM", T._sym(symbol), T._tf(tf), params, runner)
    return T._register(h)


_IND_BY_TYPE = {
    "IND_MA": iMA, "IND_ATR": iATR, "IND_RSI": iRSI, "IND_BANDS": iBands, "IND_MACD": iMACD, "IND_OSMA": iOsMA,
    "IND_CCI": iCCI, "IND_ADX": iADX, "IND_ADXW": iADXWilder, "IND_SAR": iSAR, "IND_MOMENTUM": iMomentum,
    "IND_DEMARKER": iDeMarker, "IND_MFI": iMFI, "IND_TRIX": iTriX, "IND_BEARS": iBearsPower,
    "IND_BULLS": iBullsPower, "IND_FORCE": iForce, "IND_AO": iAO, "IND_AC": iAC, "IND_ALLIGATOR": iAlligator,
    "IND_GATOR": iGator, "IND_ENVELOPES": iEnvelopes, "IND_FRACTALS": iFractals, "IND_ICHIMOKU": iIchimoku,
    "IND_OBV": iOBV, "IND_AD": iAD, "IND_VOLUMES": iVolumes, "IND_DEMA": iDEMA, "IND_TEMA": iTEMA,
    "IND_FRAMA": iFrAMA, "IND_AMA": iAMA, "IND_VIDYA": iVIDyA, "IND_STDDEV": iStdDev, "IND_WPR": iWPR,
    "IND_STOCHASTIC": iStochastic, "IND_RVI": iRVI, "IND_CHAIKIN": iChaikin, "IND_BWMFI": iBWMFI,
}


def IndicatorCreate(symbol, tf, ind_type, count=0, params=None):
    from . import rt_consts
    name = next((k for k, v in rt_consts.CONSTS.items() if k.startswith("IND_") and v == ind_type), None)
    vals = []
    if params is not None:
        for p in list(params)[: int(count) if count else None]:
            t = getattr(p, "type", 0)
            if t == 14:
                vals.append(p.string_value)
            elif t in (12, 13):
                vals.append(p.double_value)
            else:
                vals.append(p.integer_value)
    if name == "IND_CUSTOM":
        return iCustom(symbol, tf, *(vals or [""]))
    fn = _IND_BY_TYPE.get(name)
    if fn is None:
        return -1
    try:
        return fn(symbol, tf, *vals)
    except TypeError:
        return -1
