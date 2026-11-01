"""Time_Averaged_Price — converted from MQL5: MQL5 Indicators/Time_Averaged_Price/Time_Averaged_Price.mq5

Time Averaged Price
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TAP'}, 'levels': [], 'description': ['Time Averaged Price'], 'name': 'Time_Averaged_Price', 'source': 'MQL5 Indicators/Time_Averaged_Price/Time_Averaged_Price.mq5', 'folder': 'Time_Averaged_Price', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTAP = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferTAP, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Time Averaged Price (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTAP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferTAP, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period, i)
        bl = Lowest(period, i)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        max_ = high[bh]
        min_ = low[bl]
        BufferTAP[i] = (close[i + period - 1] if (InpAppliedPrice == PRICE_CLOSE) else open[i + period - 1] if (InpAppliedPrice == PRICE_OPEN) else max_ if (InpAppliedPrice == PRICE_HIGH) else min_ if (InpAppliedPrice == PRICE_LOW) else ((max_ + min_) / 2.0) if (InpAppliedPrice == PRICE_MEDIAN) else ((max_ + min_ + close[i]) / 3.0) if (InpAppliedPrice == PRICE_TYPICAL) else ((max_ + min_ + (2.0 * close[i])) / 4.0))
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


class TimeAveragedPrice(_MQL5Indicator):
    name = 'Time_Averaged_Price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

