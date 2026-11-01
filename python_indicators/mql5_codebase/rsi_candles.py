"""RSI candles — converted from MQL5: MQL5 Indicators/RSI Candles/RSI candles.mq5

Rsi candles
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 16748574, 3937500]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RSI'}, 'levels': [], 'description': ['Rsi candles'], 'name': 'RSI candles', 'source': 'MQL5 Indicators/RSI Candles/RSI candles.mq5', 'folder': 'RSI Candles', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
rsio = Arr(0, 0.0)
rsih = Arr(0, 0.0)
rsil = Arr(0, 0.0)
rsic = Arr(0, 0.0)
rsicl = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(12,))

def OnInit():
    SetIndexBuffer(0, rsio, INDICATOR_DATA)
    SetIndexBuffer(1, rsih, INDICATOR_DATA)
    SetIndexBuffer(2, rsil, INDICATOR_DATA)
    SetIndexBuffer(3, rsic, INDICATOR_DATA)
    SetIndexBuffer(4, rsicl, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi candles (' + _str(inpRsiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _rsi = Arr(4, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _rsi[0] = iRsi(open[i], inpRsiPeriod, i, rates_total, 0)
        _rsi[1] = iRsi(high[i], inpRsiPeriod, i, rates_total, 1)
        _rsi[2] = iRsi(low[i], inpRsiPeriod, i, rates_total, 2)
        _rsi[3] = iRsi(close[i], inpRsiPeriod, i, rates_total, 3)
        rsio[i] = _rsi[0]
        rsic[i] = _rsi[3]
        rsih[i] = _rsi[ArrayMaximum(_rsi, 0, 4)]
        rsil[i] = _rsi[ArrayMinimum(_rsi, 0, 4)]
        rsicl[i] = (1 if (rsic[i] > rsio[i]) else 2 if (rsic[i] < rsio[i]) else 0)
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSICandles(_MQL5Indicator):
    name = 'RSI candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
    }

