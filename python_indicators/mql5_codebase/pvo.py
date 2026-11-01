"""PVO — converted from MQL5: MQL5 Indicators/PVO/PVO.mq5

Percentage Volume Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [16711935], 2: [16711680], 3: [32768, 255, 11119017]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'PVO', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['Percentage Volume Oscillator'], 'name': 'PVO', 'source': 'MQL5 Indicators/PVO/PVO.mq5', 'folder': 'PVO', 'inputs': [{'mql': 'InpShowHist', 'py': 'InpShowHist', 'param': 'InpShowHist', 'type': 'int', 'default': 1, 'label': 'Show histogram', 'sinput': False}, {'mql': 'InpShowPVO', 'py': 'InpShowPVO', 'param': 'InpShowPVO', 'type': 'int', 'default': 1, 'label': 'Show PVO', 'sinput': False}, {'mql': 'InpShowSig', 'py': 'InpShowSig', 'param': 'InpShowSig', 'type': 'int', 'default': 1, 'label': 'Show Signal', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpMethodFast', 'py': 'InpMethodFast', 'param': 'InpMethodFast', 'type': 'int', 'default': 1, 'label': 'Fast MA method', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpMethodSlow', 'py': 'InpMethodSlow', 'param': 'InpMethodSlow', 'type': 'int', 'default': 1, 'label': 'Slow MA method', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 1, 'label': 'Signal method', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Calculation mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_MODE
MODE_ABS = 0
MODE_RLT = 1
_enum('ENUM_MODE', {0: 'MODE_ABS', 1: 'MODE_RLT'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpShowHist = _input('InpShowHist', INPUT_YES)  # Show histogram
InpShowPVO = _input('InpShowPVO', INPUT_YES)  # Show PVO
InpShowSig = _input('InpShowSig', INPUT_YES)  # Show Signal
InpPeriodFast = _input('InpPeriodFast', 12)  # Fast MA period
InpMethodFast = _input('InpMethodFast', MODE_EMA)  # Fast MA method
InpPeriodSlow = _input('InpPeriodSlow', 26)  # Slow MA period
InpMethodSlow = _input('InpMethodSlow', MODE_EMA)  # Slow MA method
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal period
InpMethodSig = _input('InpMethodSig', MODE_EMA)  # Signal method
InpMode = _input('InpMode', MODE_ABS)  # Calculation mode
BufferPVO = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferAvgFVol = Arr(0, 0.0)
BufferAvgSVol = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_sig = 0
period_max = 0
weight_sum = 0

def OnInit():
    global period_fma, period_max, period_sig, period_sma
    period_fma = (2 if (InpPeriodFast < 2) else InpPeriodFast)
    period_sma = ((period_fma + 1) if (InpPeriodSlow == period_fma) else 2 if (InpPeriodSlow < 2) else InpPeriodSlow)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    period_max = fmax(period_fma, period_sma)
    SetIndexBuffer(0, BufferPVO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgFVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgSVol, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PVO (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowPVO else DRAW_NONE))
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowSig else DRAW_NONE))
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, (DRAW_COLOR_HISTOGRAM if InpShowHist else DRAW_NONE))
    ArraySetAsSeries(BufferPVO, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferAvgFVol, True)
    ArraySetAsSeries(BufferAvgSVol, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferPVO, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferAvgFVol, 0)
        ArrayInitialize(BufferAvgSVol, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
    _sw1 = InpMethodFast
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_max, period_fma, BufferVol, BufferAvgFVol) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_max, period_fma, BufferVol, BufferAvgFVol) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_max, period_fma, BufferVol, BufferAvgFVol, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_max, period_fma, BufferVol, BufferAvgFVol) == 0:
            return 0
    _sw2 = InpMethodSlow
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_max, period_sma, BufferVol, BufferAvgSVol) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_max, period_sma, BufferVol, BufferAvgSVol) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_max, period_sma, BufferVol, BufferAvgSVol, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_max, period_sma, BufferVol, BufferAvgSVol) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        fma = BufferAvgFVol[i]
        sma = BufferAvgSVol[i]
        BufferPVO[i] = ((fma - sma) if (InpMode == MODE_ABS) else _fdiv(100.0 * (fma - sma), sma) if (sma != 0) else 0)
    _sw3 = InpMethodSig
    if _sw3 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferPVO, BufferSignal) == 0:
            return 0
    elif _sw3 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferPVO, BufferSignal) == 0:
            return 0
    elif _sw3 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_max, period_sig, BufferPVO, BufferSignal, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferPVO, BufferSignal) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferHist[i] = BufferPVO[i] - BufferSignal[i]
        BufferColors[i] = (0 if (BufferHist[i] > BufferHist[i + 1]) else 1 if (BufferHist[i] < BufferHist[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PVO(_MQL5Indicator):
    name = 'PVO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpShowHist': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show histogram
        'InpShowPVO': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show PVO
        'InpShowSig': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Signal
        'InpPeriodFast': 12,  # Fast MA period
        'InpMethodFast': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Fast MA method
        'InpPeriodSlow': 26,  # Slow MA period
        'InpMethodSlow': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Slow MA method
        'InpPeriodSig': 9,  # Signal period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Signal method
        'InpMode': _Choice({0: 'Absolute', 1: 'Relative'}, default=0),  # Calculation mode
    }

