"""cci_drawmode — converted from MQL5: MQL5 Indicators/CCI_DrawMode/cci_drawmode.mq5

Standard Commodity Channel Index indicator with different drawing modes
Copyright: Copyright 2012, Rone; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {2: 10}, 'colors': {1: [255, 32768], 2: [8421504, 32768, 3329330, 255, 17919]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'CCI Filling', 2: 'CCI'}, 'levels': [-100.0, 100.0], 'description': ['Standard Commodity Channel Index indicator with different drawing modes'], 'name': 'cci_drawmode', 'source': 'MQL5 Indicators/CCI_DrawMode/cci_drawmode.mq5', 'folder': 'CCI_DrawMode', 'inputs': [{'mql': 'InpCCIPeriod', 'py': 'InpCCIPeriod', 'param': 'InpCCIPeriod', 'type': 'int', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 2, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpConfirmationBars', 'py': 'InpConfirmationBars', 'param': 'InpConfirmationBars', 'type': 'int', 'default': 3, 'label': 'Confirmation (number of bars)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum DRAW_MODE
LINE = 0
FILLING = 1
HISTOGRAM = 2
_enum('DRAW_MODE', {0: 'LINE', 1: 'FILLING', 2: 'HISTOGRAM'})

# ---- inputs and global variables
InpCCIPeriod = _input('InpCCIPeriod', 14)  # CCI period
InpDrawMode = _input('InpDrawMode', HISTOGRAM)  # Drawing mode
InpConfirmationBars = _input('InpConfirmationBars', 3)  # Confirmation (number of bars)
ZeroLineBuffer = Arr(0, 0.0)
CCIBuffer = Arr(0, 0.0)
CCIColors = Arr(0, 0.0)
SMABuffer = Arr(0, 0.0)
ExtCCIPeriod = 0
ExtConfirmationBars = 0
minRequiredBars = 0

def OnInit():
    global ExtCCIPeriod, ExtConfirmationBars, minRequiredBars
    if InpCCIPeriod <= 0:
        ExtCCIPeriod = 14
        printf('Invalid parameter value "CCI period": %d. The value to be used: %d.', InpCCIPeriod, ExtCCIPeriod)
    else:
        ExtCCIPeriod = InpCCIPeriod
    minRequiredBars = (2 * ExtCCIPeriod) - 1
    if InpConfirmationBars < 0:
        ExtConfirmationBars = 3
        printf('Invalid parameter value "Confirmation": %d. The value to be used: %d.', InpConfirmationBars, ExtConfirmationBars)
    else:
        ExtConfirmationBars = InpConfirmationBars
    SetIndexBuffer(0, ZeroLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, CCIBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, CCIColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, SMABuffer, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
    if InpDrawMode == LINE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    elif InpDrawMode == FILLING:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_FILLING)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
    elif InpDrawMode == HISTOGRAM:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_COLOR_HISTOGRAM)
    shortname = Box("")
    StringConcatenate(shortname, 'CCI (', ExtCCIPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_counter_, minRequiredBars
    startBar = 0
    counter = 0
    multiplier = _fdiv(0.015, ExtCCIPeriod)
    minRequiredBars += begin
    if rates_total < minRequiredBars:
        Print('Insufficient data for calculation: ', rates_total, ' min: ', minRequiredBars, ' begin: ', begin)
        return 0
    if begin > 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, minRequiredBars)
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = ExtCCIPeriod - 1 + begin
        _s_OnCalculate_counter_ = 0
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        valueD = 0.0
        valueM = 0.0
        SMABuffer[bar] = SimpleMA(bar, ExtCCIPeriod, price)
        valueD = 0.0
        for shift in range(0, ExtCCIPeriod):
            valueD += MathAbs(price[bar - shift] - SMABuffer[bar])
        valueD *= multiplier
        valueM = price[bar] - SMABuffer[bar]
        if valueD != 0.0:
            CCIBuffer[bar] = _fdiv(valueM, valueD)
        else:
            CCIBuffer[bar] = 0.0
        ZeroLineBuffer[bar] = 0.0
    if InpDrawMode == HISTOGRAM:
        counter = _s_OnCalculate_counter_
        for bar in range(startBar, rates_total):
            prevBar = bar - 1
            if rates_total != prev_calculated and bar == (rates_total - 1):
                _s_OnCalculate_counter_ = counter
            if CCIBuffer[bar] > 0.0:
                CCIColors[bar] = 1.0
                if CCIBuffer[bar] <= CCIBuffer[prevBar]:
                    CCIColors[bar] = 2.0
            else:
                CCIColors[bar] = 3.0
                if CCIBuffer[bar] >= CCIBuffer[prevBar]:
                    CCIColors[bar] = 4.0
            if (CCIBuffer[bar] * CCIBuffer[bar - 1]) < 0:
                counter = 0
            if counter < ExtConfirmationBars:
                counter += 1
                CCIColors[bar] = 0.0
    return rates_total

# ---- static local variables
_s_OnCalculate_counter_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciDrawmode(_MQL5Indicator):
    name = 'cci_drawmode'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpCCIPeriod': 14,  # CCI period
        'InpDrawMode': _Choice({0: 'Line', 1: 'Color fill', 2: 'Histogram'}, default=2),  # Drawing mode
        'InpConfirmationBars': 3,  # Confirmation (number of bars)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

