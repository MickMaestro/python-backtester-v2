"""Trendless_OS — converted from MQL5: MQL5 Indicators/Trendless_OS/Trendless_OS.mq5

Trendless OS DiNapoli indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11829830, 32768, 15570276, 6333684, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrendLess'}, 'levels': [], 'description': ['Trendless OS DiNapoli indicator'], 'name': 'Trendless_OS', 'source': 'MQL5 Indicators/Trendless_OS/Trendless_OS.mq5', 'folder': 'Trendless_OS', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 7, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 47.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -47.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpTypeDrawing', 'py': 'InpTypeDrawing', 'param': 'InpTypeDrawing', 'type': 'int', 'default': 10, 'label': 'Drawing type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 11829830  # #property indicator_color1
indicator_width1 = 2  # #property indicator_width1

# enum ENUM_TYPE_DRAWING
TYPE_DRAWING_LINE = 1
TYPE_DRAWING_HIST = 10
_enum('ENUM_TYPE_DRAWING', {1: 'TYPE_DRAWING_LINE', 10: 'TYPE_DRAWING_HIST'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 7)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 47.0)  # Overbought
InpOversold = _input('InpOversold', -47.0)  # Oversold
InpTypeDrawing = _input('InpTypeDrawing', TYPE_DRAWING_HIST)  # Drawing type
BufferTL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
overbought06 = 0.0
overbought08 = 0.0
overbought0 = 0.0
oversold0 = 0.0
oversold08 = 0.0
oversold06 = 0.0
period_ma = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, overbought0, overbought06, overbought08, oversold0, oversold06, oversold08, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = InpOverbought * 10.0 * Point()
    oversold = fabs(InpOversold * 10.0 * Point())
    overbought0 = ((10 * Point()) if (overbought < (10 * Point())) else overbought)
    overbought08 = overbought0 * 0.8
    overbought06 = overbought0 * 0.6
    oversold0 = ((10 * Point()) if (oversold < (10 * Point())) else oversold) * -1.0
    oversold08 = oversold0 * 0.8
    oversold06 = oversold0 * 0.6
    SetIndexBuffer(0, BufferTL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trendless OS (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overbought08)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, overbought06)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, oversold0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, oversold08)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, oversold06)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, InpTypeDrawing)
    if InpTypeDrawing == TYPE_DRAWING_LINE:
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, indicator_color1)
        PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 1)
    else:
        PlotIndexSetInteger(0, PLOT_LINE_WIDTH, indicator_width1)
    ArraySetAsSeries(BufferTL, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferTL, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 0)
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
        BufferTL[i] = BufferMA1[i] - BufferMAP[i]
        BufferColors[i] = (4 if (BufferTL[i] > overbought0 or BufferTL[i] < oversold0) else 3 if ((BufferTL[i] <= overbought0 and BufferTL[i] > overbought08) or (BufferTL[i] >= oversold0 and BufferTL[i] < oversold08)) else 2 if ((BufferTL[i] <= overbought08 and BufferTL[i] > overbought06) or (BufferTL[i] >= oversold08 and BufferTL[i] < oversold06)) else 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendlessOS(_MQL5Indicator):
    name = 'Trendless_OS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 7,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 47.0,  # Overbought
        'InpOversold': -47.0,  # Oversold
        'InpTypeDrawing': _Choice({1: 'Line', 10: 'Histogram'}, default=10),  # Drawing type
    }

