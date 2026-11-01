"""EhlersCyberCycle — converted from MQL5: MQL5 Indicators/The Cyber Cycle/EhlersCyberCycle.mq5

Telegram Channel: https://t.me/fxstill\\n
The Cyber Cycle:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.34
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 3329330], 2: [42495]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The Cyber Cycle:\\nJohn Ehlers, \\"Cybernetic Analysis For Stocks And Futures\\", pg.34'], 'name': 'EhlersCyberCycle', 'source': 'MQL5 Indicators/The Cyber Cycle/EhlersCyberCycle.mq5', 'folder': 'The Cyber Cycle', 'inputs': [{'mql': 'alpha', 'py': 'alpha', 'param': 'alpha', 'type': 'double', 'default': 0.07, 'label': 'Alpha', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
alpha = _input('alpha', 0.07)  # Alpha
cycle = Arr(0, 0.0)
trigger = Arr(0, 0.0)
smooth = Arr(0, 0.0)
cf = Arr(0, 0.0)
a1 = 0.0
a2 = 0.0
MINBAR = 5

def OnInit():
    SetIndexBuffer(0, cycle, INDICATOR_DATA)
    SetIndexBuffer(1, cf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, trigger, INDICATOR_DATA)
    SetIndexBuffer(3, smooth, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(cycle, True)
    ArraySetAsSeries(trigger, True)
    ArraySetAsSeries(smooth, True)
    ArraySetAsSeries(cf, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersSuperPassBandFilter')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def GetValue(price, shift):
    smooth[shift] = (price[shift] + (2 * price[shift + 1]) + (2 * price[shift + 2]) + price[shift + 3]) / 6
    if False:
        cycle[shift] = (price[shift] - (2 * price[shift + 1]) + price[shift + 2]) / 4
    else:
        c1 = ZerroIfEmpty(cycle[shift + 1])
        c2 = ZerroIfEmpty(cycle[shift + 2])
        cycle[shift] = (pow(1 - (0.5 * alpha), 2) * (smooth[shift] - (2 * smooth[shift + 1]) + smooth[shift + 2])) + (2 * (1 - alpha) * c1) - (pow(1 - alpha, 2) * c2)
    trigger[shift] = cycle[shift + 1]
    if cycle[shift] < trigger[shift]:
        cf[shift] = 1.0
    elif cycle[shift] > trigger[shift]:
        cf[shift] = 2.0

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
        ArrayInitialize(cycle, EMPTY_VALUE)
        ArrayInitialize(trigger, EMPTY_VALUE)
        ArrayInitialize(smooth, 0)
        ArrayInitialize(cf, 0)
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


class EhlersCyberCycle(_MQL5Indicator):
    name = 'EhlersCyberCycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'alpha': 0.07,  # Alpha
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

