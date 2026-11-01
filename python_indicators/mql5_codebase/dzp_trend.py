"""DZP_Trend — converted from MQL5: MQL5 Indicators/DZP_Trend/DZP_Trend.mq5

DZP Trend oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 10}, 'colors': {1: [32768], 2: [32768, 255, 11119017]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DZP', 2: 'DZP'}, 'levels': [], 'description': ['DZP Trend oscillator'], 'name': 'DZP_Trend', 'source': 'MQL5 Indicators/DZP_Trend/DZP_Trend.mq5', 'folder': 'DZP_Trend', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'uint', 'default': 22, 'label': 'Shift', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpViewMode', 'py': 'InpViewMode', 'param': 'InpViewMode', 'type': 'int', 'default': 1, 'label': 'Mode view', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE_VIEW
MODE_LINE = 1
MODE_HIST = 10
_enum('ENUM_MODE_VIEW', {1: 'MODE_LINE', 10: 'MODE_HIST'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpShift = _input('InpShift', 22)  # Shift
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpViewMode = _input('InpViewMode', MODE_LINE)  # Mode view
BufferLine = Arr(0, 0.0)
BufferDZP = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
period = 0
shift = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, period, shift
    period = (1 if (InpPeriod < 1) else InpPeriod)
    shift = (1 if (InpShift < 1) else InpShift)
    SetIndexBuffer(0, BufferLine, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDZP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DZP Trend (' + _str(period) + ',' + _str(shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    if InpViewMode == MODE_LINE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_COLOR_HISTOGRAM)
    ArraySetAsSeries(BufferLine, True)
    ArraySetAsSeries(BufferDZP, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferMA1, True)
    ResetLastError()
    handle_maP = iMA(None, PERIOD_CURRENT, period, 0, MODE_EMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(shift, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - shift - 2
        ArrayInitialize(BufferLine, EMPTY_VALUE)
        ArrayInitialize(BufferDZP, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        EMA0 = BufferMAP[i]
        EMAS = BufferMAP[i + shift]
        Pr0 = BufferMA1[i]
        PrS = BufferMA1[i + shift]
        if PrS != 0 and EMAS != 0:
            A = _fdiv(Pr0 - PrS, PrS)
            B = _fdiv(EMA0 - EMAS, EMAS)
            BufferDZP[i] = 100.0 * (A - B)
            BufferLine[i] = BufferDZP[i]
        else:
            BufferDZP[i] = 0.0
            BufferLine[i] = BufferDZP[i]
        BufferColors[i] = (0 if (BufferDZP[i] > BufferDZP[i + 1]) else 1 if (BufferDZP[i] < BufferDZP[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DZPTrend(_MQL5Indicator):
    name = 'DZP_Trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpShift': 22,  # Shift
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpViewMode': _Choice({1: 'Line', 10: 'Histogram'}, default=1),  # Mode view
    }

