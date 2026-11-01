"""Running converted MQL5 programs, and the :class:`MQL5Indicator` base class
the generated plugin files derive from.

Each calculation re-executes the converted module's code in a fresh
namespace, so global and static variables start from their initial values
exactly as when MetaTrader loads an indicator; then ``OnInit`` and
``OnCalculate`` (with ``prev_calculated = 0`` over all bars) run inside a
:class:`~.rt_term.Context`. The indicator buffers are read back, empty values
become NaN, and each plot is mapped to the app's draw styles.
"""

from __future__ import annotations

import builtins
import json
import os
import re
import sys
import threading

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Level, Pane, Plot

from . import rt_term as T
from .rt_core import DBL_MAX, Arr, MqlRuntimeError, color_to_hex

# ------------------------------------------------------------------ program cache

_code_cache: dict[str, tuple[float, object]] = {}
_lock = threading.RLock()


def _compiled(path: str):
    mt = os.path.getmtime(path)
    with _lock:
        ent = _code_cache.get(path)
        if ent and ent[0] == mt:
            return ent[1]
        src = open(path, encoding="utf-8").read()
        code = compile(src, path, "exec")
        _code_cache[path] = (mt, code)
        return code


def fresh_namespace(path: str, inputs: dict | None = None) -> dict:
    """Execute the module anew; ``inputs`` are applied before the globals are
    initialised (MQL5 initialises globals after the inputs are set)."""
    from . import runtime
    code = _compiled(path)
    ns = {"__name__": "mql5prog_" + re.sub(r"\W", "_", os.path.basename(path)[:-3]),
          "__file__": path, "__builtins__": builtins, "__mql5_fresh__": True}
    runtime._set_inputs(inputs)
    try:
        exec(code, ns)
    finally:
        runtime._set_inputs(None)
    return ns


# ------------------------------------------------------------------ library index (iCustom)

LIBRARY_DIRS: list[str] = []


def _default_library_dirs():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    dirs = [os.path.join(root, "python_indicators", "mql5_codebase")]
    if getattr(sys, "frozen", False):
        dirs.append(os.path.join(os.path.dirname(sys.executable), "python_indicators", "mql5_codebase"))
    return dirs


_index_cache: dict[str, tuple[float, dict]] = {}


def library_index() -> dict:
    """name (lower-case file stem) -> list of {module, source, folder}"""
    merged: dict[str, list] = {}
    for d in (LIBRARY_DIRS or _default_library_dirs()):
        p = os.path.join(d, "_index.json")
        if not os.path.isfile(p):
            continue
        mt = os.path.getmtime(p)
        ent = _index_cache.get(p)
        if not ent or ent[0] != mt:
            with open(p, encoding="utf-8") as fh:
                data = json.load(fh)
            ent = (mt, data)
            _index_cache[p] = ent
        for name, items in ent[1].items():
            for it in items:
                it = dict(it)
                it["module"] = os.path.join(d, it["module"])
                merged.setdefault(name, []).append(it)
    return merged


_LOOKALIKE = str.maketrans("асеорхкмтнвіу", "aceopxkmthbiy")


def resolve_indicator(name: str, caller_folder: str = "") -> dict | None:
    nm = str(name).replace("\\", "/").split("/")[-1]
    if nm.startswith("::"):
        nm = nm[2:]
    nm = re.sub(r"\.(ex5|mq5)$", "", nm, flags=re.I).strip().lower()
    idx = library_index()
    items = idx.get(nm)
    if not items:
        # Cyrillic look-alike letters typed into Latin names ('JССX'), then a
        # versioned file name ('CCI_withShift' -> 'cci_withshift_v1.01')
        alt = nm.translate(_LOOKALIKE)
        items = idx.get(alt)
        if not items:
            cands = sorted(k for k in idx if re.match(re.escape(alt) + r"[ _\-]?v?\d", k))
            items = idx.get(cands[0]) if cands else None
    if not items:
        return None
    for it in items:
        if caller_folder and it.get("folder") == caller_folder:
            return it
    return items[0]


# ------------------------------------------------------------------ running

class ProgramResult:
    def __init__(self, ctx, ns, ok, error, n):
        self.ctx = ctx
        self.ns = ns
        self.ok = ok
        self.error = error
        self.n = n

    def buffer(self, index) -> list | None:
        b = self.ctx.buffers.get(index)
        return list(b[0].a) if b else None


def _timeseries(values, n):
    a = Arr(0, 0.0, dyn=False)
    a.a = list(values)
    return a


def _applied(series: T.Series, price) -> list:
    o, h, l, c = series.open, series.high, series.low, series.close
    p = int(price) if price is not None else 1
    if p == 2:
        return list(o)
    if p == 3:
        return list(h)
    if p == 4:
        return list(l)
    if p == 5:
        return [(a + b) / 2.0 for a, b in zip(h, l)]
    if p == 6:
        return [(a + b + d) / 3.0 for a, b, d in zip(h, l, c)]
    if p == 7:
        return [(a + b + 2 * d) / 4.0 for a, b, d in zip(h, l, c)]
    return list(c)


def run_program(path: str, market: T.Market, symbol: str, period: int, inputs: dict | None = None,
                applied_price=1, calculate=True, name="", folder="", price_values=None, depth=0) -> ProgramResult:
    """Execute a converted program: OnInit, then OnCalculate over all bars."""
    ctx0 = T.Context(market, symbol, period, name=name)
    T.push_ctx(ctx0)      # globals may call terminal functions while initialising
    try:
        ns = fresh_namespace(path, inputs)
    finally:
        T.pop_ctx()
    meta = ns.get("MQL5_META", {})
    for k, v in (inputs or {}).items():
        ns[k] = v
    ctx = T.Context(market, symbol, period, name=name or meta.get("name", ""), program=meta)
    ctx.folder = folder or meta.get("folder", "")
    ctx.calc_depth = depth
    T.push_ctx(ctx)
    try:
        error = None
        ok = True
        n = 0
        try:
            oninit = ns.get("OnInit")
            rc = oninit() if oninit else 0
            if rc not in (None, 0, False) and rc is not True:
                ok = False
                error = f"OnInit returned {rc}"
        except MqlRuntimeError as e:
            ok, error = False, f"OnInit: {e}"
        if ok and calculate:
            s = ctx.series
            n = s.n if s is not None else 0
            ctx.rates_total = n
            for idx, (arr, _t) in ctx.buffers.items():
                if len(arr.a) != n:
                    arr.a = [0.0] * n
            oncalc = ns.get("OnCalculate")
            if oncalc is None:
                ok, error = False, "no OnCalculate"
            elif n > 0:
                short = meta.get("short_form", False)
                try:
                    for attempt in range(3):
                        if short:
                            vals = price_values if price_values is not None else _applied(s, applied_price)
                            ret = oncalc(n, 0, 0, _timeseries(vals, n))
                        else:
                            ret = oncalc(n, 0, _timeseries(s.time, n), _timeseries(s.open, n),
                                         _timeseries(s.high, n), _timeseries(s.low, n), _timeseries(s.close, n),
                                         _timeseries(s.tick_volume, n), _timeseries(s.volume, n),
                                         _timeseries(s.spread, n))
                        if ret:
                            break
                except MqlRuntimeError as e:
                    ok, error = False, f"OnCalculate: {e}"
                except ZeroDivisionError:
                    ok, error = False, "OnCalculate: zero divide"
        return ProgramResult(ctx, ns, ok, error, n)
    finally:
        T.pop_ctx()


# ------------------------------------------------------------------ handles: iCustom

_run_cache = threading.local()


def custom_handle_runner(path, folder, inputs, applied):
    def runner(h: T.Handle):
        c = T.ctx()
        if c.calc_depth > 6:
            raise MqlRuntimeError("iCustom nesting too deep")
        key = (path, tuple(sorted((k, repr(v)) for k, v in inputs.items())), h.symbol, h.tf, repr(applied))
        # results belong to one market (data set); keep them on it, not under id(), which Python reuses
        cache = getattr(c.market, "_icustom_cache", None)
        if cache is None:
            cache = {}
            try:
                c.market._icustom_cache = cache
            except AttributeError:
                pass
        if key in cache:
            return cache[key]
        price_values = None
        ap = 1
        if applied is not None:
            ap = applied
            sub = T._handle(applied) if isinstance(applied, int) and applied >= 10 else None
            if sub is not None:
                bufs, nn = sub.data()
                price_values = list(bufs.get(0, []))
        res = run_program(path, c.market, h.symbol, h.tf, inputs, applied_price=ap, folder=folder,
                          price_values=price_values, depth=c.calc_depth + 1)
        if not res.ok:
            h.error = res.error
            out = ({}, 0)
        else:
            out = ({i: list(a.a) for i, (a, _t) in res.ctx.buffers.items()}, res.n)
        if len(cache) > 64:
            cache.clear()
        cache[key] = out
        return out
    return runner


def program_inputs(path: str) -> list:
    ns = fresh_namespace(path)
    return ns.get("MQL5_META", {}).get("inputs", [])


def map_icustom_params(path: str, params: list) -> tuple[dict, object]:
    """Positional iCustom parameters -> {python input name: value}; extra trailing
    parameter = applied price / handle (short-form indicators)."""
    inputs = program_inputs(path)
    out = {}
    applied = None
    for i, val in enumerate(params):
        if i < len(inputs):
            out[inputs[i]["py"]] = _coerce(val, inputs[i]["type"])
        elif i == len(inputs):
            applied = val
    return out, applied


def _coerce(v, t):
    if t in ("double", "float"):
        try:
            return float(v)
        except (TypeError, ValueError):
            return v
    if t == "bool":
        return bool(v)
    if t == "string":
        return str(v) if v is not None else ""
    try:
        return int(v)
    except (TypeError, ValueError):
        return v


# ------------------------------------------------------------------ bar data from a DataFrame

def market_from_df(df, symbol=None):
    from backtester.indicators import mql5 as M
    s = T.Series.from_df(df)
    sym = symbol or df.attrs.get("symbol") or "EURUSD"
    period = df.attrs.get("mql5_period")
    if not period:
        if s.n >= 2:
            diffs = np.diff(np.asarray(s.time[: min(s.n, 500)], dtype=np.int64))
            diffs = diffs[diffs > 0]
            sec = float(np.min(diffs)) if len(diffs) else 3600.0
        else:
            sec = 3600.0
        period = T.seconds_to_tf(sec)
    spec = {"point": M.point(df), "digits": M.digits(df)}
    for k in ("tick_value", "tick_size", "contract_size", "volume_min", "volume_step", "volume_max",
              "description", "currency_profit", "currency_base"):
        if k in df.attrs:
            spec[k] = df.attrs[k]
    m = T.Market()
    m.add(sym, s, period, spec)
    return m, sym, period


def dummy_market():
    m = T.Market()
    m.add("EURUSD", T.Series([], [], [], [], [], [], [], []), T.PERIOD_H1, {"point": 0.00001, "digits": 5})
    return m


# ------------------------------------------------------------------ plots

ARROW_SYMBOLS = {233: "t1", 225: "t1", 241: "t1", 221: "t1", 217: "t1", 236: "t1", 200: "t1",
                 234: "t", 226: "t", 242: "t", 222: "t", 218: "t", 238: "t", 202: "t",
                 159: "o", 158: "o", 108: "o", 161: "o", 164: "o", 152: "o", 119: "d", 117: "d", 116: "d",
                 110: "s", 167: "s", 168: "s", 113: "s", 251: "x", 253: "x", 252: "+", 254: "+", 115: "d"}

BUFFERS_PER_TYPE = {0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 3, 12: 2,
                    13: 3, 14: 4, 15: 4, 16: 5, 17: 5}


def _prop(props, plot, key, default=None):
    d = props.get(plot, {})
    return d.get(key, default)


class PlotMap:
    """How one MT5 plot maps to the app: its buffers and the app Plots."""

    def __init__(self, index, draw_type, buffers, colors, label, width, dash, arrow, shift, begin, empty):
        self.index = index
        self.draw_type = draw_type
        self.buffers = buffers
        self.colors = colors
        self.label = label
        self.width = width
        self.dash = dash
        self.arrow = arrow
        self.shift = shift
        self.begin = begin
        self.empty = empty


def _hex_colors(cols):
    out = []
    for c in cols:
        h = color_to_hex(c)
        out.append(h)
    return out


def build_plot_maps(meta: dict, ctx) -> list[PlotMap]:
    props = meta.get("props", {})
    n_plots = int(props.get("indicator_plots", 0) or 0)
    data_bufs = sorted(i for i, (a, t) in ctx.buffers.items()) if ctx is not None else []
    plot_props = ctx.plot_props if ctx is not None else {}
    if not n_plots and data_bufs:
        n_plots = sum(1 for i in data_bufs if ctx.buffers[i][1] == 0)
    maps = []
    bi = 0
    for k in range(n_plots):
        pp = plot_props.get(k, {})
        dt = pp.get(("i", 3))
        if dt is None:
            dt = meta.get("types", {}).get(k + 1, 1)
        dt = int(dt)
        need = BUFFERS_PER_TYPE.get(dt, 1)
        bufs = data_bufs[bi:bi + need]
        bi += need
        cols = list(meta.get("colors", {}).get(k + 1, []))
        ncol = pp.get(("i", 8))
        if ncol:
            cols = (cols + [cols[-1] if cols else 0x0000FF] * int(ncol))[:max(int(ncol), 1)]
        if ("i", 9) in pp:
            if cols:
                cols[0] = pp[("i", 9)]
            else:
                cols = [pp[("i", 9)]]
        for key, val in pp.items():
            if key[0] == "i" and key[1] == 9 and len(key) == 3:
                j = key[2]
                while len(cols) <= j:
                    cols.append(cols[-1] if cols else 0)
                cols[j] = val
        label = pp.get(("s", 0)) or meta.get("labels", {}).get(k + 1, "") or f"Plot {k + 1}"
        width = pp.get(("i", 7)) or meta.get("widths", {}).get(k + 1, 1) or 1
        style = pp.get(("i", 6))
        if style is None:
            style = meta.get("styles", {}).get(k + 1, 0)
        arrow = pp.get(("i", 0), 159)
        shift = pp.get(("i", 5), 0) or 0
        begin = pp.get(("i", 2), 0) or 0
        empty = pp.get(("d", 0), DBL_MAX)
        maps.append(PlotMap(k, dt, bufs, cols, str(label), float(width), int(style or 0) != 0, int(arrow or 159),
                            int(shift), int(begin), empty))
    return maps


def _labels(label: str, n: int) -> list[str]:
    parts = [p.strip() for p in label.split(";")]
    while len(parts) < n:
        parts.append(parts[-1] if parts else "")
    return parts


def app_plots(maps: list[PlotMap]) -> list[Plot]:
    plots = []
    for m in maps:
        k = m.index
        cols = [c for c in _hex_colors(m.colors)]
        c0 = next((c for c in cols if c), "#f0a732")
        labs = _labels(m.label, max(len(m.buffers), 2))
        w = max(1.0, m.width)
        dt = m.draw_type
        if dt == 0:
            plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.NONE))
        elif dt in (1, 2):
            plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.LINE if dt == 1 else DrawStyle.SECTION,
                              color=c0, width=w, dash=m.dash))
        elif dt == 3:
            plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.HISTOGRAM, color=c0))
        elif dt == 5:
            plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.ARROW, color=c0,
                              symbol=ARROW_SYMBOLS.get(m.arrow, "o"), size=int(6 + 2 * w)))
        elif dt in (6, 13):
            plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.ZIGZAG, color=c0, width=w, fill_with=f"p{k}_b"))
        elif dt == 7:
            c1 = cols[1] if len(cols) > 1 and cols[1] else c0
            plots.append(Plot(f"p{k}_up", labs[0], style=DrawStyle.FILL, color=c0, fill_with=f"p{k}_upb"))
            plots.append(Plot(f"p{k}_dn", labs[1], style=DrawStyle.FILL, color=c1, fill_with=f"p{k}_dnb"))
        elif dt in (8, 9):
            for j, c in enumerate(cols or [c0]):
                if not c:
                    continue
                plots.append(Plot(f"p{k}_c{j}", f"{labs[0]}" + (f" [{j}]" if len(cols) > 1 else ""),
                                  style=DrawStyle.LINE if dt == 8 else DrawStyle.SECTION, color=c, width=w,
                                  dash=m.dash))
        elif dt == 10:
            for j, c in enumerate(cols or [c0]):
                if not c:
                    continue
                plots.append(Plot(f"p{k}_c{j}", f"{labs[0]}" + (f" [{j}]" if len(cols) > 1 else ""),
                                  style=DrawStyle.HISTOGRAM, color=c))
        elif dt in (4, 11):
            if dt == 4:
                plots.append(Plot(f"p{k}", labs[0], style=_HIST2, color=c0, fill_with=f"p{k}_b"))
            else:
                for j, c in enumerate(cols or [c0]):
                    if not c:
                        continue
                    plots.append(Plot(f"p{k}_c{j}", f"{labs[0]}" + (f" [{j}]" if len(cols) > 1 else ""),
                                      style=_HIST2, color=c, fill_with=f"p{k}_c{j}_b"))
        elif dt == 12:
            for j, c in enumerate(cols or [c0]):
                if not c:
                    continue
                plots.append(Plot(f"p{k}_c{j}", f"{labs[0]}" + (f" [{j}]" if len(cols) > 1 else ""),
                                  style=DrawStyle.ARROW, color=c, symbol=ARROW_SYMBOLS.get(m.arrow, "o"),
                                  size=int(6 + 2 * w)))
        elif dt in (14, 15, 16, 17):
            up = cols[0] if cols and cols[0] else "#26a69a"
            dn = cols[1] if len(cols) > 1 and cols[1] else (up if dt in (16, 17) else "#ef5350")
            if dt in (16, 17):
                plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.CANDLES,
                                  colors=tuple(c or "#808080" for c in (cols or [up])),
                                  color_key=f"p{k}_color"))
            else:
                plots.append(Plot(f"p{k}", labs[0], style=DrawStyle.CANDLES, colors=(up, dn)))
        else:
            plots.append(Plot(f"p{k}", labs[0], color=c0, width=w))
    return plots


_HIST2 = getattr(DrawStyle, "HISTOGRAM2", DrawStyle.HISTOGRAM)


def _shift(values: np.ndarray, bars: int) -> np.ndarray:
    if not bars:
        return values
    out = np.full(len(values), np.nan)
    if bars > 0:
        out[bars:] = values[:-bars]
    else:
        out[:bars] = values[-bars:]
    return out


def plot_arrays(maps: list[PlotMap], res: ProgramResult, n: int) -> dict:
    from backtester.indicators.mql5 import segments
    out = {}
    for m in maps:
        k = m.index
        raw = []
        for bi in m.buffers:
            vals = res.buffer(bi)
            arr = np.asarray(vals if vals is not None and len(vals) == n else [np.nan] * n, dtype=float)
            raw.append(arr)
        if not raw:
            continue

        def clean(a):
            a = a.copy()
            bad = ~np.isfinite(a) | (np.abs(a) >= DBL_MAX * 0.999)
            if m.empty is not None and m.empty != DBL_MAX:
                try:
                    bad |= a == float(m.empty)
                except (TypeError, ValueError):
                    pass
            a[bad] = np.nan
            if m.begin > 0:
                a[: min(m.begin, n)] = np.nan
            return _shift(a, m.shift)

        dt = m.draw_type
        if dt in (0, 1, 2, 3, 5):
            out[f"p{k}"] = clean(raw[0])
        elif dt in (6, 13):
            out[f"p{k}"] = clean(raw[0])
            out[f"p{k}_b"] = clean(raw[1]) if len(raw) > 1 else np.full(n, np.nan)
        elif dt == 7:
            a = clean(raw[0])
            b = clean(raw[1]) if len(raw) > 1 else np.full(n, np.nan)
            up = a >= b
            dn = a < b
            out[f"p{k}_up"] = np.where(up, a, np.nan)
            out[f"p{k}_upb"] = np.where(up, b, np.nan)
            out[f"p{k}_dn"] = np.where(dn, a, np.nan)
            out[f"p{k}_dnb"] = np.where(dn, b, np.nan)
        elif dt in (8, 9, 10, 12):
            v = clean(raw[0])
            ci = _shift(np.nan_to_num(raw[-1], nan=0.0), m.shift) if len(raw) > 1 else np.zeros(n)
            ncol = max(len(m.colors), 1)
            for j in range(ncol):
                mask = (np.round(ci) == j) & np.isfinite(v)
                if dt in (8, 9):
                    out[f"p{k}_c{j}"] = segments(v, mask)
                else:
                    out[f"p{k}_c{j}"] = np.where(mask, v, np.nan)
        elif dt == 4:
            out[f"p{k}"] = clean(raw[0])
            out[f"p{k}_b"] = clean(raw[1]) if len(raw) > 1 else np.full(n, np.nan)
        elif dt == 11:
            a = clean(raw[0])
            b = clean(raw[1]) if len(raw) > 1 else np.full(n, np.nan)
            ci = _shift(np.nan_to_num(raw[2], nan=0.0), m.shift) if len(raw) > 2 else np.zeros(n)
            for j in range(max(len(m.colors), 1)):
                mask = np.round(ci) == j
                out[f"p{k}_c{j}"] = np.where(mask, a, np.nan)
                out[f"p{k}_c{j}_b"] = np.where(mask, b, np.nan)
        elif dt in (14, 15, 16, 17):
            parts = [clean(raw[i]) if i < len(raw) else np.full(n, np.nan) for i in range(4)]
            for name, a in zip(("open", "high", "low", "close"), parts):
                out[f"p{k}_{name}"] = a
            if dt in (16, 17):
                ci = np.nan_to_num(raw[4], nan=0.0) if len(raw) > 4 else np.zeros(n)
                out[f"p{k}_color"] = _shift(ci, m.shift)
    return out


# ------------------------------------------------------------------ chart objects -> plots

_ARROW_TYPES = {21: "t1", 22: "t", 23: "t1", 24: "t", 25: "x", 26: "+", 27: "s", 28: "s", 29: "t1", 30: "t", 31: None}
_P_COLOR, _P_ARROW, _P_RAYR, _P_RAY, _P_WIDTH, _P_STYLE = 100, 122, 119, 120, 102, 101
MAX_OBJECT_SERIES = 40


def _obj_color(o, default="#c0c0c0"):
    c = o["i"].get((_P_COLOR, 0))
    h = color_to_hex(c) if c is not None else None
    return h or default


def object_plots(ctx, n: int, separate: bool):
    """Plots for the chart objects a program left on the chart: arrows (as
    markers), horizontal lines, trend lines and rectangles. Text, labels and
    other objects are not drawn."""
    s = ctx.series
    if s is None or not ctx.objects or n == 0:
        return [], {}
    times = s.time
    import bisect

    def bar(t):
        try:
            t = int(t)
        except (TypeError, ValueError):
            return None
        k = bisect.bisect_right(times, t) - 1
        if k < 0 or k >= n:
            return None
        return k

    arrows: dict = {}
    hlines = []
    segs = []
    rects = []
    for name in ctx.object_order:
        o = ctx.objects.get(name)
        if o is None:
            continue
        typ = int(o["type"]) if o["type"] is not None else -1
        sub = int(o.get("sub") or 0)
        if typ in _ARROW_TYPES:
            b = bar(o["time"].get(0, 0))
            price = o["price"].get(0)
            if b is None or price is None:
                continue
            sym = _ARROW_TYPES[typ] or ARROW_SYMBOLS.get(int(o["i"].get((_P_ARROW, 0), 159) or 159), "o")
            key = (sub, sym, _obj_color(o))
            arrows.setdefault(key, []).append((b, float(price)))
        elif typ == 1:
            price = o["price"].get(0)
            if price is not None:
                hlines.append((sub, float(price), _obj_color(o)))
        elif typ in (2, 43, 3):
            b1, b2 = bar(o["time"].get(0, 0)), bar(o["time"].get(1, 0))
            p1, p2 = o["price"].get(0), o["price"].get(1)
            if None in (b1, b2, p1, p2):
                continue
            ray = bool(o["i"].get((_P_RAYR, 0)) or o["i"].get((_P_RAY, 0)))
            segs.append((sub, b1, float(p1), b2, float(p2), ray, _obj_color(o)))
        elif typ == 18:
            b1, b2 = bar(o["time"].get(0, 0)), bar(o["time"].get(1, 0))
            p1, p2 = o["price"].get(0), o["price"].get(1)
            if None in (b1, b2, p1, p2):
                continue
            rects.append((sub, min(b1, b2), max(b1, b2), max(p1, p2), min(p1, p2), _obj_color(o)))
    plots, out = [], {}

    def pane(sub):
        return Pane.SEPARATE if (sub > 0 or (separate and sub != 0)) else Pane.PRICE

    for k, ((sub, sym, col), pts) in enumerate(arrows.items()):
        if len(plots) >= MAX_OBJECT_SERIES:
            break
        arr = np.full(n, np.nan)
        for b, p in pts:
            arr[b] = p
        key = f"obj_arrow{k}"
        out[key] = arr
        plots.append(Plot(key, "Object arrows", style=DrawStyle.ARROW, color=col, symbol=sym, size=9, pane=pane(sub)))
    for k, (sub, price, col) in enumerate(hlines[:20]):
        key = f"obj_hline{k}"
        out[key] = np.full(n, price)
        plots.append(Plot(key, "Horizontal line", color=col, width=1.0, dash=True, autoscale=False, pane=pane(sub)))
    # trend lines packed into as few series as possible (per colour)
    lanes: list = []
    for sub, b1, p1, b2, p2, ray, col in segs:
        if b2 < b1:
            b1, b2, p1, p2 = b2, b1, p2, p1
        end = n - 1 if ray else b2
        xs = np.arange(b1, end + 1)
        ys = p1 + (p2 - p1) * (xs - b1) / (b2 - b1) if b2 != b1 else np.full(len(xs), p1)
        for lane in lanes:
            if lane["col"] != col or lane["sub"] != sub:
                continue
            a = lane["arr"]
            lo, hi = max(b1 - 1, 0), min(end + 1, n - 1)
            window = a[lo:hi + 1]
            touching = np.isfinite(window)
            ok = not touching.any()
            if not ok:
                # allowed: a polyline continuing from the previous segment's end point
                inner = a[b1 + 1:end + 1]
                ok = (not np.isfinite(inner).any()) and np.isfinite(a[b1]) and abs(a[b1] - p1) < 1e-12 \
                    and (b1 == 0 or not np.isfinite(a[max(b1 - 1, 0)]) or True)
            if ok:
                a[b1:end + 1] = np.where(np.isfinite(a[b1:end + 1]), a[b1:end + 1], ys)
                break
        else:
            if len(lanes) >= MAX_OBJECT_SERIES:
                continue
            a = np.full(n, np.nan)
            a[b1:end + 1] = ys
            lanes.append({"col": col, "sub": sub, "arr": a})
    for k, lane in enumerate(lanes):
        key = f"obj_line{k}"
        out[key] = lane["arr"]
        plots.append(Plot(key, "Trend line", color=lane["col"], width=1.0, autoscale=False, pane=pane(lane["sub"])))
    rlanes: list = []
    for sub, b1, b2, top, bot, col in rects:
        for lane in rlanes:
            if lane["col"] == col and lane["sub"] == sub and not np.isfinite(lane["top"][max(b1 - 1, 0):b2 + 2]).any():
                lane["top"][b1:b2 + 1] = top
                lane["bot"][b1:b2 + 1] = bot
                break
        else:
            if len(rlanes) >= MAX_OBJECT_SERIES // 2:
                continue
            t, bo = np.full(n, np.nan), np.full(n, np.nan)
            t[b1:b2 + 1] = top
            bo[b1:b2 + 1] = bot
            rlanes.append({"col": col, "sub": sub, "top": t, "bot": bo})
    for k, lane in enumerate(rlanes):
        key = f"obj_rect{k}"
        out[key] = lane["top"]
        out[key + "b"] = lane["bot"]
        plots.append(Plot(key, "Rectangle", style=DrawStyle.FILL, color=lane["col"], fill_with=key + "b",
                          pane=pane(lane["sub"])))
    return plots, out


# ------------------------------------------------------------------ the plugin base class

_SETUP_CACHE: dict = {}


class MQL5Indicator(Indicator):
    """Base of converted indicators. Subclasses (generated) set
    ``program_file``, ``params`` and ``MQL5_META`` (via the module)."""

    program_file: str = ""
    meta: dict = {}
    #: input python name -> param key (identical in generated files)
    applied_price_param = "applied_price"

    def _inputs(self) -> dict:
        out = {}
        for inp in self.meta.get("inputs", []):
            key = inp["param"]
            if key and hasattr(self.p, key):
                v = getattr(self.p, key)
                out[inp["py"]] = _coerce(v, inp["type"])
        return out

    def _applied(self):
        if self.meta.get("short_form"):
            return int(getattr(self.p, self.applied_price_param, 1))
        return 1

    def setup(self) -> None:
        key = (self.program_file, tuple(sorted((k, repr(v)) for k, v in vars(self.p).items())))
        cached = _SETUP_CACHE.get(key)
        if cached is None:
            ctx = None
            try:
                res = run_program(self.program_file, dummy_market(), "EURUSD", T.PERIOD_H1, self._inputs(),
                                  calculate=False)
                ctx = res.ctx
            except Exception:
                ctx = None
            maps = build_plot_maps(self.meta, ctx)
            levels = list(self.meta.get("levels", []))
            if ctx is not None:
                lv = {}
                for k, v in ctx.ind_props.items():
                    if isinstance(k, tuple) and k[0] == "d" and k[1] == 2 and len(k) == 3:
                        lv[k[2]] = v
                if lv:
                    nlev = ctx.ind_props.get(("i", 2))
                    vals = [lv[i] for i in sorted(lv)]
                    if nlev:
                        vals = vals[: int(nlev)]
                    levels = vals
            cached = (maps, levels)
            if len(_SETUP_CACHE) > 2000:
                _SETUP_CACHE.clear()
            _SETUP_CACHE[key] = cached
        maps, levels = cached
        self._maps = maps
        self.plots = app_plots(maps)
        self.levels = [Level(float(v)) for v in levels]

    def calculate(self, df):
        n = len(df)
        market, sym, period = market_from_df(df)
        res = run_program(self.program_file, market, sym, period, self._inputs(), applied_price=self._applied())
        self.last_error = res.error
        if not res.ok:
            out = {}
            for p in self.plots:
                for key in _plot_keys(p):
                    out[key] = np.full(n, np.nan)
            return out
        maps = build_plot_maps(self.meta, res.ctx)
        vals = plot_arrays(maps, res, n)
        obj_plots, obj_vals = object_plots(res.ctx, n, self.pane is Pane.SEPARATE)
        self.plots = app_plots(self._maps) + obj_plots
        vals.update(obj_vals)
        out = {}
        for p in self.plots:
            for key in _plot_keys(p):
                v = vals.get(key)
                out[key] = v if v is not None and len(v) == n else np.full(n, np.nan)
        return out


def _plot_keys(p: Plot):
    if p.style is DrawStyle.CANDLES:
        keys = [f"{p.key}_{x}" for x in ("open", "high", "low", "close")]
        if p.color_key:
            keys.append(p.color_key)
        return keys
    keys = [p.key]
    if p.fill_with:
        keys.append(p.fill_with)
    return keys
