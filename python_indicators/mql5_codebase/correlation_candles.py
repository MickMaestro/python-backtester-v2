"""Correlation_candles — converted from MQL5: MQL5 Indicators/Correlation candles/Correlation_candles.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 17}, 'colors': {1: [8421504, 3329330, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: 'correlation candles'}, 'levels': [], 'description': [], 'name': 'Correlation_candles', 'source': 'MQL5 Indicators/Correlation candles/Correlation_candles.mq5', 'folder': 'Correlation candles', 'inputs': [{'mql': 'CorPeriod', 'py': 'CorPeriod', 'param': 'CorPeriod', 'type': 'int', 'default': 32, 'label': 'Correlation rank', 'sinput': False}, {'mql': 'CorType', 'py': 'CorType', 'param': 'CorType', 'type': 'int', 'default': 0, 'label': 'Correlation type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enCorrType
cor_spe = 0
cor_pea = 1
_enum('enCorrType', {0: 'cor_spe', 1: 'cor_pea'})

# ---- inputs and global variables
CorPeriod = _input('CorPeriod', 32)  # Correlation rank
CorType = _input('CorType', cor_spe)  # Correlation type
canc = Arr(0, 0.0)
cano = Arr(0, 0.0)
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
colors = Arr(0, 0.0)
corrNames = Arr.of(['Spearman', 'Pearson'], fill="")
workPearson = Arr(0, 0.0, dims=(4,))
workSpearman = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    SetIndexBuffer(4, colors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, corrNames[CorType] + ' candles (' + _str(CorPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        values = Arr(4, 0.0, dyn=False)
        values[0] = iCorrelation(CorType, open[i], CorPeriod, i, rates_total, 0)
        values[1] = iCorrelation(CorType, close[i], CorPeriod, i, rates_total, 1)
        values[2] = iCorrelation(CorType, high[i], CorPeriod, i, rates_total, 2)
        values[3] = iCorrelation(CorType, low[i], CorPeriod, i, rates_total, 3)
        colors[i] = (2 if (values[0] > values[1]) else 1 if (values[0] < values[1]) else 0)
        ArraySort(values)
        canl[i] = values[0]
        cano[i] = (values[1] if (open[i] > close[i]) else values[2])
        canc[i] = (values[1] if (open[i] < close[i]) else values[2])
        canh[i] = values[3]
        i += 1
    return i

def iCorrelation(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == cor_pea:
        return iPearson(price, _int(length), r, bars, instanceNo)
    elif _sw1 == cor_spe:
        return iSpearman(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iPearson(value, period, i, bars, instanceNo=0):
    if ArrayRange(workPearson, 0) != bars:
        ArrayResize(workPearson, bars)
    workPearson[i][instanceNo] = value
    SumXY = 0.0
    SumXX = 0.0
    SumYY = 0.0
    SumY = 0.0
    SumX = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        val = workPearson[i - k][instanceNo]
        SumX += val
        SumY += k
        SumXX += val * val
        SumYY += k * k
        SumXY += val * k
        k += 1
    SXY = (period * SumXY) - (SumY * SumX)
    SXXYY = ((period * SumXX) - (SumX * SumX)) * ((period * SumYY) - (SumY * SumY))
    result = (_fdiv(-SXY, MathSqrt(MathAbs(SXXYY))) if (SXXYY != 0) else 0)
    return result

def iSpearman(value, period, i, bars, instanceNo=0):
    if ArrayRange(workSpearman, 0) != bars:
        ArrayResize(workSpearman, bars)
    workSpearman[i][instanceNo] = value
    total = 0.0
    data = Arr(0, 0.0)
    ArrayResize(data, period)
    ArrayInitialize(data, 0)
    k = 0
    while k < period and (i - k) >= 0:
        data[k] = workSpearman[i - k][instanceNo]
        k += 1
    for k in range(0, period):
        max_ = ArrayMaximum(data)
        total += (max_ - k) * (max_ - k)
        data[max_] = 0.0
    return 1.0 - _fdiv(6.0 * total, period * ((period * period) - 1.0))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrelationCandles(_MQL5Indicator):
    name = 'Correlation_candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CorPeriod': 32,  # Correlation rank
        'CorType': _Choice({0: 'Spearman rank correlation', 1: 'Pearson rank correlation'}, default=0),  # Correlation type
    }
    y_range = (-1.0, 1.0)

