"""Mean_Reversion — converted from MQL5: MQL5 Indicators/Mean_Reversion/Mean_Reversion.mq5

Mean reversion indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680], 4: [42495]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Highest', 2: 'Lowest', 3: 'Median', 4: 'MovAvg'}, 'levels': [], 'description': ['Mean reversion indicator'], 'name': 'Mean_Reversion', 'source': 'MQL5 Indicators/Mean_Reversion/Mean_Reversion.mq5', 'folder': 'Mean_Reversion', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Range', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 50, 'label': 'MA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Range
InpPeriodMA = _input('InpPeriodMA', 50)  # MA period
BufferDU = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferDM = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period = 0
period_ma = 0
period_max = 0
handle_ma = 0

def OnInit():
    global handle_ma, period, period_ma, period_max
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_max = fmax(period, period_ma)
    SetIndexBuffer(0, BufferDU, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDM, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mean reversion (' + _str(period) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'Highest at ' + _str(period))
    PlotIndexSetString(1, PLOT_LABEL, 'Lowest at ' + _str(period))
    PlotIndexSetString(2, PLOT_LABEL, 'Median at ' + _str(period))
    PlotIndexSetString(3, PLOT_LABEL, 'MovAvg ' + _str(period_ma))
    ArraySetAsSeries(BufferDU, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferDM, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferDU, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferDM, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferDN[i] = min_
        BufferDU[i] = max_
        BufferDM[i] = (min_ + max_) / 2.0
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


class MeanReversion(_MQL5Indicator):
    name = 'Mean_Reversion'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Range
        'InpPeriodMA': 50,  # MA period
    }

