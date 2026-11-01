"""Yang Zhang extension of Garman Klass volatility — converted from MQL5: MQL5 Indicators/Yang Zhang extension of Garman Klass Volatility/Yang Zhang extension of Garman Klass volatility.mq5

Yang Zhang extension of Garman Klass Volatility
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Yang Zhang extension of Garman Klass Volatility'}, 'levels': [], 'description': ['Yang Zhang extension of Garman Klass Volatility'], 'name': 'Yang Zhang extension of Garman Klass volatility', 'source': 'MQL5 Indicators/Yang Zhang extension of Garman Klass Volatility/Yang Zhang extension of Garman Klass volatility.mq5', 'folder': 'Yang Zhang extension of Garman Klass Volatility', 'inputs': [{'mql': 'inpVolPeriod', 'py': 'inpVolPeriod', 'param': 'inpVolPeriod', 'type': 'int', 'default': 22, 'label': 'Volatility lookback period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVolPeriod = _input('inpVolPeriod', 22)  # Volatility lookback period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Yang Zhang extension of Garman Klass Volatility (' + _str(inpVolPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    _corr = sqrt(_fdiv(float(inpVolPeriod), inpVolPeriod - 1.0))
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        work[i][0] = log(_fdiv(open[i], (close[i - 1] if (i > 0) else close[i]))) * log(_fdiv(open[i], (close[i - 1] if (i > 0) else close[i])))
        work[i][1] = 0.5 * log(_fdiv(high[i], low[i])) * log(_fdiv(high[i], low[i]))
        work[i][2] = ((2 * log(2)) - 1.0) * log(_fdiv(close[i], open[i])) * log(_fdiv(close[i], open[i]))
        _sum = 0.0
        k = 0
        while k < inpVolPeriod and (i - k) >= 0:
            _sum += work[i - k][0] + work[i - k][1] - work[i - k][2]
            k += 1
        gkyz = sqrt(_sum) * sqrt(256.0 / float(inpVolPeriod))
        val[i] = gkyz * _corr
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YangZhangExtensionOfGarmanKlassVolatility(_MQL5Indicator):
    name = 'Yang Zhang extension of Garman Klass volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpVolPeriod': 22,  # Volatility lookback period
    }

