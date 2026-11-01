"""RSI Custom Smoothing — converted from MQL5: MQL5 Indicators/RSI Custom Smoothing/RSI Custom Smoothing.mq5

Relative Strength Index smoothing
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Relative Strength Index smoothing'], 'name': 'RSI Custom Smoothing', 'source': 'MQL5 Indicators/RSI Custom Smoothing/RSI Custom Smoothing.mq5', 'folder': 'RSI Custom Smoothing', 'inputs': [{'mql': 'Inp_RSI_Period', 'py': 'Inp_RSI_Period', 'param': 'Inp_RSI_Period', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'Inp_RSI_Color', 'py': 'Inp_RSI_Color', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Color line', 'sinput': False}, {'mql': 'Inp_RSI_Width', 'py': 'Inp_RSI_Width', 'param': 'Inp_RSI_Width', 'type': 'int', 'default': 1, 'label': 'Width', 'sinput': False}, {'mql': 'Inp_RSI_Level1', 'py': 'Inp_RSI_Level1', 'param': 'Inp_RSI_Level1', 'type': 'int', 'default': 30, 'label': 'Value Level #1', 'sinput': False}, {'mql': 'Inp_RSI_Level2', 'py': 'Inp_RSI_Level2', 'param': 'Inp_RSI_Level2', 'type': 'double', 'default': 70.0, 'label': 'Value Level #2', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Inp_RSI_Period = _input('Inp_RSI_Period', 14)  # Period
Inp_RSI_Color = _input('Inp_RSI_Color', clrDodgerBlue)  # Color line
Inp_RSI_Width = _input('Inp_RSI_Width', 1)  # Width
Inp_RSI_Level1 = _input('Inp_RSI_Level1', _int(30.0))  # Value Level #1
Inp_RSI_Level2 = _input('Inp_RSI_Level2', 70.0)  # Value Level #2
ExtRSIBufferSmoothing = Arr(0, 0.0)
ExtRSIBuffer = Arr(0, 0.0)
ExtPosBuffer = Arr(0, 0.0)
ExtNegBuffer = Arr(0, 0.0)
ExtPeriodRSI = 0

def OnInit():
    global ExtPeriodRSI
    if Inp_RSI_Period < 1:
        ExtPeriodRSI = 12
        Print('Incorrect value for input variable Inp_RSI_Period =', Inp_RSI_Period, 'Indicator will use value =', ExtPeriodRSI, 'for calculations.')
    else:
        ExtPeriodRSI = Inp_RSI_Period
    SetIndexBuffer(0, ExtRSIBufferSmoothing, INDICATOR_DATA)
    SetIndexBuffer(1, ExtRSIBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtPosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtNegBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, Inp_RSI_Color)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, Inp_RSI_Width)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_RSI_Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_RSI_Level2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodRSI)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI(' + _str(ExtPeriodRSI) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    diff = 0.0
    if rates_total <= ExtPeriodRSI:
        return 0
    pos = prev_calculated - 1
    if pos <= ExtPeriodRSI:
        ExtRSIBuffer[0] = 0.0
        ExtPosBuffer[0] = 0.0
        ExtNegBuffer[0] = 0.0
        SumP = 0.0
        SumN = 0.0
        i = 1
        for i in range(i, ExtPeriodRSI + 1):
            ExtRSIBuffer[i] = 0.0
            ExtPosBuffer[i] = 0.0
            ExtNegBuffer[i] = 0.0
            diff = price[i] - price[i - 1]
            SumP += (diff if (diff > 0) else 0)
            SumN += ((-diff) if (diff < 0) else 0)
        else:
            i = _range_end(i, ExtPeriodRSI + 1, 1)
        ExtPosBuffer[ExtPeriodRSI] = _fdiv(SumP, ExtPeriodRSI)
        ExtNegBuffer[ExtPeriodRSI] = _fdiv(SumN, ExtPeriodRSI)
        if ExtNegBuffer[ExtPeriodRSI] != 0.0:
            ExtRSIBuffer[ExtPeriodRSI] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(ExtPosBuffer[ExtPeriodRSI], ExtNegBuffer[ExtPeriodRSI]))
        else:
            if ExtPosBuffer[ExtPeriodRSI] != 0.0:
                ExtRSIBuffer[ExtPeriodRSI] = 100.0
            else:
                ExtRSIBuffer[ExtPeriodRSI] = 50.0
        pos = ExtPeriodRSI + 1
    i = pos
    for i in range(i, rates_total):
        diff = price[i] - price[i - 1]
        ExtPosBuffer[i] = _fdiv((ExtPosBuffer[i - 1] * (ExtPeriodRSI - 1)) + (diff if (diff > 0.0) else 0.0), ExtPeriodRSI)
        ExtNegBuffer[i] = _fdiv((ExtNegBuffer[i - 1] * (ExtPeriodRSI - 1)) + ((-diff) if (diff < 0.0) else 0.0), ExtPeriodRSI)
        if ExtNegBuffer[i] != 0.0:
            ExtRSIBuffer[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(ExtPosBuffer[i], ExtNegBuffer[i]))
        else:
            if ExtPosBuffer[i] != 0.0:
                ExtRSIBuffer[i] = 100.0
            else:
                ExtRSIBuffer[i] = 50.0
    else:
        i = _range_end(i, rates_total, 1)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, 6, ExtRSIBuffer, ExtRSIBufferSmoothing)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSICustomSmoothing(_MQL5Indicator):
    name = 'RSI Custom Smoothing'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_RSI_Period': 14,  # Period
        'Inp_RSI_Width': 1,  # Width
        'Inp_RSI_Level1': 30,  # Value Level #1
        'Inp_RSI_Level2': 70.0,  # Value Level #2
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 100.0)

