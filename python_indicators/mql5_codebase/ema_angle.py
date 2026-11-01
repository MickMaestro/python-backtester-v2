"""EMA_Angle — converted from MQL5: MQL5 Indicators/Simple oscillator showing the difference between two Moving Averages/EMA_Angle.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 65535]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'EMA Angle'}, 'levels': [], 'description': [''], 'name': 'EMA_Angle', 'source': 'MQL5 Indicators/Simple oscillator showing the difference between two Moving Averages/EMA_Angle.mq5', 'folder': 'Simple oscillator showing the difference between two Moving Averages', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 50, 'label': 'Period EMA', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'uint', 'default': 6, 'label': 'Shift of the second EMA', 'sinput': False}, {'mql': 'InpTreshold', 'py': 'InpTreshold', 'param': 'InpTreshold', 'type': 'double', 'default': 0.3, 'label': 'Treshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 50)  # Period EMA
InpShift = _input('InpShift', 6)  # Shift of the second EMA
InpTreshold = _input('InpTreshold', 0.3)  # Treshold
BufferEMA = Arr(0, 0.0)
BufferEMAColors = Arr(0, 0.0)
BufferTMP = Arr(0, 0.0)
period = 0
shift = 0
handle_ema = 0

def OnInit():
    global handle_ema, period, shift
    period = (1 if (InpPeriod < 1) else InpPeriod)
    shift = (1 if (InpShift == 0) else InpShift)
    handle_ema = iMA(None, 0, period, 0, MODE_EMA, PRICE_MEDIAN)
    if handle_ema == INVALID_HANDLE:
        Print('Failed to create an EMA handle')
        return INIT_FAILED
    SetIndexBuffer(0, BufferEMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferEMAColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferTMP, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, clrGreen)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, clrRed)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 2, clrYellow)
    params = '(' + _str(period) + ',' + _str(shift) + ',' + _str(InpTreshold) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMA Angle' + params)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period + shift + 1):
        return 0
    ArraySetAsSeries(BufferEMA, True)
    ArraySetAsSeries(BufferEMAColors, True)
    ArraySetAsSeries(BufferTMP, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - shift - 1
        ArrayInitialize(BufferEMA, 0.0)
        ArrayInitialize(BufferTMP, EMPTY_VALUE)
        copied = CopyBuffer(handle_ema, 0, 0, (1 if (limit == 0) else rates_total), BufferTMP)
        if copied < 1 or Point() == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        copied = CopyBuffer(handle_ema, 0, 0, (1 if (limit == 0) else rates_total), BufferTMP)
        if copied < 1 or Point() == 0:
            return 0
        ema0 = BufferTMP[i]
        ema1 = BufferTMP[i + shift]
        angle = _fdiv(ema0 - ema1, Point())
        BufferEMA[i] = angle
        if angle >= InpTreshold:
            BufferEMAColors[i] = 0.0
        elif angle <= (-InpTreshold):
            BufferEMAColors[i] = 1.0
        else:
            BufferEMAColors[i] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAAngle(_MQL5Indicator):
    name = 'EMA_Angle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 50,  # Period EMA
        'InpShift': 6,  # Shift of the second EMA
        'InpTreshold': 0.3,  # Treshold
    }

