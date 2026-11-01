"""EhlersDecycler — converted from MQL5: MQL5 Indicators/The Decycler/EhlersDecycler.mq5

The Decycler:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.40-41
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 3329330]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'db'}, 'levels': [], 'description': ['The Decycler:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.40-41'], 'name': 'EhlersDecycler', 'source': 'MQL5 Indicators/The Decycler/EhlersDecycler.mq5', 'folder': 'The Decycler', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
length = _input('length', 20)
db = Arr(0, 0.0)
dc = Arr(0, 0.0)
a = 0.0
a1 = 0.0
t = 0.0
MINBAR = 5

def OnInit():
    global a, a1, t
    SetIndexBuffer(0, db, INDICATOR_DATA)
    SetIndexBuffer(1, dc, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(db, True)
    ArraySetAsSeries(dc, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersDecycler')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    t = (2 * M_PI) / length
    a = _fdiv(MathCos(t) + MathSin(t) - 1, MathCos(t))
    a1 = 1 - a
    a = a / 2
    return INIT_SUCCEEDED

def GetValue(price, shift):
    d1 = ZerroIfEmpty(db[shift + 1])
    db[shift] = (a * (price[shift] + price[shift + 1])) + (a1 * d1)
    if db[shift] < price[shift]:
        dc[shift] = 2.0
    elif db[shift] > price[shift]:
        dc[shift] = 1.0

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
        ArrayInitialize(db, EMPTY_VALUE)
        ArrayInitialize(dc, 0)
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


class EhlersDecycler(_MQL5Indicator):
    name = 'EhlersDecycler'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 20,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

