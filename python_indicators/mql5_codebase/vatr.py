"""VATR — converted from MQL5: MQL5 Indicators/The volume based ATR indicator/VATR.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VATR'}, 'levels': [], 'description': [], 'name': 'VATR', 'source': 'MQL5 Indicators/The volume based ATR indicator/VATR.mq5', 'folder': 'The volume based ATR indicator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 14, 'label': 'Period of indicator', 'sinput': False}, {'mql': 'InpUseVolume', 'py': 'InpUseVolume', 'param': 'InpUseVolume', 'type': 'int', 'default': 1, 'label': 'Use volume:', 'sinput': False}, {'mql': 'InpTypeDrawing', 'py': 'InpTypeDrawing', 'param': 'InpTypeDrawing', 'type': 'int', 'default': 0, 'label': 'Type of indicator:', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_TYPE_DRAWING
DRAWING_TYPE_LINE = 0
DRAWING_TYPE_HISTOGRAMM = 1
_enum('ENUM_TYPE_DRAWING', {0: 'DRAWING_TYPE_LINE', 1: 'DRAWING_TYPE_HISTOGRAMM'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period of indicator
InpUseVolume = _input('InpUseVolume', INPUT_YES)  # Use volume:
InpTypeDrawing = _input('InpTypeDrawing', DRAWING_TYPE_LINE)  # Type of indicator:
BufferVATR = Arr(0, 0.0)
BufferTEMP = Arr(0, 0.0)
period_vatr = 0

def OnInit():
    global period_vatr
    period_vatr = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferVATR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTEMP, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, (DRAW_HISTOGRAM if InpTypeDrawing else DRAW_LINE))
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'VATR(' + _str(period_vatr) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period_vatr + 1):
        return 0
    ArraySetAsSeries(BufferTEMP, True)
    ArraySetAsSeries(BufferVATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVATR, 0.0)
        ArrayInitialize(BufferTEMP, 0.0)
    for i in range(limit, 0 - 1, -1):
        hl = high[i] - low[i]
        hc = fabs(high[i] - close[i + 1])
        lc = fabs(low[i] - close[i + 1])
        mn = fmin(fmin(hl, hc), lc)
        tmp = mn * (tick_volume[i] if InpUseVolume else 1.0)
        BufferTEMP[i] = (DBL_MIN if (tmp <= 0) else tmp)
    return SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_vatr, BufferTEMP, BufferVATR)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VATR(_MQL5Indicator):
    name = 'VATR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period of indicator
        'InpUseVolume': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use volume:
        'InpTypeDrawing': _Choice({0: 'Draw line', 1: 'Draw hictogramm'}, default=0),  # Type of indicator:
    }

