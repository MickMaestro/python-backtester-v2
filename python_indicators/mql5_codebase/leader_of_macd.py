"""Leader of MACD — converted from MQL5: MQL5 Indicators/Leader of the MACD - Extended/Leader of MACD.mq5

MACD of average
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 8, 4: 1}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16760576, 8036607], 4: [255]}, 'widths': {3: 2}, 'styles': {4: 2}, 'labels': {1: 'MACD', 2: 'Leader', 3: 'Leader of MACD', 4: 'MACD signal'}, 'levels': [], 'description': ['MACD of average'], 'name': 'Leader of MACD', 'source': 'MQL5 Indicators/Leader of the MACD - Extended/Leader of MACD.mq5', 'folder': 'Leader of the MACD - Extended', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'MACD signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSignalOn', 'py': 'inpSignalOn', 'param': 'inpSignalOn', 'type': 'int', 'default': 1, 'label': 'Signal on :', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
color_onSlope = 0
color_onSignal = 1
_enum('enColorOn', {0: 'color_onSlope', 1: 'color_onSignal'})

# enum enSignalOn
signal_onLeader = 0
signal_onMacd = 1
_enum('enSignalOn', {0: 'signal_onLeader', 1: 'signal_onMacd'})

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # MACD signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSignalOn = _input('inpSignalOn', signal_onMacd)  # Signal on :
inpColorOn = _input('inpColorOn', color_onSignal)  # Color change on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
macd = Arr(0, 0.0)
leader = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, macd, INDICATOR_DATA)
    SetIndexBuffer(1, leader, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Leader of MACD (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        iFastEma = iEma(price, inpFastPeriod, i, rates_total, 0)
        iSlowEma = iEma(price, inpSlowPeriod, i, rates_total, 1)
        iFastEmx = iEma(price - iFastEma, inpFastPeriod, i, rates_total, 2)
        iSlowEmx = iEma(price - iSlowEma, inpSlowPeriod, i, rates_total, 3)
        macd[i] = iFastEma - iSlowEma
        leader[i] = iFastEma + iFastEmx - iSlowEma - iSlowEmx
        signal[i] = ((leader[i] - iEma(leader[i], inpSignalPeriod, i, rates_total, 4)) if (inpSignalOn == signal_onLeader) else iEma(macd[i], inpSignalPeriod, i, rates_total, 4))
        val[i] = (leader[i] if (inpSignalOn == signal_onLeader) else macd[i])
        if inpColorOn == color_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def iEma(price, period, r, bars, instanceNo=0):
    if ArrayRange(workEma, 0) != bars:
        ArrayResize(workEma, bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LeaderOfMACD(_MQL5Indicator):
    name = 'Leader of MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpSignalPeriod': 9,  # MACD signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSignalOn': _Choice({0: 'Signal on leader', 1: 'Signal on macd'}, default=1),  # Signal on :
        'inpColorOn': _Choice({0: 'Change color on MACD slope change', 1: 'Change color on MACD crossing signal line'}, default=1),  # Color change on :
    }

