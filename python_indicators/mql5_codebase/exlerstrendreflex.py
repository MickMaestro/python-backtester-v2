"""ExlersTrendReflex — converted from MQL5: MQL5 Indicators/Reflex and Trendflex/ExlersTrendReflex.mq5

Telegram Channel: https://t.me/fxstill\\n
Reflex: A New Zero-Lag Indicator. John Ehlers, \\"Stocks & Commodities. Feb.2020 pg. 6-8\\"
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16748574]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RefLex', 2: 'Trendflex'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'Reflex: A New Zero-Lag Indicator. John Ehlers, \\"Stocks & Commodities. Feb.2020 pg. 6-8\\"'], 'name': 'ExlersTrendReflex', 'source': 'MQL5 Indicators/Reflex and Trendflex/ExlersTrendReflex.mq5', 'folder': 'Reflex and Trendflex', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 20)
rf = Arr(0, 0.0)
tf = Arr(0, 0.0)
fl = Arr(0, 0.0)
ts = Arr(0, 0.0)
rs = Arr(0, 0.0)
MINBAR = Length + 1
c1 = 0.0
c2 = 0.0
c3 = 0.0

def OnInit():
    global c1, c2, c3
    SetIndexBuffer(0, rf, INDICATOR_DATA)
    SetIndexBuffer(1, tf, INDICATOR_DATA)
    SetIndexBuffer(2, fl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ts, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, rs, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(rf, True)
    ArraySetAsSeries(tf, True)
    ArraySetAsSeries(fl, True)
    ArraySetAsSeries(ts, True)
    ArraySetAsSeries(rs, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ExlersTrendReflex')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    a1 = MathExp(_fdiv((-M_SQRT2) * M_PI, 0.5 * Length))
    b1 = 2 * a1 * MathCos(_fdiv(M_SQRT2 * M_PI, 0.5 * Length))
    c2 = b1
    c3 = (-a1) * a1
    c1 = 1 - c2 - c3
    return INIT_SUCCEEDED

def GetValue(data, i):
    fl[i] = ((c1 * (data[i] + data[i + 1])) / 2) + (c2 * fl[i + 1]) + (c3 * fl[i + 2])
    sum0 = 0.0
    sum1 = 0.0
    slope = (fl[i + Length] - fl[i]) / Length
    for k in range(1, Length + 1):
        sum0 += fl[i] - fl[i + k]
        sum1 += fl[i] + (k * slope) - fl[i + k]
    sum0 = sum0 / Length
    sum1 = sum1 / Length
    ts[i] = (0.04 * sum0 * sum0) + (0.96 * ts[i + 1])
    rs[i] = (0.04 * sum1 * sum1) + (0.96 * rs[i + 1])
    if ts[i] != 0:
        tf[i] = _fdiv(sum0, MathSqrt(ts[i]))
    if rs[i] != 0:
        rf[i] = _fdiv(sum1, MathSqrt(rs[i]))

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < MINBAR:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(close, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(rf, EMPTY_VALUE)
        ArrayInitialize(tf, EMPTY_VALUE)
        ArrayInitialize(fl, 0)
        ArrayInitialize(ts, 0)
        ArrayInitialize(rs, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(close, i)
        return rates_total
    GetValue(close, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExlersTrendReflex(_MQL5Indicator):
    name = 'ExlersTrendReflex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 20,
    }

