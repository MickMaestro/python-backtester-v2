"""EhlersDecycler-II — converted from MQL5: MQL5 Indicators/The Decycler II/EhlersDecycler-II.mq5

The Decycler:\\nJohn Ehlers, \\"Stocks & Commodities V. 33:09\\", pg.12-15
Copyright: Copyright 2021, Andrei Novichkov.; Link: https://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Andrei Novichkov.', 'link': 'https://fxstill.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 8, 2: 1, 3: 1}, 'colors': {1: [9470064, 16711680, 255], 2: [3329330], 3: [3329330]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'decycler', 2: 'decyclerUp', 3: 'decyclerDown'}, 'levels': [], 'description': ['The Decycler:\\nJohn Ehlers, \\"Stocks & Commodities V. 33:09\\", pg.12-15'], 'name': 'EhlersDecycler-II', 'source': 'MQL5 Indicators/The Decycler II/EhlersDecycler-II.mq5', 'folder': 'The Decycler II', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'wdt', 'py': 'wdt', 'param': 'wdt', 'type': 'double', 'default': 0.2, 'label': 'Channel Width', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
length = _input('length', 20)  # Period
wdt = _input('wdt', 0.2)  # Channel Width
decyclerBuffer = Arr(0, 0.0)
decyclerColors = Arr(0, 0.0)
decyclerUpBuffer = Arr(0, 0.0)
decyclerDownBuffer = Arr(0, 0.0)
hp = Arr(0, 0.0)
MINBAR = 5
a1 = 0.0
a2 = 0.0
a3 = 0.0
wu = 0.0
wd = 0.0

def OnInit():
    global a1, a2, a3, wd, wu
    SetIndexBuffer(0, decyclerBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, decyclerColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, decyclerUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, decyclerDownBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, hp, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(decyclerBuffer, True)
    ArraySetAsSeries(decyclerColors, True)
    ArraySetAsSeries(decyclerUpBuffer, True)
    ArraySetAsSeries(decyclerDownBuffer, True)
    ArraySetAsSeries(hp, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersDecycler-II')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    t0 = (((0.707 * 360) / length) * M_PI) / 180
    tc = MathCos(t0)
    ts = MathSin(t0)
    alpha = _fdiv(tc + ts - 1, tc)
    a1 = 1 - alpha
    a2 = 1 - (alpha / 2)
    a2 *= a2
    a3 = a1 * a1
    wu = 1.0 + (wdt / 200.0)
    wd = 1.0 - (wdt / 200.0)
    return INIT_SUCCEEDED

def GetValue(price, shift):
    d1 = ZerroIfEmpty(hp[shift + 1])
    d2 = ZerroIfEmpty(hp[shift + 2])
    hp[shift] = (a2 * (price[shift] - (2 * price[shift + 1]) + price[shift + 2])) + (2 * a1 * d1) - (a3 * d2)
    decyclerBuffer[shift] = price[shift] - hp[shift]
    decyclerUpBuffer[shift] = wu * decyclerBuffer[shift]
    decyclerDownBuffer[shift] = wd * decyclerBuffer[shift]
    if decyclerBuffer[shift] < price[shift]:
        decyclerColors[shift] = 1.0
    elif decyclerBuffer[shift] > price[shift]:
        decyclerColors[shift] = 2.0
    else:
        decyclerColors[shift] = 0.0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total <= MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(decyclerBuffer, EMPTY_VALUE)
        ArrayInitialize(decyclerColors, 0)
        ArrayInitialize(decyclerUpBuffer, EMPTY_VALUE)
        ArrayInitialize(decyclerDownBuffer, EMPTY_VALUE)
        ArrayInitialize(hp, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersDecyclerII(_MQL5Indicator):
    name = 'EhlersDecycler-II'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 20,  # Period
        'wdt': 0.2,  # Channel Width
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

