"""Sylvain_Vervoort_rainbow_moving_average — converted from MQL5: MQL5 Indicators/Sylvain_Vervoort_rainbow_moving_average/Sylvain_Vervoort_rainbow_moving_average.mq5

Sylvain Vervoort rainbow moving average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SVRMA'}, 'levels': [], 'description': ['Sylvain Vervoort rainbow moving average'], 'name': 'Sylvain_Vervoort_rainbow_moving_average', 'source': 'MQL5 Indicators/Sylvain_Vervoort_rainbow_moving_average/Sylvain_Vervoort_rainbow_moving_average.mq5', 'folder': 'Sylvain_Vervoort_rainbow_moving_average', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 2, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 2)  # Period
BufferSVRMA = Arr(0, 0.0)
BufferLWMA1 = Arr(0, 0.0)
BufferLWMA2 = Arr(0, 0.0)
BufferLWMA3 = Arr(0, 0.0)
BufferLWMA4 = Arr(0, 0.0)
BufferLWMA5 = Arr(0, 0.0)
BufferLWMA6 = Arr(0, 0.0)
BufferLWMA7 = Arr(0, 0.0)
BufferLWMA8 = Arr(0, 0.0)
BufferLWMA9 = Arr(0, 0.0)
BufferLWMA10 = Arr(0, 0.0)
period_ma = 0
period_max = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, period_max
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    period_max = period_ma + (period_ma * 9)
    SetIndexBuffer(0, BufferSVRMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLWMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferLWMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferLWMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferLWMA4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferLWMA5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferLWMA6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferLWMA7, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferLWMA8, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferLWMA9, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferLWMA10, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Sylvain Vervoort rainbow MA (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    ArraySetAsSeries(BufferSVRMA, True)
    ArraySetAsSeries(BufferLWMA1, True)
    ArraySetAsSeries(BufferLWMA2, True)
    ArraySetAsSeries(BufferLWMA3, True)
    ArraySetAsSeries(BufferLWMA4, True)
    ArraySetAsSeries(BufferLWMA5, True)
    ArraySetAsSeries(BufferLWMA6, True)
    ArraySetAsSeries(BufferLWMA7, True)
    ArraySetAsSeries(BufferLWMA8, True)
    ArraySetAsSeries(BufferLWMA9, True)
    ArraySetAsSeries(BufferLWMA10, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferSVRMA, EMPTY_VALUE)
        ArrayInitialize(BufferLWMA1, 0)
        ArrayInitialize(BufferLWMA2, 0)
        ArrayInitialize(BufferLWMA3, 0)
        ArrayInitialize(BufferLWMA4, 0)
        ArrayInitialize(BufferLWMA5, 0)
        ArrayInitialize(BufferLWMA6, 0)
        ArrayInitialize(BufferLWMA7, 0)
        ArrayInitialize(BufferLWMA8, 0)
        ArrayInitialize(BufferLWMA9, 0)
        ArrayInitialize(BufferLWMA10, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferLWMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferLWMA2[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA1)
        BufferLWMA3[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA2)
        BufferLWMA4[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA3)
        BufferLWMA5[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA4)
        BufferLWMA6[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA5)
        BufferLWMA7[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA6)
        BufferLWMA8[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA7)
        BufferLWMA9[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA8)
        BufferLWMA10[i] = LinearWeightedMA(rates_total, period_ma, i, BufferLWMA9)
        value = 0.0
        value += 5 * BufferLWMA1[i]
        value += 4 * BufferLWMA2[i]
        value += 3 * BufferLWMA3[i]
        value += 2 * BufferLWMA4[i]
        value += BufferLWMA5[i]
        value += BufferLWMA6[i]
        value += BufferLWMA7[i]
        value += BufferLWMA8[i]
        value += BufferLWMA9[i]
        value += BufferLWMA10[i]
        BufferSVRMA[i] = value / 20.0
    return rates_total

def LinearWeightedMA(rates_total, period, index, price):
    result = 0.0
    count = 0.0
    total = 0.0
    k = 0.0
    wsum = 0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    for j in range(index + period - 1, index - 1, -1):
        count += 1
        k += count
        total += price[j] * count
    result = _fdiv(total, k)
    return result


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SylvainVervoortRainbowMovingAverage(_MQL5Indicator):
    name = 'Sylvain_Vervoort_rainbow_moving_average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 2,  # Period
    }

