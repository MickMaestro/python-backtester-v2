"""Time_Averaged_MA — converted from MQL5: MQL5 Indicators/Time_Averaged_MA/Time_Averaged_MA.mq5

Time Averaged moving average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TAMA'}, 'levels': [], 'description': ['Time Averaged moving average'], 'name': 'Time_Averaged_MA', 'source': 'MQL5 Indicators/Time_Averaged_MA/Time_Averaged_MA.mq5', 'folder': 'Time_Averaged_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 15, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpPeriodMA = _input('InpPeriodMA', 15)  # Smoothing period
InpMethod = _input('InpMethod', MODE_SMA)  # Smoothing method
BufferTAMA = Arr(0, 0.0)
BufferTAP = Arr(0, 0.0)
period_ind = 0
period_sm = 0
weight_sum = 0

def OnInit():
    global period_ind, period_sm
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    SetIndexBuffer(0, BufferTAMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTAP)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Time Averaged MA (' + _str(period_ind) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTAMA, True)
    ArraySetAsSeries(BufferTAP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_ind, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 1
        ArrayInitialize(BufferTAMA, EMPTY_VALUE)
        ArrayInitialize(BufferTAP, 0)
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period_ind, i)
        bl = Lowest(period_ind, i)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        max_ = high[bh]
        min_ = low[bl]
        BufferTAP[i] = (close[i + period_ind - 1] if (InpAppliedPrice == PRICE_CLOSE) else open[i + period_ind - 1] if (InpAppliedPrice == PRICE_OPEN) else max_ if (InpAppliedPrice == PRICE_HIGH) else min_ if (InpAppliedPrice == PRICE_LOW) else ((max_ + min_) / 2.0) if (InpAppliedPrice == PRICE_MEDIAN) else ((max_ + min_ + close[i]) / 3.0) if (InpAppliedPrice == PRICE_TYPICAL) else ((max_ + min_ + (2.0 * close[i])) / 4.0))
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTAP, BufferTAMA)
    elif _sw1 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTAP, BufferTAMA)
    elif _sw1 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferTAP, BufferTAMA, _GlobRef(globals(), 'weight_sum'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTAP, BufferTAMA)
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeAveragedMA(_MQL5Indicator):
    name = 'Time_Averaged_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpPeriodMA': 15,  # Smoothing period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
    }

