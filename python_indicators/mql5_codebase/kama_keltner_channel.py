"""KAMA Keltner channel — converted from MQL5: MQL5 Indicators/KAMA Keltner Сhannel/KAMA Keltner channel.mq5

Kaufman adaptive average Keltner channel
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 1}, 'colors': {1: [13628367], 2: [13492732], 3: [3329330, 6333684], 4: [3329330, 6333684], 5: [11119017]}, 'widths': {}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': ['Kaufman adaptive average Keltner channel'], 'name': 'KAMA Keltner channel', 'source': 'MQL5 Indicators/KAMA Keltner Сhannel/KAMA Keltner channel.mq5', 'folder': 'KAMA Keltner Сhannel', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpPower', 'py': 'inpPower', 'param': 'inpPower', 'type': 'double', 'default': 2.0, 'label': 'Smooth power', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpAtrMultiplier', 'py': 'inpAtrMultiplier', 'param': 'inpAtrMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Channel multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFastPeriod = _input('inpFastPeriod', 2)  # Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # Slow end period
inpPower = _input('inpPower', 2.0)  # Smooth power
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpAtrPeriod = _input('inpAtrPeriod', 14)  # ATR period
inpAtrMultiplier = _input('inpAtrMultiplier', 1.5)  # Channel multiplier
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
workAma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _atr = 0.0
        k = 0
        while k < inpAtrPeriod and (i - k - 1) >= 0:
            _atr += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        _atr = _atr / inpAtrPeriod
        bufferMe[i] = iKama(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpFastPeriod, inpSlowPeriod, inpPower, i, open, close, high, low, rates_total)
        bufferUp[i] = bufferMe[i] + (_atr * inpAtrMultiplier)
        bufferDn[i] = bufferMe[i] - (_atr * inpAtrMultiplier)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        if i > 0:
            bufferUpc[i] = bufferUpc[i - 1]
            bufferDnc[i] = bufferDnc[i - 1]
            if bufferUp[i] > bufferUp[i - 1]:
                bufferUpc[i] = 0.0
            if bufferUp[i] < bufferUp[i - 1]:
                bufferUpc[i] = 1.0
            if bufferDn[i] > bufferDn[i - 1]:
                bufferDnc[i] = 0.0
            if bufferDn[i] < bufferDn[i - 1]:
                bufferDnc[i] = 1.0
        i += 1
    return i

def iKama(price, period, fast, slow, power, i, open, close, high, low, bars, instanceNo=0):
    if ArrayRange(workAma, 0) != bars:
        ArrayResize(workAma, bars)
    r = i
    instanceNo *= 3
    fastend = _fdiv(2.0, fast + 1)
    slowend = _fdiv(2.0, slow + 1)
    efratio = 1.0
    workAma[r][instanceNo + 2] = price
    signal = (MathAbs(price - workAma[r - period][instanceNo + 2]) if (r >= period) else 0)
    noise = 0.0
    workAma[r][instanceNo + 0] = (MathAbs(price - workAma[r - 1][instanceNo + 2]) if (r > 0) else 0)
    k = 0
    while k < period and (r - k) >= 0:
        noise += workAma[r - k][instanceNo + 0]
        k += 1
    if noise != 0:
        efratio = _fdiv(signal, noise)
    else:
        efratio = 1.0
    smooth = MathPow((efratio * (fastend - slowend)) + slowend, power)
    workAma[r][instanceNo + 1] = ((workAma[r - 1][instanceNo + 1] + (smooth * (price - workAma[r - 1][instanceNo + 1]))) if (r > 0) else price)
    return workAma[r][instanceNo + 1]

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


class KAMAKeltnerChannel(_MQL5Indicator):
    name = 'KAMA Keltner channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFastPeriod': 2,  # Fast end period
        'inpSlowPeriod': 30,  # Slow end period
        'inpPower': 2.0,  # Smooth power
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpAtrPeriod': 14,  # ATR period
        'inpAtrMultiplier': 1.5,  # Channel multiplier
    }

