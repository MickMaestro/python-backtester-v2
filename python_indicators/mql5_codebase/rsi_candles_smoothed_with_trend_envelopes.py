"""RSI candles - smoothed - with trend envelopes — converted from MQL5: MQL5 Indicators/RSI Сandles - Smoothed with Trend Envelopes/RSI candles - smoothed - with trend envelopes.mq5

Rsi candles - smoothed - with trend envelopes
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 17, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [8421504, 16748574, 3937500], 2: [16748574], 3: [3937500], 4: [16748574], 5: [3937500]}, 'widths': {1: 1, 2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {}, 'labels': {1: 'RSI', 2: 'Trend envelope up trend line', 3: 'Trend envelope down trend line', 4: 'Trend envelope up trend start', 5: 'Trend envelope down trend start'}, 'levels': [], 'description': ['Rsi candles - smoothed - with trend envelopes'], 'name': 'RSI candles - smoothed - with trend envelopes', 'source': 'MQL5 Indicators/RSI Сandles - Smoothed with Trend Envelopes/RSI candles - smoothed - with trend envelopes.mq5', 'folder': 'RSI Сandles - Smoothed with Trend Envelopes', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 32, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpSmtPeriod', 'py': 'inpSmtPeriod', 'param': 'inpSmtPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 20.0, 'label': 'Trend envelopes deviation %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 32)  # RSI period
inpSmtPeriod = _input('inpSmtPeriod', 14)  # Smoothing period (<=1 for no smoothing)
inpMaMethod = _input('inpMaMethod', ma_sma)  # Smoothing method
inpDeviation = _input('inpDeviation', 20.0)  # Trend envelopes deviation %
rsio = Arr(0, 0.0)
rsih = Arr(0, 0.0)
rsil = Arr(0, 0.0)
rsic = Arr(0, 0.0)
rsicl = Arr(0, 0.0)
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
arrowup = Arr(0, 0.0)
arrowdn = Arr(0, 0.0)
_avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(4,))
workSmma = Arr(0, 0.0, dims=(4,))
workLwma = Arr(0, 0.0, dims=(4,))
workRsi = Arr(0, 0.0, dims=(12,))
workTrendEnvelopes = Arr(0, 0.0, dims=(3,))

class sTrendEnvelope(MqlObject):
    _q_fields = ('upline', 'downline', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upline = 0.0
        self.downline = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    SetIndexBuffer(0, rsio, INDICATOR_DATA)
    SetIndexBuffer(1, rsih, INDICATOR_DATA)
    SetIndexBuffer(2, rsil, INDICATOR_DATA)
    SetIndexBuffer(3, rsic, INDICATOR_DATA)
    SetIndexBuffer(4, rsicl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, lineup, INDICATOR_DATA)
    SetIndexBuffer(6, linedn, INDICATOR_DATA)
    SetIndexBuffer(7, arrowup, INDICATOR_DATA)
    PlotIndexGetInteger(3, PLOT_ARROW, 159)
    SetIndexBuffer(8, arrowdn, INDICATOR_DATA)
    PlotIndexGetInteger(4, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi candles with trend envelopes (' + _str(inpRsiPeriod) + ')(' + _str(inpSmtPeriod) + ' ' + _avgNames[inpMaMethod] + ' smoothed)(' + _str(inpDeviation) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _rsi = Arr(4, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _rsi[0] = iRsi(iCustomMa(inpMaMethod, open[i], inpSmtPeriod, i, rates_total, 0), inpRsiPeriod, i, rates_total, 0)
        _rsi[1] = iRsi(iCustomMa(inpMaMethod, high[i], inpSmtPeriod, i, rates_total, 1), inpRsiPeriod, i, rates_total, 1)
        _rsi[2] = iRsi(iCustomMa(inpMaMethod, low[i], inpSmtPeriod, i, rates_total, 2), inpRsiPeriod, i, rates_total, 2)
        _rsi[3] = iRsi(iCustomMa(inpMaMethod, close[i], inpSmtPeriod, i, rates_total, 3), inpRsiPeriod, i, rates_total, 3)
        rsio[i] = _rsi[0]
        rsic[i] = _rsi[3]
        rsih[i] = _rsi[ArrayMaximum(_rsi, 0, 4)]
        rsil[i] = _rsi[ArrayMinimum(_rsi, 0, 4)]
        rsicl[i] = (1 if (rsic[i] > rsio[i]) else 2 if (rsic[i] < rsio[i]) else 0)
        _result = iTrendEnvelope(rsih[i], rsil[i], rsic[i], inpDeviation, i, rates_total)
        lineup[i] = _result.upline
        linedn[i] = _result.downline
        arrowup[i] = (lineup[i] if (_result.trendChange and _result.trend == 1) else EMPTY_VALUE)
        arrowdn[i] = (linedn[i] if (_result.trendChange and _result.trend == -1) else EMPTY_VALUE)
        i += 1
    return i

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

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

def iTrendEnvelope(valueh, valuel, value, deviation, i, bars, instanceNo=0):
    if ArrayRange(workTrendEnvelopes, 0) != bars:
        ArrayResize(workTrendEnvelopes, bars)
    instanceNo *= 3
    workTrendEnvelopes[i][instanceNo + 1] = (1 + (deviation / 100)) * valueh
    workTrendEnvelopes[i][instanceNo + 0] = (1 - (deviation / 100)) * valuel
    workTrendEnvelopes[i][instanceNo + 2] = ((1 if (value > workTrendEnvelopes[i - 1][instanceNo + 1]) else -1 if (value < workTrendEnvelopes[i - 1][instanceNo + 0]) else workTrendEnvelopes[i - 1][instanceNo + 2]) if (i > 0) else 0)
    if (i > 0 and workTrendEnvelopes[i][instanceNo + 2] > 0) and workTrendEnvelopes[i][instanceNo + 0] < workTrendEnvelopes[i - 1][instanceNo + 0]:
        workTrendEnvelopes[i][instanceNo + 0] = workTrendEnvelopes[i - 1][instanceNo + 0]
    if (i > 0 and workTrendEnvelopes[i][instanceNo + 2] < 0) and workTrendEnvelopes[i][instanceNo + 1] > workTrendEnvelopes[i - 1][instanceNo + 1]:
        workTrendEnvelopes[i][instanceNo + 1] = workTrendEnvelopes[i - 1][instanceNo + 1]
    _result = sTrendEnvelope()
    _result.trend = _int(workTrendEnvelopes[i][instanceNo + 2])
    _result.trendChange = ((workTrendEnvelopes[i][instanceNo + 2] != workTrendEnvelopes[i - 1][instanceNo + 2]) if (i > 0) else False)
    _result.upline = (workTrendEnvelopes[i][instanceNo + 0] if (workTrendEnvelopes[i][instanceNo + 2] == 1) else EMPTY_VALUE)
    _result.downline = (workTrendEnvelopes[i][instanceNo + 1] if (workTrendEnvelopes[i][instanceNo + 2] == -1) else EMPTY_VALUE)
    return _copy(_result)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSICandlesSmoothedWithTrendEnvelopes(_MQL5Indicator):
    name = 'RSI candles - smoothed - with trend envelopes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 32,  # RSI period
        'inpSmtPeriod': 14,  # Smoothing period (<=1 for no smoothing)
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
        'inpDeviation': 20.0,  # Trend envelopes deviation %
    }

