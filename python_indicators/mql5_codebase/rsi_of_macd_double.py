"""rsi_of_macd_double — converted from MQL5: MQL5 Indicators/RSI of MACD double/rsi_of_macd_double.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 10, 2: 8, 3: 1}, 'colors': {1: [65280, 32768, 42495, 755384], 2: [65280, 42495], 3: [55295]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'MACD histo', 2: 'MACD', 3: 'Signal'}, 'levels': [], 'description': [], 'name': 'rsi_of_macd_double', 'source': 'MQL5 Indicators/RSI of MACD double/rsi_of_macd_double.mq5', 'folder': 'RSI of MACD double', 'inputs': [{'mql': 'InpRsiPeriod', 'py': 'InpRsiPeriod', 'param': 'InpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalEMA', 'py': 'InpSignalEMA', 'param': 'InpSignalEMA', 'type': 'int', 'default': 9, 'label': 'Signal EMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'InpDoubleMacd', 'py': 'InpDoubleMacd', 'param': 'InpDoubleMacd', 'type': 'bool', 'default': True, 'label': 'Should it be double macd?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted'})

# ---- inputs and global variables
InpRsiPeriod = _input('InpRsiPeriod', 14)  # RSI period
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalEMA = _input('InpSignalEMA', 9)  # Signal EMA period
InpAppliedPrice = _input('InpAppliedPrice', pr_close)  # Price to use
InpDoubleMacd = _input('InpDoubleMacd', True)  # Should it be double macd?
macd = Arr(0, 0.0)
maclc = Arr(0, 0.0)
macdh = Arr(0, 0.0)
macdc = Arr(0, 0.0)
signal = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, macdh, INDICATOR_DATA)
    SetIndexBuffer(1, macdc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, macd, INDICATOR_DATA)
    SetIndexBuffer(3, maclc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    add = ''
    if InpDoubleMacd:
        add = 'double'
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD ' + add + ' (' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ',' + _str(InpSignalEMA) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(InpAppliedPrice, open, close, high, low, i, rates_total)
        tmacd = iEma(price, InpFastEMA, rates_total, i, 0) - iEma(price, InpSlowEMA, rates_total, i, 1)
        if InpDoubleMacd:
            macd[i] = iRsi(iEma(tmacd, InpFastEMA, rates_total, i, 2) - iEma(tmacd, InpSlowEMA, rates_total, i, 3), InpRsiPeriod, rates_total, i) - 50
        else:
            macd[i] = iRsi(tmacd, InpRsiPeriod, rates_total, i) - 50
        signal[i] = iEma(macd[i], InpSignalEMA, rates_total, i, 4)
        macdh[i] = macd[i]
        if i > 0:
            macdc[i] = macdc[i - 1]
            maclc[i] = maclc[i - 1]
            if macd[i] > 0:
                if macd[i] > macd[i - 1]:
                    macdc[i] = 0.0
                if macd[i] < macd[i - 1]:
                    macdc[i] = 1.0
            if macd[i] < 0:
                if macd[i] < macd[i - 1]:
                    macdc[i] = 2.0
                if macd[i] > macd[i - 1]:
                    macdc[i] = 3.0
            if macd[i] > signal[i]:
                maclc[i] = 0.0
            if macd[i] < signal[i]:
                maclc[i] = 1.0
    return rates_total

def iRsi(price, period, bars, i, forInstance=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = forInstance * 3
    alpha = _fdiv(1.0, period)
    workRsi[i][0 + z] = price
    if i < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (i - k - 1) >= 0:
            sum_ += MathAbs(workRsi[i - k][0 + z] - workRsi[i - k - 1][0 + z])
            k += 1
        workRsi[i][1 + z] = _fdiv(workRsi[i][0 + z] - workRsi[0][0 + z], MathMax(k, 1))
        workRsi[i][2 + z] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[i][0 + z] - workRsi[i - 1][0 + z]
        workRsi[i][1 + z] = workRsi[i - 1][1 + z] + (alpha * (change - workRsi[i - 1][1 + z]))
        workRsi[i][2 + z] = workRsi[i - 1][2 + z] + (alpha * (MathAbs(change) - workRsi[i - 1][2 + z]))
    if workRsi[i][2 + z] != 0:
        return 50.0 * (_fdiv(workRsi[i][1 + z], workRsi[i][2 + z]) + 1)
    else:
        return 0.0

def iEma(price, period, bars, r, instanceNo=0):
    if ArrayRange(workEma, 0) != bars:
        ArrayResize(workEma, bars)
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    else:
        workEma[r][instanceNo] = price
    return workEma[r][instanceNo]

def getPrice(pricet, open, close, high, low, i, bars):
    _sw1 = pricet
    if _sw1 == pr_close:
        return close[i]
    elif _sw1 == pr_open:
        return open[i]
    elif _sw1 == pr_high:
        return high[i]
    elif _sw1 == pr_low:
        return low[i]
    elif _sw1 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiOfMacdDouble(_MQL5Indicator):
    name = 'rsi_of_macd_double'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRsiPeriod': 14,  # RSI period
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalEMA': 9,  # Signal EMA period
        'InpAppliedPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted'}, default=0),  # Price to use
        'InpDoubleMacd': True,  # Should it be double macd?
    }

