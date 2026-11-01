"""Logarithmic Garman Klass Volatility — converted from MQL5: MQL5 Indicators/Logarithmic Garman Klass volatility/Logarithmic Garman Klass Volatility.mq5

Logarithmic Garman Klass Volatility
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Logarithmic Garman Klass Volatility'}, 'levels': [], 'description': ['Logarithmic Garman Klass Volatility'], 'name': 'Logarithmic Garman Klass Volatility', 'source': 'MQL5 Indicators/Logarithmic Garman Klass volatility/Logarithmic Garman Klass Volatility.mq5', 'folder': 'Logarithmic Garman Klass volatility', 'inputs': [{'mql': 'inpVolPeriod', 'py': 'inpVolPeriod', 'param': 'inpVolPeriod', 'type': 'int', 'default': 30, 'label': 'Volatility lookback period', 'sinput': False}, {'mql': 'inpCompound', 'py': 'inpCompound', 'param': 'inpCompound', 'type': 'int', 'default': 252, 'label': 'Compound', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVolPeriod = _input('inpVolPeriod', 30)  # Volatility lookback period
inpCompound = _input('inpCompound', 252)  # Compound
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Logarithmic Garman Klass Volatility (' + _str(inpVolPeriod) + ',' + _str(inpCompound) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        work[i][0] = log(_fdiv(close[i], (close[i - 1] if (i > 0) else close[i])))
        work[i][1] = log(_fdiv(close[i], open[i]))
        work[i][2] = log(_fdiv(open[i], (close[i - 1] if (i > 0) else close[i])))
        work[i][3] = log(_fdiv(high[i], low[i]))
        lambda_ = _fdiv(inpVolPeriod, inpVolPeriod + 3.0)
        varCC = 0.0
        k = 0
        while k < inpVolPeriod and (i - k) >= 0:
            varCC += work[i - k][0] * work[i - k][0]
            k += 1
        varCC = varCC / inpVolPeriod
        work[i][5] = varCC
        work[i][4] = (work[i][2] * work[i][2]) + (0.5 * (work[i][3] * work[i][3])) - (0.386 * (work[i][1] * work[i][1]))
        if i > (inpVolPeriod + 4):
            work[i][5] = (log(varCC) if (varCC > 0) else log(1))
            work[i][5] = ((1.0 - lambda_) * log((work[i - 1][4] if (work[i - 1][4] > 0) else 1))) + (lambda_ * log((work[i - 1][5] if (work[i - 1][5] > 0) else 1)))
            work[i][5] = exp(work[i][5])
        val[i] = sqrt(work[i][5]) * sqrt(inpCompound) * 100
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LogarithmicGarmanKlassVolatility(_MQL5Indicator):
    name = 'Logarithmic Garman Klass Volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpVolPeriod': 30,  # Volatility lookback period
        'inpCompound': 252,  # Compound
    }

