"""TRIX ARROWS — converted from MQL5: MQL5 Indicators/TRIX ARROWS/TRIX ARROWS.mq5

Triple Exponential Average + signal period + arrows
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.004

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.004', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [255], 2: [16711680], 3: [16711680], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'TRIX', 2: 'Signal', 3: 'Arrows Up', 4: 'Arrows Down'}, 'levels': [], 'description': ['Triple Exponential Average + signal period + arrows'], 'name': 'TRIX ARROWS', 'source': 'MQL5 Indicators/TRIX ARROWS/TRIX ARROWS.mq5', 'folder': 'TRIX ARROWS', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpSignalPeriod', 'py': 'InpSignalPeriod', 'param': 'InpSignalPeriod', 'type': 'int', 'default': 8, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpCodeUp', 'py': 'InpCodeUp', 'param': 'InpCodeUp', 'type': 'ushort', 'default': 233, 'label': 'Symbol code up', 'sinput': False}, {'mql': 'InpCodeDown', 'py': 'InpCodeDown', 'param': 'InpCodeDown', 'type': 'ushort', 'default': 234, 'label': 'Symbol code down', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
InpSignalPeriod = _input('InpSignalPeriod', 8)  # Signal period
InpCodeUp = _input('InpCodeUp', 233)  # Symbol code up
InpCodeDown = _input('InpCodeDown', 234)  # Symbol code down
TRIX_Buffer = Arr(0, 0.0)
Signal_Buffer = Arr(0, 0.0)
Arrows_Buffer_Up = Arr(0, 0.0)
Arrows_Buffer_Down = Arr(0, 0.0)
EMA_TRIX = Arr(0, 0.0)
SecondEMA_TRIX = Arr(0, 0.0)
ThirdEMA_TRIX = Arr(0, 0.0)
EMA_Signal = Arr(0, 0.0)
SecondEMA_Signal = Arr(0, 0.0)
ThirdEMA_Signal = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, TRIX_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (3 * InpPeriodEMA) - 3)
    PlotIndexSetString(0, PLOT_LABEL, 'TRIX(' + _str(InpPeriodEMA) + ')')
    SetIndexBuffer(1, Signal_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, (3 * InpSignalPeriod) - 3)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal(' + _str(InpSignalPeriod) + ')')
    SetIndexBuffer(2, Arrows_Buffer_Up, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, InpCodeUp)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, Arrows_Buffer_Down, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, InpCodeDown)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, EMA_TRIX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, SecondEMA_TRIX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ThirdEMA_TRIX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, EMA_Signal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, SecondEMA_Signal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, ThirdEMA_Signal, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRIX(' + _str(InpPeriodEMA) + '), Signal(' + _str(InpSignalPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ((3 * InpPeriodEMA) - 3) or rates_total < ((3 * InpSignalPeriod) - 3):
        return 0
    limit_TRIX = 0
    limit_Signal = 0
    limit_Arrows = 0
    if prev_calculated == 0:
        limit_TRIX = 3 * (InpPeriodEMA - 1)
        for i in range(0, limit_TRIX):
            TRIX_Buffer[i] = EMPTY_VALUE
        limit_Signal = 3 * (InpSignalPeriod - 1)
        for i in range(0, limit_Signal):
            Signal_Buffer[i] = EMPTY_VALUE
        limit_Arrows = 0
    else:
        limit_Arrows = prev_calculated - 1
        limit_Signal = limit_Arrows
        limit_TRIX = limit_Signal
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriodEMA, price, EMA_TRIX)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpPeriodEMA - 1, InpPeriodEMA, EMA_TRIX, SecondEMA_TRIX)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (2 * InpPeriodEMA) - 2, InpPeriodEMA, SecondEMA_TRIX, ThirdEMA_TRIX)
    for i in range(limit_TRIX, rates_total):
        if ThirdEMA_TRIX[i - 1] != 0.0:
            TRIX_Buffer[i] = _fdiv(ThirdEMA_TRIX[i] - ThirdEMA_TRIX[i - 1], ThirdEMA_TRIX[i - 1])
        else:
            TRIX_Buffer[i] = 0.0
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpSignalPeriod, price, EMA_Signal)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpSignalPeriod - 1, InpSignalPeriod, EMA_Signal, SecondEMA_Signal)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (2 * InpSignalPeriod) - 2, InpSignalPeriod, SecondEMA_Signal, ThirdEMA_Signal)
    for i in range(limit_Signal, rates_total):
        if ThirdEMA_Signal[i - 1] != 0.0:
            Signal_Buffer[i] = _fdiv(ThirdEMA_Signal[i] - ThirdEMA_Signal[i - 1], ThirdEMA_Signal[i - 1])
        else:
            Signal_Buffer[i] = 0.0
    for i in range(limit_Arrows, rates_total):
        if i > 0:
            if Signal_Buffer[i - 1] < TRIX_Buffer[i - 1] and Signal_Buffer[i] > TRIX_Buffer[i]:
                Arrows_Buffer_Up[i] = TRIX_Buffer[i]
            else:
                Arrows_Buffer_Up[i] = 0.0
            if Signal_Buffer[i - 1] > TRIX_Buffer[i - 1] and Signal_Buffer[i] < TRIX_Buffer[i]:
                Arrows_Buffer_Down[i] = TRIX_Buffer[i]
            else:
                Arrows_Buffer_Down[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TRIXARROWS(_MQL5Indicator):
    name = 'TRIX ARROWS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'InpSignalPeriod': 8,  # Signal period
        'InpCodeUp': 233,  # Symbol code up
        'InpCodeDown': 234,  # Symbol code down
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

