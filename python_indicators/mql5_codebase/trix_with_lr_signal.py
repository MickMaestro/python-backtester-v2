"""TRIX with LR signal — converted from MQL5: MQL5 Indicators/Trix with LR signal/TRIX with LR signal.mq5

Trix with linear regression signal line
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 16748574, 6333684], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'Trix signal', 2: 'Trix'}, 'levels': [], 'description': ['Trix with linear regression signal line'], 'name': 'TRIX with LR signal', 'source': 'MQL5 Indicators/Trix with LR signal/TRIX with LR signal.mq5', 'folder': 'Trix with LR signal', 'inputs': [{'mql': 'inpTrixPeriod', 'py': 'inpTrixPeriod', 'param': 'inpTrixPeriod', 'type': 'int', 'default': 8, 'label': 'Trix period', 'sinput': False}, {'mql': 'inpTrixPrice', 'py': 'inpTrixPrice', 'param': 'inpTrixPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSignPeriod', 'py': 'inpSignPeriod', 'param': 'inpSignPeriod', 'type': 'int', 'default': 14, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTrixPeriod = _input('inpTrixPeriod', 8)  # Trix period
inpTrixPrice = _input('inpTrixPrice', PRICE_CLOSE)  # Price
inpSignPeriod = _input('inpSignPeriod', 14)  # Signal period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
signalc = Arr(0, 0.0)
workTrix = Arr(0, 0.0, dims=(3,))
workLinr = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, signal, INDICATOR_DATA)
    SetIndexBuffer(1, signalc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRIX with LR (' + _str(inpTrixPeriod) + ',' + _str(inpSignPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(workTrix, 0) != rates_total:
        ArrayResize(workTrix, rates_total)
    alpha = _fdiv(2.0, 1.0 + inpTrixPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = MathLog(getPrice(inpTrixPrice, open, close, high, low, i, rates_total))
        workTrix[i][0] = ((workTrix[i - 1][0] + (alpha * (price - workTrix[i - 1][0]))) if (i > 0) else 0)
        workTrix[i][1] = ((workTrix[i - 1][1] + (alpha * (workTrix[i][0] - workTrix[i - 1][1]))) if (i > 0) else 0)
        workTrix[i][2] = ((workTrix[i - 1][2] + (alpha * (workTrix[i][1] - workTrix[i - 1][2]))) if (i > 0) else 0)
        val[i] = ((_fdiv(workTrix[i][2] - workTrix[i - 1][2], workTrix[i - 1][2]) if (workTrix[i - 1][2] != 0) else 0) if (i > 0) else 0)
        signal[i] = iLinr(val[i], inpSignPeriod, i, rates_total)
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        signalc[i] = valc[i]
        i += 1
    return i

def iLinr(price, period, r, bars, instanceNo=0):
    if ArraySize(workLinr) != bars:
        ArrayResize(workLinr, bars)
    period = MathMax(period, 1)
    workLinr[r][instanceNo] = price
    lwmw = period
    lwma = lwmw * price
    sma = price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        lwmw += weight
        lwma += weight * workLinr[r - k][instanceNo]
        sma += workLinr[r - k][instanceNo]
        k += 1
    return _fdiv(3.0 * lwma, lwmw) - _fdiv(2.0 * sma, period)

def getPrice(tprice, open, close, high, low, i, _bars):
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


class TRIXWithLRSignal(_MQL5Indicator):
    name = 'TRIX with LR signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTrixPeriod': 8,  # Trix period
        'inpTrixPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSignPeriod': 14,  # Signal period
    }

