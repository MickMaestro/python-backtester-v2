"""Triggerlines — converted from MQL5: MQL5 Indicators/TriggerLines/Triggerlines.mq5

Triggerlines indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [32768, 255, 11119017], 2: [3329330, 17919, 11119017]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'WT', 2: 'Signal'}, 'levels': [], 'description': ['Triggerlines indicator'], 'name': 'Triggerlines', 'source': 'MQL5 Indicators/TriggerLines/Triggerlines.mq5', 'folder': 'TriggerLines', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 25, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 13, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 25)  # Period
InpPeriodSM = _input('InpPeriodSM', 13)  # Smoothing
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferWT = Arr(0, 0.0)
BufferColorsWT = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferColorsSignal = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
lv = 0.0
period1 = 0
period_sm = 0
period_max = 0
handle_ma = 0

def OnInit():
    global handle_ma, lv, period1, period_max, period_sm
    period1 = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodSM < 2) else InpPeriodSM)
    period_max = fmax(period1, period_sm)
    lv = (1.0 + period1) / 3.0
    SetIndexBuffer(0, BufferWT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColorsWT, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColorsSignal, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMA1, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Triggerlines (' + _str(period1) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_sm)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'WT(' + _str(period1) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Signal(' + _str(period_sm) + ')')
    ArraySetAsSeries(BufferWT, True)
    ArraySetAsSeries(BufferColorsWT, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferColorsSignal, True)
    ArraySetAsSeries(BufferMA1, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period1 - 1
        ArrayInitialize(BufferWT, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferMA1, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        for j in range(1, period1 + 1):
            sum_ += (j - lv) * BufferMA1[i + period1 - j]
        BufferWT[i] = _fdiv(6.0 * sum_, period1 * (period1 + 1.0))
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period1, period_sm, BufferWT, BufferSignal) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferWT[i] > BufferSignal[i]:
            BufferColorsWT[i] = 0.0
            BufferColorsSignal[i] = BufferColorsWT[i]
        elif BufferWT[i] < BufferSignal[i]:
            BufferColorsWT[i] = 1.0
            BufferColorsSignal[i] = BufferColorsWT[i]
        else:
            BufferColorsWT[i] = 2.0
            BufferColorsSignal[i] = BufferColorsWT[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Triggerlines(_MQL5Indicator):
    name = 'Triggerlines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 25,  # Period
        'InpPeriodSM': 13,  # Smoothing
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

