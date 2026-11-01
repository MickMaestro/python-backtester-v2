"""M1MA — converted from MQL5: MQL5 Indicators/M1MA indicator/M1MA.mq5

M1-based Moving Average. It gives more adequate estimation of average price per bar compared to any standard price type (close, open, median, typical, weighted, etc).\\n
Copyright: Copyright (c) 2020 Marketeer; Link: https://www.mql5.com/en/users/marketeer; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.indarray import *  # #include IndArray.mqh

MQL5_META = {'props': {'copyright': 'Copyright (c) 2020 Marketeer', 'link': 'https://www.mql5.com/en/users/marketeer', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['M1-based Moving Average. It gives more adequate estimation of average price per bar compared to any standard price type (close, open, median, typical, weighted, etc).\\n'], 'name': 'M1MA', 'source': 'MQL5 Indicators/M1MA indicator/M1MA.mq5', 'folder': 'M1MA indicator', 'inputs': [{'mql': 'BarLimit', 'py': 'BarLimit', 'param': 'BarLimit', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'BarPeriod', 'py': 'BarPeriod', 'param': 'BarPeriod', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'M1Price', 'py': 'M1Price', 'param': 'M1Price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['IndArray.mqh']}

# ---- inputs and global variables
BarLimit = _input('BarLimit', 100)
BarPeriod = _input('BarPeriod', 1)
M1Price = _input('M1Price', PRICE_CLOSE)
handle = 0

def OnInit():
    global handle
    parts = Arr(0, "")
    legend = EnumToString(M1Price, 'ENUM_APPLIED_PRICE')
    if StringSplit(legend, 95, parts) == 2:
        legend = parts[1]
    IndicatorSetString(INDICATOR_SHORTNAME, 'M1MA (' + legend + ',' + _str(BarPeriod) + '[' + _str(_idiv(PeriodSeconds(), 60)) + '])')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1 + BarPeriod)
    p = _idiv(PeriodSeconds(), 60) * BarPeriod
    handle = iMA(Symbol(), PERIOD_M1, p, 0, MODE_SMA, M1Price)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_barCount, _s_OnCalculate_lastBar
    i = 0
    limit = 1
    if _s_OnCalculate_lastBar == 0 or fabs(_s_OnCalculate_barCount - rates_total) > 1:
        limit = _int(MathMin(rates_total - 1 - BarPeriod, BarLimit))
        i = 0
        for i in range(i, rates_total):
            buffers[0][i] = EMPTY_VALUE
        else:
            i = _range_end(i, rates_total, 1)
    elif _s_OnCalculate_lastBar != iTime(None, 0, 0):
        limit = 2
    bar = 0
    i = 0
    for i in range(i, limit):
        dt = iTime(None, 0, i) + PeriodSeconds() - 60
        if dt > TimeCurrent():
            bar = 0
        else:
            bar = iBarShift(None, PERIOD_M1, dt)
        if CopyBuffer(handle, 0, bar, 1, _s_OnCalculate_result) == 1:
            buffers[0][i] = _s_OnCalculate_result[0]
        else:
            if prev_calculated == 0:
                Print('M1 not ready: ', GetLastError())
            return prev_calculated
    else:
        i = _range_end(i, limit, 1)
    _s_OnCalculate_lastBar = iTime(None, 0, 0)
    _s_OnCalculate_barCount = rates_total
    return rates_total

# ---- global variables initialised from expressions
buffers = _alloc(IndicatorArray)
buffers.__init__(1)

# ---- static local variables
_s_OnCalculate_lastBar = 0
_s_OnCalculate_barCount = 0
_s_OnCalculate_result = Arr(1, 0.0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class M1MA(_MQL5Indicator):
    name = 'M1MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BarLimit': 100,
        'BarPeriod': 1,
        'M1Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

