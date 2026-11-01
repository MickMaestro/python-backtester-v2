"""linearregression — converted from MQL5: MQL5 Indicators/LinearRegression/linearregression.mq5

Linear Regression
Copyright: Copyright © 2006, tageiger, aka fxid10t@yahoo.com; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, tageiger, aka fxid10t@yahoo.com', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Linear Regression'], 'name': 'linearregression', 'source': 'MQL5 Indicators/LinearRegression/linearregression.mq5', 'folder': 'LinearRegression', 'inputs': [{'mql': 'lines_sirname', 'py': 'lines_sirname', 'param': None, 'type': 'string', 'default': 'Linear_Regression_', 'label': 'Graphic objects group name', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'Chart period', 'sinput': False}, {'mql': 'LR_length', 'py': 'LR_length', 'param': 'LR_length', 'type': 'int', 'default': 34, 'label': 'Indicator calculation period', 'sinput': False}, {'mql': 'Deletelevel', 'py': 'Deletelevel', 'param': 'Deletelevel', 'type': 'bool', 'default': True, 'label': 'Level deletion', 'sinput': False}, {'mql': 'LR_c', 'py': 'LR_c', 'param': None, 'type': 'color', 'default': 0, 'label': 'Middle line color', 'sinput': False}, {'mql': 'LR_style', 'py': 'LR_style', 'param': 'LR_style', 'type': 'int', 'default': 0, 'label': 'Middle line style', 'sinput': False}, {'mql': 'LR_width', 'py': 'LR_width', 'param': 'LR_width', 'type': 'int', 'default': 3, 'label': 'Middle line width', 'sinput': False}, {'mql': 'std_channel_1', 'py': 'std_channel_1', 'param': 'std_channel_1', 'type': 'double', 'default': 0.618, 'label': 'Minimum regression', 'sinput': False}, {'mql': 'c_1', 'py': 'c_1', 'param': None, 'type': 'color', 'default': 0, 'label': 'Minimum line color', 'sinput': False}, {'mql': 'style_1', 'py': 'style_1', 'param': 'style_1', 'type': 'int', 'default': 1, 'label': 'Minimum line style', 'sinput': False}, {'mql': 'width_1', 'py': 'width_1', 'param': 'width_1', 'type': 'int', 'default': 1, 'label': 'Minimum line width', 'sinput': False}, {'mql': 'std_channel_2', 'py': 'std_channel_2', 'param': 'std_channel_2', 'type': 'double', 'default': 1.618, 'label': 'Nominal regression', 'sinput': False}, {'mql': 'c_2', 'py': 'c_2', 'param': None, 'type': 'color', 'default': 0, 'label': 'Nominal line color', 'sinput': False}, {'mql': 'style_2', 'py': 'style_2', 'param': 'style_2', 'type': 'int', 'default': 2, 'label': 'Nominal line style', 'sinput': False}, {'mql': 'width_2', 'py': 'width_2', 'param': 'width_2', 'type': 'int', 'default': 1, 'label': 'Nominal line width', 'sinput': False}, {'mql': 'std_channel_3', 'py': 'std_channel_3', 'param': 'std_channel_3', 'type': 'double', 'default': 2.618, 'label': 'Maximum regression', 'sinput': False}, {'mql': 'c_3', 'py': 'c_3', 'param': None, 'type': 'color', 'default': 0, 'label': 'Maximum line color', 'sinput': False}, {'mql': 'style_3', 'py': 'style_3', 'param': 'style_3', 'type': 'int', 'default': 0, 'label': 'Maximum line style', 'sinput': False}, {'mql': 'width_3', 'py': 'width_3', 'param': 'width_3', 'type': 'int', 'default': 3, 'label': 'Maximum line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Gold = 0x00D7FF  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
lines_sirname = _input('lines_sirname', 'Linear_Regression_')  # Graphic objects group name
period = _input('period', PERIOD_CURRENT)  # Chart period
LR_length = _input('LR_length', 34)  # Indicator calculation period
Deletelevel = _input('Deletelevel', True)  # Level deletion
LR_style = _input('LR_style', STYLE_SOLID)  # Middle line style
LR_width = _input('LR_width', w_3)  # Middle line width
std_channel_1 = _input('std_channel_1', 0.618)  # Minimum regression
style_1 = _input('style_1', STYLE_DASH)  # Minimum line style
width_1 = _input('width_1', w_1)  # Minimum line width
std_channel_2 = _input('std_channel_2', 1.618)  # Nominal regression
style_2 = _input('style_2', STYLE_DOT)  # Nominal line style
width_2 = _input('width_2', w_1)  # Nominal line width
std_channel_3 = _input('std_channel_3', 2.618)  # Maximum regression
style_3 = _input('style_3', STYLE_SOLID)  # Maximum line style
width_3 = _input('width_3', w_3)  # Maximum line width
start_bar = 0
end_bar = 0
n = 0
to_copy = 0
LR_name = ""
CH1P_name = ""
CH1M_name = ""
CH2P_name = ""
CH2M_name = ""
CH3P_name = ""
CH3M_name = ""

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global CH1M_name, CH1P_name, CH2M_name, CH2P_name, CH3M_name, CH3P_name, LR_name, end_bar, n, start_bar, to_copy
    fullname = lines_sirname + _str(period) + ' ' + _str(LR_length)
    LR_name = fullname + ' TL'
    CH1P_name = fullname + ' +' + _str(std_channel_1) + 'd'
    CH1M_name = fullname + ' -' + _str(std_channel_1) + 'd'
    CH2P_name = fullname + ' +' + _str(std_channel_2) + 'd'
    CH2M_name = fullname + ' -' + _str(std_channel_2) + 'd'
    CH3P_name = fullname + ' +' + _str(std_channel_3) + 'd'
    CH3M_name = fullname + ' -' + _str(std_channel_3) + 'd'
    start_bar = LR_length
    end_bar = 0
    n = start_bar - end_bar + 1
    to_copy = 2 * n

def OnDeinit(reason):
    if Deletelevel:
        ObjectDelete(0, LR_name)
        ObjectDelete(0, CH1P_name)
        ObjectDelete(0, CH1M_name)
        ObjectDelete(0, CH2P_name)
        ObjectDelete(0, CH2M_name)
        ObjectDelete(0, CH3P_name)
        ObjectDelete(0, CH3M_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    value = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    iClose_ = Arr(0, 0.0)
    iTime_ = Arr(0, 0)
    start_time = 0
    end_time = 0
    if CopyClose(None, period, 0, to_copy, iClose_) <= 0:
        return 0
    if CopyTime(None, period, 0, to_copy, iTime_) <= 0:
        return 0
    ArraySetAsSeries(iClose_, True)
    ArraySetAsSeries(iTime_, True)
    start_time = iTime_[start_bar]
    end_time = iTime_[end_bar]
    value = iClose_[end_bar]
    sumy = value
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    for iii in range(1, n):
        value = iClose_[end_bar + iii]
        sumy += value
        sumxy += value * iii
        sumx += iii
        sumx2 += iii * iii
    c = (sumx2 * n) - (sumx * sumx)
    if not c:
        return rates_total
    b = _fdiv((sumxy * n) - (sumx * sumy), c)
    a = _fdiv(sumy - (sumx * b), n)
    LR_price_2 = a
    LR_price_1 = a + (b * n)
    max_dev = 0.0
    deviation = 0.0
    dvalue = a
    for iii in range(0, n):
        value = iClose_[end_bar + iii]
        dvalue += b
        deviation = MathAbs(value - dvalue)
        if max_dev <= deviation:
            max_dev = deviation
    SetTline(0, LR_name, 0, start_time, LR_price_1, end_time, LR_price_2, LR_c, LR_style, LR_width, LR_name)
    x = 0.0
    x_sum = 0.0
    x_avg = 0.0
    x_sum_squared = 0.0
    std_dev = 0.0
    price1 = 0.0
    price2 = 0.0
    for iii in range(0, start_bar):
        x = MathAbs(iClose_[iii] - ObjectGetValueByTime(0, LR_name, iTime_[iii], 0))
        x_sum += x
        if iii > 0:
            x_avg = _fdiv(x_avg + x, iii)
            x_sum_squared += (x - x_avg) * (x - x_avg)
            std_dev = MathSqrt(_fdiv(x_sum_squared, start_bar - 1))
    price1 = LR_price_1 + (std_dev * std_channel_1)
    price2 = LR_price_2 + (std_dev * std_channel_1)
    SetTline(0, CH1P_name, 0, start_time, price1, end_time, price2, c_1, style_1, width_1, CH1P_name)
    price1 = LR_price_1 - (std_dev * std_channel_1)
    price2 = LR_price_2 - (std_dev * std_channel_1)
    SetTline(0, CH1M_name, 0, start_time, price1, end_time, price2, c_1, style_1, width_1, CH1M_name)
    price1 = LR_price_1 + (std_dev * std_channel_2)
    price2 = LR_price_2 + (std_dev * std_channel_2)
    SetTline(0, CH2P_name, 0, start_time, price1, end_time, price2, c_2, style_2, width_2, CH2P_name)
    price1 = LR_price_1 - (std_dev * std_channel_2)
    price2 = LR_price_2 - (std_dev * std_channel_2)
    SetTline(0, CH2M_name, 0, start_time, price1, end_time, price2, c_2, style_2, width_2, CH2M_name)
    price1 = LR_price_1 + (std_dev * std_channel_3)
    price2 = LR_price_2 + (std_dev * std_channel_3)
    SetTline(0, CH3P_name, 0, start_time, price1, end_time, price2, c_3, style_3, width_3, CH3P_name)
    price1 = LR_price_1 - (std_dev * std_channel_3)
    price2 = LR_price_2 - (std_dev * std_channel_3)
    SetTline(0, CH3M_name, 0, start_time, price1, end_time, price2, c_3, style_3, width_3, CH3M_name)
    return rates_total

# ---- global variables initialised from expressions
LR_c = _input('LR_c', _uint(Blue))  # Middle line color
c_1 = _input('c_1', _uint(Gold))  # Minimum line color
c_2 = _input('c_2', _uint(Lime))  # Nominal line color
c_3 = _input('c_3', _uint(Magenta))  # Maximum line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Linearregression(_MQL5Indicator):
    name = 'linearregression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Chart period
        'LR_length': 34,  # Indicator calculation period
        'Deletelevel': True,  # Level deletion
        'LR_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Middle line style
        'LR_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Middle line width
        'std_channel_1': 0.618,  # Minimum regression
        'style_1': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Minimum line style
        'width_1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Minimum line width
        'std_channel_2': 1.618,  # Nominal regression
        'style_2': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Nominal line style
        'width_2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Nominal line width
        'std_channel_3': 2.618,  # Maximum regression
        'style_3': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Maximum line style
        'width_3': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Maximum line width
    }

