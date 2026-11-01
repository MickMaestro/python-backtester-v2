"""MA or Price Histogram — converted from MQL5: MQL5 Indicators/MA or Price Histogram/MA or Price Histogram.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.003

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.003', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 11}, 'colors': {1: [755384], 2: [55295], 3: [16711680, 255]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 2}, 'labels': {1: 'MA_Fast_', 2: 'MA_Slow_', 3: 'Trend'}, 'levels': [], 'description': [], 'name': 'MA or Price Histogram', 'source': 'MQL5 Indicators/MA or Price Histogram/MA or Price Histogram.mq5', 'folder': 'MA or Price Histogram', 'inputs': [{'mql': 'InpMAPrice', 'py': 'InpMAPrice', 'param': 'InpMAPrice', 'type': 'int', 'default': 2, 'label': 'Histogram:', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Price:', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_period', 'py': 'Inp_MA_Fast_ma_period', 'param': 'Inp_MA_Fast_ma_period', 'type': 'int', 'default': 12, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_shift', 'py': 'Inp_MA_Fast_ma_shift', 'param': 'Inp_MA_Fast_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_method', 'py': 'Inp_MA_Fast_ma_method', 'param': 'Inp_MA_Fast_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Fast_applied_price', 'py': 'Inp_MA_Fast_applied_price', 'param': 'Inp_MA_Fast_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_period', 'py': 'Inp_MA_Slow_ma_period', 'param': 'Inp_MA_Slow_ma_period', 'type': 'int', 'default': 48, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_shift', 'py': 'Inp_MA_Slow_ma_shift', 'param': 'Inp_MA_Slow_ma_shift', 'type': 'int', 'default': 3, 'label': 'MA: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_method', 'py': 'Inp_MA_Slow_ma_method', 'param': 'Inp_MA_Slow_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Slow_applied_price', 'py': 'Inp_MA_Slow_applied_price', 'param': 'Inp_MA_Slow_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}, {'mql': 'InpUse', 'py': 'InpUse', 'param': 'InpUse', 'type': 'bool', 'default': True, 'label': 'Use Info', 'sinput': False}, {'mql': 'InpX', 'py': 'InpX', 'param': 'InpX', 'type': 'int', 'default': 50, 'label': 'X coordinate', 'sinput': False}, {'mql': 'InpY', 'py': 'InpY', 'param': 'InpY', 'type': 'int', 'default': 50, 'label': 'Y coordinate', 'sinput': False}, {'mql': 'InpYStep', 'py': 'InpYStep', 'param': 'InpYStep', 'type': 'int', 'default': 12, 'label': 'Y step', 'sinput': False}, {'mql': 'InpCorner', 'py': 'InpCorner', 'param': 'InpCorner', 'type': 'int', 'default': 2, 'label': 'Chart corner for anchoring', 'sinput': False}, {'mql': 'InpFont', 'py': 'InpFont', 'param': None, 'type': 'string', 'default': 'Consolas', 'label': 'Font Name', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 10, 'label': 'Font size', 'sinput': False}, {'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color', 'sinput': False}, {'mql': 'InpAngle', 'py': 'InpAngle', 'param': 'InpAngle', 'type': 'double', 'default': 0.0, 'label': 'Text slope', 'sinput': False}, {'mql': 'InpAnchor', 'py': 'InpAnchor', 'param': 'InpAnchor', 'type': 'int', 'default': 4, 'label': 'Anchor type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_PRICE
price_fast = 0
price_slow = 1
fast_slow = 2
_enum('ENUM_MA_PRICE', {0: 'price_fast', 1: 'price_slow', 2: 'fast_slow'})

# ---- inputs and global variables
InpMAPrice = _input('InpMAPrice', fast_slow)  # Histogram:
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Price:
Inp_MA_Fast_ma_period = _input('Inp_MA_Fast_ma_period', 12)  # MA: averaging period
Inp_MA_Fast_ma_shift = _input('Inp_MA_Fast_ma_shift', 0)  # MA: horizontal shift
Inp_MA_Fast_ma_method = _input('Inp_MA_Fast_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_Fast_applied_price = _input('Inp_MA_Fast_applied_price', PRICE_CLOSE)  # MA: type of price
Inp_MA_Slow_ma_period = _input('Inp_MA_Slow_ma_period', 48)  # MA: averaging period
Inp_MA_Slow_ma_shift = _input('Inp_MA_Slow_ma_shift', 3)  # MA: horizontal shift
Inp_MA_Slow_ma_method = _input('Inp_MA_Slow_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_Slow_applied_price = _input('Inp_MA_Slow_applied_price', PRICE_CLOSE)  # MA: type of price
InpUse = _input('InpUse', True)  # Use Info
InpX = _input('InpX', 50)  # X coordinate
InpY = _input('InpY', 50)  # Y coordinate
InpYStep = _input('InpYStep', 12)  # Y step
InpCorner = _input('InpCorner', CORNER_RIGHT_LOWER)  # Chart corner for anchoring
InpFont = _input('InpFont', 'Consolas')  # Font Name
InpFontSize = _input('InpFontSize', 10)  # Font size
InpColor = _input('InpColor', clrRed)  # Color
InpAngle = _input('InpAngle', 0.0)  # Text slope
InpAnchor = _input('InpAnchor', ANCHOR_RIGHT_LOWER)  # Anchor type
MA_Fast_Buffer = Arr(0, 0.0)
MA_Slow_Buffer = Arr(0, 0.0)
TrendBuffer1 = Arr(0, 0.0)
TrendBuffer2 = Arr(0, 0.0)
TrendColors = Arr(0, 0.0)
handle_iMA_Fast = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Slow = 0  # variable for storing the handle of the iMA indicator
m_min_bars = 0
m_prefix = 'MA_or_Price_'
m_color_0 = clrLightGray
m_color_1 = clrLightGray
bars_calculated = 0  # we will keep the number of values in the Moving Average indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA_Fast, handle_iMA_Slow, m_color_0, m_color_1, m_init_error, m_min_bars
    SetIndexBuffer(0, MA_Fast_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MA_Slow_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, TrendBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, TrendBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, TrendColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Inp_MA_Fast_ma_shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Inp_MA_Slow_ma_shift)
    mode_fast = ""
    _sw1 = Inp_MA_Fast_ma_method
    if _sw1 == MODE_EMA:
        mode_fast = 'EMA'
    elif _sw1 == MODE_LWMA:
        mode_fast = 'LWMA'
    elif _sw1 == MODE_SMA:
        mode_fast = 'SMA'
    elif _sw1 == MODE_SMMA:
        mode_fast = 'SMMA'
    else:
        mode_fast = 'unknown mode'
    price_fast_ = StringSubstr(EnumToString(Inp_MA_Fast_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1)
    name_fast = StringFormat('MA Fast(%d,%s,%s,%d)', Inp_MA_Fast_ma_period, mode_fast, price_fast_, Inp_MA_Fast_ma_shift)
    PlotIndexSetString(0, PLOT_LABEL, name_fast)
    mode_slow = ""
    _sw2 = Inp_MA_Slow_ma_method
    if _sw2 == MODE_EMA:
        mode_slow = 'EMA'
    elif _sw2 == MODE_LWMA:
        mode_slow = 'LWMA'
    elif _sw2 == MODE_SMA:
        mode_slow = 'SMA'
    elif _sw2 == MODE_SMMA:
        mode_slow = 'SMMA'
    else:
        mode_slow = 'unknown mode'
    price_slow_ = StringSubstr(EnumToString(Inp_MA_Slow_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1)
    name_slow = StringFormat('MA Slow(%d,%s,%s,%d)', Inp_MA_Slow_ma_period, mode_slow, price_slow_, Inp_MA_Slow_ma_shift)
    PlotIndexSetString(1, PLOT_LABEL, name_slow)
    handle_iMA_Fast = iMA(Symbol(), Period(), Inp_MA_Fast_ma_period, Inp_MA_Fast_ma_shift, Inp_MA_Fast_ma_method, Inp_MA_Fast_applied_price)
    if handle_iMA_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('Fast') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_Slow = iMA(Symbol(), Period(), Inp_MA_Slow_ma_period, Inp_MA_Slow_ma_shift, Inp_MA_Slow_ma_method, Inp_MA_Slow_applied_price)
    if handle_iMA_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('Slow') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    min_bars_fast = Inp_MA_Fast_ma_period + Inp_MA_Fast_ma_shift
    min_bars_slow = Inp_MA_Slow_ma_period + Inp_MA_Slow_ma_shift
    m_min_bars = (min_bars_slow if (min_bars_fast < min_bars_slow) else min_bars_fast)
    m_color_0 = _uint(PlotIndexGetInteger(0, PLOT_LINE_COLOR, 0))
    m_color_1 = _uint(PlotIndexGetInteger(1, PLOT_LINE_COLOR, 0))
    if InpUse:
        width = Box(0)
        height = Box(0)
        step_y = _int((height.v if TextGetSize('80', width, height) else 3))
        LabelCreate(ChartID(), m_prefix + 'Fast', 0, InpX, InpY + 0, InpCorner, 'Fast: - - -', InpFont, InpFontSize, InpColor, InpAngle, InpAnchor)
        LabelCreate(ChartID(), m_prefix + 'Slow', 0, InpX, InpY + step_y, InpCorner, 'Slow: - - -', InpFont, InpFontSize, InpColor, InpAngle, InpAnchor)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    if rates_total < m_min_bars:
        return 0
    values_to_copy = 0
    calculated_fast = BarsCalculated(handle_iMA_Fast)
    if calculated_fast <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, error code %d', calculated_fast, GetLastError())
        return 0
    calculated_slow = BarsCalculated(handle_iMA_Slow)
    if calculated_slow <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Slow) returned %d, error code %d', calculated_slow, GetLastError())
        return 0
    if calculated_fast != calculated_slow:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, BarsCalculated(handle_iMA_Slow) returned %d', calculated_fast, calculated_slow)
        return 0
    calculated = calculated_fast
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(MA_Fast_Buffer, Inp_MA_Fast_ma_shift, handle_iMA_Fast, values_to_copy):
        return 0
    if not FillArrayFromBuffer(MA_Slow_Buffer, Inp_MA_Slow_ma_shift, handle_iMA_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = rates_total - values_to_copy
    if limit < Inp_MA_Fast_ma_shift:
        limit = Inp_MA_Fast_ma_shift
    if limit < Inp_MA_Slow_ma_shift:
        limit = Inp_MA_Slow_ma_shift
    for i in range(limit, rates_total):
        price_1 = MA_Fast_Buffer[i - Inp_MA_Fast_ma_shift]
        price_2 = MA_Slow_Buffer[i - Inp_MA_Slow_ma_shift]
        _sw3 = InpMAPrice
        if _sw3 == price_fast:
            price_2 = MA_Fast_Buffer[i - Inp_MA_Fast_ma_shift]
        elif _sw3 == price_slow:
            price_2 = MA_Slow_Buffer[i - Inp_MA_Slow_ma_shift]
        else:
            price_2 = MA_Slow_Buffer[i - Inp_MA_Slow_ma_shift]
        if InpMAPrice != fast_slow:
            _sw4 = InpPrice
            if _sw4 == PRICE_CLOSE:
                price_1 = close[i]
            elif _sw4 == PRICE_OPEN:
                price_1 = open[i]
            elif _sw4 == PRICE_HIGH:
                price_1 = high[i]
            elif _sw4 == PRICE_LOW:
                price_1 = low[i]
            elif _sw4 == PRICE_MEDIAN:
                price_1 = (high[i] + low[i]) / 2.0
            elif _sw4 == PRICE_TYPICAL:
                price_1 = (high[i] + low[i] + close[i]) / 3.0
            elif _sw4 == PRICE_WEIGHTED:
                price_1 = (high[i] + low[i] + close[i] + close[i]) / 4.0
        TrendBuffer1[i] = price_1
        TrendBuffer2[i] = price_2
        if MA_Fast_Buffer[i] > MA_Slow_Buffer[i]:
            TrendColors[i] = 0.0
        else:
            TrendColors[i] = 1.0
    if InpUse:
        chart_id = ChartID()
        LabelTextChange(chart_id, m_prefix + 'Fast', 'Fast: ' + DoubleToString(TrendBuffer1[rates_total - 1], Digits() + 1), m_color_0)
        LabelTextChange(chart_id, m_prefix + 'Slow', 'Slow: ' + DoubleToString(TrendBuffer2[rates_total - 1], Digits() + 1), m_color_1)
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def LabelCreate(chart_ID=0, name='Label', sub_window=0, x=0, y=0, corner=CORNER_LEFT_UPPER, text='Label', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_CENTER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_LABEL, sub_window, 0, 0):
        Print('LabelCreate', ': failed to create text label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def LabelTextChange(chart_ID=0, name='Label', text='text', clr=clrRed):
    ResetLastError()
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    return True

def OnDeinit(reason):
    if handle_iMA_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Fast)
    if handle_iMA_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Slow)
    ObjectsDeleteAll(ChartID(), m_prefix, 0, OBJ_LABEL)
    ChartRedraw(ChartID())


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAOrPriceHistogram(_MQL5Indicator):
    name = 'MA or Price Histogram'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPrice': _Choice({0: 'Price <-> Fast', 1: 'Price <-> Slow', 2: 'Fast <-> Slow'}, default=2),  # Histogram:
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price:
        'Inp_MA_Fast_ma_period': 12,  # MA: averaging period
        'Inp_MA_Fast_ma_shift': 0,  # MA: horizontal shift
        'Inp_MA_Fast_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_Fast_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
        'Inp_MA_Slow_ma_period': 48,  # MA: averaging period
        'Inp_MA_Slow_ma_shift': 3,  # MA: horizontal shift
        'Inp_MA_Slow_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_Slow_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
        'InpUse': True,  # Use Info
        'InpX': 50,  # X coordinate
        'InpY': 50,  # Y coordinate
        'InpYStep': 12,  # Y step
        'InpCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=2),  # Chart corner for anchoring
        'InpFontSize': 10,  # Font size
        'InpAngle': 0.0,  # Text slope
        'InpAnchor': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=4),  # Anchor type
    }

