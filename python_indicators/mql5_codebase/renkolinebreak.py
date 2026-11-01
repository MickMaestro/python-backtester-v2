"""renkolinebreak — converted from MQL5: MQL5 Indicators/Renko Line Break/renkolinebreak.mq5

It is a hybrid of Renko and Three Line Break indicators. Built on the 
close prices of current Time Frame, the box size must be equal or larger than the specified.
Copyright: Copyright 2013, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 0}, 'colors': {1: [14772545], 2: [3937500], 3: [4294967295]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper', 2: 'Lower', 3: 'Boxes'}, 'levels': [], 'description': ['It is a hybrid of Renko and Three Line Break indicators. Built on the ', 'close prices of current Time Frame, the box size must be equal or larger than the specified.'], 'name': 'renkolinebreak', 'source': 'MQL5 Indicators/Renko Line Break/renkolinebreak.mq5', 'folder': 'Renko Line Break', 'inputs': [{'mql': 'InpMinBoxSize', 'py': 'InpMinBoxSize', 'param': 'InpMinBoxSize', 'type': 'int', 'default': 300, 'label': 'Min Box Size', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMinBoxSize = _input('InpMinBoxSize', 300)  # Min Box Size
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
BoxesBuffer = Arr(0, 0.0)
box_size = 0.0

def OnInit():
    global box_size
    if InpMinBoxSize < 0:
        box_size = 300.0
        printf('Incorrected input value InpMinBoxSize = %d. Indicator will use value %d', InpMinBoxSize, _int(box_size))
    else:
        box_size = InpMinBoxSize
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BoxesBuffer, INDICATOR_DATA)
    for plot in range(0, 3):
        PlotIndexSetInteger(plot, PLOT_DRAW_BEGIN, 1)
        PlotIndexSetInteger(plot, PLOT_SHIFT, 0)
        PlotIndexSetDouble(plot, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Renko Line Break (' + DoubleToString(box_size, 0) + ')')
    box_size *= Point()
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate__up
    start_bar = 0
    up = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        start_bar = 0
        while MathAbs(price[0] - price[start_bar]) < box_size:
            pass
            start_bar += 1
        if price[start_bar] > price[0]:
            UpperBuffer[start_bar] = price[start_bar]
            LowerBuffer[start_bar] = price[0]
            BoxesBuffer[start_bar] = 1.0
            _s_OnCalculate__up = True
        else:
            UpperBuffer[start_bar] = price[0]
            LowerBuffer[start_bar] = price[start_bar]
            BoxesBuffer[start_bar] = -1.0
            _s_OnCalculate__up = False
        start_bar += 1
        for plot in range(0, 3):
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start_bar)
    else:
        start_bar = prev_calculated - 1
    up = _s_OnCalculate__up
    for bar in range(start_bar, rates_total):
        prev_up = UpperBuffer[bar - 1]
        prev_dn = LowerBuffer[bar - 1]
        prev_boxes = BoxesBuffer[bar - 1]
        if price[bar] >= (prev_up + box_size):
            UpperBuffer[bar] = price[bar]
            LowerBuffer[bar] = prev_up
            if up:
                BoxesBuffer[bar] = prev_boxes + 1
            else:
                up = True
                BoxesBuffer[bar] = 1.0
        elif price[bar] <= (prev_dn - box_size):
            UpperBuffer[bar] = prev_dn
            LowerBuffer[bar] = price[bar]
            if up:
                up = False
                BoxesBuffer[bar] = -1.0
            else:
                BoxesBuffer[bar] = prev_boxes - 1
        else:
            UpperBuffer[bar] = prev_up
            LowerBuffer[bar] = prev_dn
            BoxesBuffer[bar] = prev_boxes
        if bar < (rates_total - 1):
            _s_OnCalculate__up = up
    return rates_total

# ---- static local variables
_s_OnCalculate__up = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Renkolinebreak(_MQL5Indicator):
    name = 'renkolinebreak'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMinBoxSize': 300,  # Min Box Size
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

