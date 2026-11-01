"""iMax3 — converted from MQL5: MQL5 Indicators/iMax3/iMax3.mq5

iMAX3 - Fast Trend Detector
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [32768], 2: [255], 3: [4163021], 4: [14524637], 5: [8421504], 6: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'HPX0', 2: 'HPX1', 3: 'HP0', 4: 'HP1', 5: 'IMAX0', 6: 'IMAX1'}, 'levels': [], 'description': ['iMAX3 - Fast Trend Detector'], 'name': 'iMax3', 'source': 'MQL5 Indicators/iMax3/iMax3.mq5', 'folder': 'iMax3', 'inputs': [{'mql': 'InpStepHP', 'py': 'InpStepHP', 'param': 'InpStepHP', 'type': 'double', 'default': 0.0, 'label': 'Step', 'sinput': False}, {'mql': 'InpAutoStep', 'py': 'InpAutoStep', 'param': 'InpAutoStep', 'type': 'int', 'default': 1, 'label': 'Auto step mode', 'sinput': False}, {'mql': 'InpModeIMAX', 'py': 'InpModeIMAX', 'param': 'InpModeIMAX', 'type': 'int', 'default': 1, 'label': 'Use iMAX mode', 'sinput': False}, {'mql': 'InpModeHP', 'py': 'InpModeHP', 'param': 'InpModeHP', 'type': 'int', 'default': 1, 'label': 'Use HP mode', 'sinput': False}, {'mql': 'InpModeHPX', 'py': 'InpModeHPX', 'param': 'InpModeHPX', 'type': 'int', 'default': 1, 'label': 'Use HPX mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpStepHP = _input('InpStepHP', 0.0)  # Step
InpAutoStep = _input('InpAutoStep', INPUT_YES)  # Auto step mode
InpModeIMAX = _input('InpModeIMAX', INPUT_YES)  # Use iMAX mode
InpModeHP = _input('InpModeHP', INPUT_YES)  # Use HP mode
InpModeHPX = _input('InpModeHPX', INPUT_YES)  # Use HPX mode
BufferHPX0 = Arr(0, 0.0)
BufferHPX1 = Arr(0, 0.0)
BufferHP0 = Arr(0, 0.0)
BufferHP1 = Arr(0, 0.0)
BufferIMAX0 = Arr(0, 0.0)
BufferIMAX1 = Arr(0, 0.0)
step = 0.0
digits = 0

def OnInit():
    global digits, step
    step = (fabs(InpStepHP) if (not InpAutoStep) else GetStep())
    digits = Digits()
    SetIndexBuffer(0, BufferHPX0, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHPX1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHP0, INDICATOR_DATA)
    SetIndexBuffer(3, BufferHP1, INDICATOR_DATA)
    SetIndexBuffer(4, BufferIMAX0, INDICATOR_DATA)
    SetIndexBuffer(5, BufferIMAX1, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iMAX3 (' + DoubleToString(step, 5) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, InpModeHPX)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, InpModeHPX)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpModeHP)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpModeHP)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, InpModeIMAX)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, InpModeIMAX)
    ArraySetAsSeries(BufferHPX0, True)
    ArraySetAsSeries(BufferHPX1, True)
    ArraySetAsSeries(BufferHP0, True)
    ArraySetAsSeries(BufferHP1, True)
    ArraySetAsSeries(BufferIMAX0, True)
    ArraySetAsSeries(BufferIMAX1, True)
    ChartRedraw()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 4
        ArrayInitialize(BufferHPX0, EMPTY_VALUE)
        ArrayInitialize(BufferHPX1, EMPTY_VALUE)
        ArrayInitialize(BufferHP0, EMPTY_VALUE)
        ArrayInitialize(BufferHP1, EMPTY_VALUE)
        ArrayInitialize(BufferIMAX0, EMPTY_VALUE)
        ArrayInitialize(BufferIMAX1, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferHPX1[i] = NormalizeDouble((0.13785 * (high[i] + low[i] - ((high[i + 1] + low[i + 1]) / 2.0))) + (0.0007 * (high[i + 1] + low[i + 1] - ((high[i + 2] + low[i + 2]) / 2.0))) + (0.13785 * (high[i + 2] + low[i + 2] - ((high[i + 3] + low[i + 3]) / 2.0))) + (1.2103 * BufferHPX0[i + 1]) - (0.4867 * BufferHPX0[i + 2]), digits)
        BufferHPX0[i] = ((BufferHPX1[i] + step) if (close[i] > BufferHPX1[i]) else (BufferHPX1[i] - step))
        BufferIMAX0[i] = NormalizeDouble((0.13785 * (high[i] + low[i] - ((high[i + 1] + low[i + 1]) / 2.0))) + (0.0007 * (high[i + 1] + low[i + 1] - ((high[i + 2] + low[i + 2]) / 2.0))) + (0.13785 * (high[i + 2] + low[i + 2] - ((high[i + 3] + low[i + 3]) / 2.0))) + (1.2103 * BufferIMAX0[i + 1]) - (0.4867 * BufferIMAX0[i + 2]), digits)
        BufferHP1[i] = BufferIMAX0[i]
        BufferIMAX1[i] = BufferIMAX0[i + 1]
        BufferHP0[i] = ((BufferIMAX0[i] + step) if (close[i] > BufferIMAX0[i]) else (BufferIMAX0[i] - step))
    return rates_total

def GetStep():
    return (0.0001 if (Period() < PERIOD_M5) else 0.00015 if (Period() < PERIOD_M15) else 0.0003 if (Period() < PERIOD_M30) else 0.0005 if (Period() < PERIOD_H1) else 0.00075 if (Period() < PERIOD_H4) else 0.0015 if (Period() < PERIOD_D1) else 0.003 if (Period() < PERIOD_W1) else 0.005 if (Period() < PERIOD_MN1) else 0.01)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IMax3(_MQL5Indicator):
    name = 'iMax3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStepHP': 0.0,  # Step
        'InpAutoStep': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Auto step mode
        'InpModeIMAX': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use iMAX mode
        'InpModeHP': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use HP mode
        'InpModeHPX': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use HPX mode
    }

