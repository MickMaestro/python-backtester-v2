"""NonLagMa Keltner channel — converted from MQL5: MQL5 Indicators/NonLagMA Keltner Сhannel/NonLagMa Keltner channel.mq5

NonLagMA Keltner channel
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 1}, 'colors': {1: [13628367], 2: [13492732], 3: [3329330, 6333684], 4: [3329330, 6333684], 5: [11119017]}, 'widths': {}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': ['NonLagMA Keltner channel'], 'name': 'NonLagMa Keltner channel', 'source': 'MQL5 Indicators/NonLagMA Keltner Сhannel/NonLagMa Keltner channel.mq5', 'folder': 'NonLagMA Keltner Сhannel', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpAtrMultiplier', 'py': 'inpAtrMultiplier', 'param': 'inpAtrMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Channel multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
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
nlmvalues = Arr(0, 0.0, dims=(3,))
nlmprices = Arr(0, 0.0, dims=(1,))
nlmalphas = Arr(0, 0.0, dims=(1,))

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
        bufferMe[i] = iNonLagMa(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
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

def iNonLagMa(price, length, r, bars, instanceNo=0):
    if ArrayRange(nlmprices, 0) != bars:
        ArrayResize(nlmprices, bars)
    if ArrayRange(nlmvalues, 0) < (instanceNo + 1):
        ArrayResize(nlmvalues, instanceNo + 1)
    nlmprices[r][instanceNo] = price
    if length < 5 or r < 3:
        return nlmprices[r][instanceNo]
    if nlmvalues[instanceNo][0] != length:
        Cycle = 4.0
        Coeff = 3.0 * M_PI
        Phase = _int(length - 1)
        nlmvalues[instanceNo][0] = length
        nlmvalues[instanceNo][1] = _int(length * 4) + Phase
        nlmvalues[instanceNo][2] = 0.0
        if ArrayRange(nlmalphas, 0) < _int(nlmvalues[instanceNo][1]):
            ArrayResize(nlmalphas, _int(nlmvalues[instanceNo][1]))
        k = 0
        while k < _int(nlmvalues[instanceNo][1]):
            t = 0.0
            if k <= (Phase - 1):
                t = _fdiv(1.0 * k, Phase - 1)
            else:
                t = 1.0 + _fdiv((k - Phase + 1) * ((2.0 * Cycle) - 1.0), (Cycle * length) - 1.0)
            beta = MathCos(M_PI * t)
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            nlmalphas[k][instanceNo] = g * beta
            nlmvalues[instanceNo][2] += nlmalphas[k][instanceNo]
            k += 1
    if nlmvalues[instanceNo][2] > 0:
        sum_ = 0.0
        k = 0
        while k < _int(nlmvalues[instanceNo][1]) and (r - k) >= 0:
            sum_ += nlmalphas[k][instanceNo] * nlmprices[r - k][instanceNo]
            k += 1
        return _fdiv(sum_, nlmvalues[instanceNo][2])
    else:
        return 0.0

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


class NonLagMaKeltnerChannel(_MQL5Indicator):
    name = 'NonLagMa Keltner channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpAtrPeriod': 14,  # ATR period
        'inpAtrMultiplier': 1.5,  # Channel multiplier
    }

