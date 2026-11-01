"""easytrendvisualizer — converted from MQL5: MQL5 Indicators/Easy Trend Visualizer/easytrendvisualizer.mq5

Easy Trend Visualizer - displays trend strength, direction and
support and resistance levels.
Alerts (set UseAlert = true):
 * ERV-HL - Horizontal line
 * ERV-AU - Arrow up
 * ERV-AD - Arrow down
Copyright: Copyright © 2009-2011, EarnForex; Link: http://www.earnforex.com; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009-2011, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.20', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 11, 2: 5, 3: 5, 4: 1}, 'colors': {1: [255, 65280], 2: [7451452], 3: [255], 4: [8519755]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {}, 'levels': [], 'description': ['Easy Trend Visualizer - displays trend strength, direction and', 'support and resistance levels.', 'Alerts (set UseAlert = true):', ' * ERV-HL - Horizontal line', ' * ERV-AU - Arrow up', ' * ERV-AD - Arrow down'], 'name': 'easytrendvisualizer', 'source': 'MQL5 Indicators/Easy Trend Visualizer/easytrendvisualizer.mq5', 'folder': 'Easy Trend Visualizer', 'inputs': [{'mql': 'ADXperiod1', 'py': 'ADXperiod1', 'param': 'ADXperiod1', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ADXperiod2', 'py': 'ADXperiod2', 'param': 'ADXperiod2', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ADXperiod3', 'py': 'ADXperiod3', 'param': 'ADXperiod3', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXperiod1 = _input('ADXperiod1', 10)
ADXperiod2 = _input('ADXperiod2', 14)
ADXperiod3 = _input('ADXperiod3', 20)
MxP = 0
MnP = 0
MdP = 0
To = Arr(0, 0.0)
Tc = Arr(0, 0.0)
Color = Arr(0, 0.0)
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Ex = Arr(0, 0.0)
min_rates_total = 0
ADX1_Handle = 0
ADX2_Handle = 0
ADX3_Handle = 0

def OnInit():
    global ADX1_Handle, ADX2_Handle, ADX3_Handle, MdP, MnP, MxP, min_rates_total
    MxP = MathMax(MathMax(ADXperiod1, ADXperiod2), ADXperiod3)
    MnP = MathMin(MathMin(ADXperiod1, ADXperiod2), ADXperiod3)
    if MxP == ADXperiod1:
        MdP = MathMax(ADXperiod2, ADXperiod3)
    elif MxP == ADXperiod2:
        MdP = MathMax(ADXperiod1, ADXperiod3)
    else:
        MdP = MathMax(ADXperiod2, ADXperiod1)
    min_rates_total = MxP + 1
    ADX1_Handle = iADX(Symbol(), PERIOD_CURRENT, MnP)
    if ADX1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX 1 indicator')
        return
    ADX2_Handle = iADX(Symbol(), PERIOD_CURRENT, MdP)
    if ADX2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX 2 indicator')
        return
    ADX3_Handle = iADX(Symbol(), PERIOD_CURRENT, MxP)
    if ADX3_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX 3 indicator')
        return
    IndicatorSetString(INDICATOR_SHORTNAME, 'ETV(' + IntegerToString(MnP) + '/' + IntegerToString(MdP) + '/' + IntegerToString(MxP) + ')')
    SetIndexBuffer(0, To, INDICATOR_DATA)
    SetIndexBuffer(1, Tc, INDICATOR_DATA)
    SetIndexBuffer(2, Color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, Up, INDICATOR_DATA)
    SetIndexBuffer(4, Dn, INDICATOR_DATA)
    SetIndexBuffer(5, Ex, INDICATOR_DATA)
    ArraySetAsSeries(To, True)
    ArraySetAsSeries(Tc, True)
    ArraySetAsSeries(Color, True)
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Dn, True)
    ArraySetAsSeries(Ex, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 225)
    PlotIndexSetInteger(2, PLOT_ARROW, 226)
    PlotIndexSetString(1, PLOT_LABEL, 'Up')
    PlotIndexSetString(2, PLOT_LABEL, 'Down')
    PlotIndexSetString(3, PLOT_LABEL, 'End')

def OnCalculate(rates_total, prev_calculated, time, Open, High, Low, Close, tick_volume, volume, spread):
    if ((BarsCalculated(ADX1_Handle) < rates_total or BarsCalculated(ADX2_Handle) < rates_total) or BarsCalculated(ADX3_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    ADXArray1 = Arr(0, 0.0)
    ADXArray2 = Arr(0, 0.0)
    ADXArray3 = Arr(0, 0.0)
    ADXArray1_1 = Arr(0, 0.0)
    ADXArray1_2 = Arr(0, 0.0)
    limit = 0
    bar = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX1_Handle, MAIN_LINE, 0, to_copy, ADXArray1) <= 0:
        return 0
    if CopyBuffer(ADX1_Handle, PLUSDI_LINE, 0, to_copy, ADXArray1_1) <= 0:
        return 0
    if CopyBuffer(ADX1_Handle, MINUSDI_LINE, 0, to_copy, ADXArray1_2) <= 0:
        return 0
    if CopyBuffer(ADX2_Handle, MAIN_LINE, 0, to_copy, ADXArray2) <= 0:
        return 0
    if CopyBuffer(ADX3_Handle, MAIN_LINE, 0, to_copy, ADXArray3) <= 0:
        return 0
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(ADXArray1, True)
    ArraySetAsSeries(ADXArray2, True)
    ArraySetAsSeries(ADXArray3, True)
    ArraySetAsSeries(ADXArray1_1, True)
    ArraySetAsSeries(ADXArray1_2, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        f1 = False
        f2 = False
        f3 = False
        To[bar] = 0.0
        Tc[bar] = 0.0
        Up[bar] = 0.0
        Dn[bar] = 0.0
        Ex[bar] = 0.0
        bar1 = bar + 1
        if ADXArray1[bar1] < ADXArray1[bar]:
            f1 = True
        if ADXArray2[bar1] < ADXArray2[bar]:
            f2 = True
        if ADXArray3[bar1] < ADXArray3[bar]:
            f3 = True
        if (((f1 and f2) and f3) and ADXArray1[bar] > 35.0) and ADXArray2[bar] > 30.0:
            di = ADXArray1_1[bar] - ADXArray1_2[bar]
            hi = MathMax(Open[bar], Close[bar])
            lo = MathMin(Open[bar], Close[bar])
            op = Open[bar]
            if di > 0:
                To[bar] = lo
                Tc[bar] = hi
                if not To[bar1]:
                    Up[bar] = op
                Color[bar] = 1.0
            else:
                To[bar] = hi
                Tc[bar] = lo
                if not To[bar1]:
                    Dn[bar] = op
                Color[bar] = 0.0
        else:
            if To[bar1]:
                Ex[bar] = Close[bar + 1]
            else:
                Ex[bar] = Ex[bar1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Easytrendvisualizer(_MQL5Indicator):
    name = 'easytrendvisualizer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXperiod1': 10,
        'ADXperiod2': 14,
        'ADXperiod3': 20,
    }

