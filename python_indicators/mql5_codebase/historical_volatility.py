"""Historical volatility — converted from MQL5: MQL5 Indicators/Historical Volatility/Historical volatility.mq5

Historical volatility
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Historical volatility'}, 'levels': [], 'description': ['Historical volatility'], 'name': 'Historical volatility', 'source': 'MQL5 Indicators/Historical Volatility/Historical volatility.mq5', 'folder': 'Historical Volatility', 'inputs': [{'mql': 'inpVolPeriod', 'py': 'inpVolPeriod', 'param': 'inpVolPeriod', 'type': 'int', 'default': 18, 'label': 'Volatility period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVolPeriod = _input('inpVolPeriod', 18)  # Volatility period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Historical volatility (' + _str(inpVolPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    work = Arr(0, 0.0)
    ArrayResize(work, inpVolPeriod)
    ArrayInitialize(work, 0)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        avg = 0.0
        sum_ = 0.0
        k = 0
        while k < inpVolPeriod and (i - k) > 0:
            work[k] = MathLog(_fdiv(close[i - k], close[i - k - 1]))
            avg += work[k]
            k += 1
        avg = avg / inpVolPeriod
        for k in range(0, inpVolPeriod):
            sum_ += (work[k] - avg) * (work[k] - avg)
        val[i] = MathSqrt(sum_ / inpVolPeriod)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HistoricalVolatility(_MQL5Indicator):
    name = 'Historical volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpVolPeriod': 18,  # Volatility period
    }

