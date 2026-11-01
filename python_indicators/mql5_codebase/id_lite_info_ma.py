"""id_lite_info_ma — converted from MQL5: MQL5 Indicators/ID Lite Info MA/id_lite_info_ma.mq5

Copyright: 2017, Dina Paches; Link: https://login.mql5.com/ru/users/dipach; Version: 1.45

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2017, Dina Paches', 'link': 'https://login.mql5.com/ru/users/dipach', 'version': '1.45', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [15570276], 2: [15570276]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'id_lite_info_ma', 'source': 'MQL5 Indicators/ID Lite Info MA/id_lite_info_ma.mq5', 'folder': 'ID Lite Info MA', 'inputs': [{'mql': 'i_show_lines', 'py': 'i_show_lines', 'param': 'i_show_lines', 'type': 'bool', 'default': False, 'label': 'Show lines MA', 'sinput': False}, {'mql': 'i_ma_0_indent', 'py': 'i_ma_0_indent', 'param': 'i_ma_0_indent', 'type': 'int', 'default': 0, 'label': 'Shift in points from MA1 (-/+ Down or Up)', 'sinput': False}, {'mql': 'i_ma_1_indent', 'py': 'i_ma_1_indent', 'param': 'i_ma_1_indent', 'type': 'int', 'default': 0, 'label': 'Shift in points from MA2 (-/+ Down or Up)', 'sinput': False}, {'mql': 'i_digits', 'py': 'i_digits', 'param': 'i_digits', 'type': 'int', 'default': -1, 'label': 'Decimal digits', 'sinput': False}, {'mql': 'i_shift', 'py': 'i_shift', 'param': 'i_shift', 'type': 'uint', 'default': 1, 'label': 'Shift (bar for first value):', 'sinput': False}, {'mql': 'i_stripe_0', 'py': 'i_stripe_0', 'param': None, 'type': 'string', 'default': '+++++++++++++++++++++', 'label': '+++++++++++++++++++++', 'sinput': True}, {'mql': 'i_ma_0_period', 'py': 'i_ma_0_period', 'param': 'i_ma_0_period', 'type': 'uint', 'default': 1, 'label': 'Period Moving Averages (1)>= 1 or <= 3000:', 'sinput': False}, {'mql': 'i_ma_0_method', 'py': 'i_ma_0_method', 'param': 'i_ma_0_method', 'type': 'int', 'default': 0, 'label': 'MA method (1):', 'sinput': False}, {'mql': 'i_ma_0_applied_price', 'py': 'i_ma_0_applied_price', 'param': 'i_ma_0_applied_price', 'type': 'int', 'default': 3, 'label': 'Apply to (1):', 'sinput': False}, {'mql': 'i_stripe_1', 'py': 'i_stripe_1', 'param': None, 'type': 'string', 'default': '+++++++++++++++++++++', 'label': '+++++++++++++++++++++', 'sinput': True}, {'mql': 'i_ma_1_period', 'py': 'i_ma_1_period', 'param': 'i_ma_1_period', 'type': 'uint', 'default': 1, 'label': 'Period Moving Averages (2)>= 1 or <= 3000:', 'sinput': False}, {'mql': 'i_ma_1_method', 'py': 'i_ma_1_method', 'param': 'i_ma_1_method', 'type': 'int', 'default': 0, 'label': 'MA method (2):', 'sinput': False}, {'mql': 'i_ma_1_applied_price', 'py': 'i_ma_1_applied_price', 'param': 'i_ma_1_applied_price', 'type': 'int', 'default': 4, 'label': 'Apply to (2):', 'sinput': False}, {'mql': 'i_stripe_2', 'py': 'i_stripe_2', 'param': None, 'type': 'string', 'default': '+++++++++++++++++++++', 'label': '+++++++++++++++++++++', 'sinput': True}, {'mql': 'i_distance_x', 'py': 'i_distance_x', 'param': 'i_distance_x', 'type': 'uint', 'default': 3, 'label': 'X coordinate', 'sinput': False}, {'mql': 'i_distance_y', 'py': 'i_distance_y', 'param': 'i_distance_y', 'type': 'uint', 'default': 3, 'label': 'Y coordinate', 'sinput': False}, {'mql': 'i_clr_back_main', 'py': 'i_clr_back_main', 'param': None, 'type': 'color', 'default': 14737632, 'label': 'Background color (table and Equal)', 'sinput': False}, {'mql': 'i_clr_back_up', 'py': 'i_clr_back_up', 'param': None, 'type': 'color', 'default': 15570276, 'label': 'Background color (Up)', 'sinput': False}, {'mql': 'i_clr_back_down', 'py': 'i_clr_back_down', 'param': None, 'type': 'color', 'default': 5592575, 'label': 'Background color (Down)', 'sinput': False}, {'mql': 'i_clr_text_ma', 'py': 'i_clr_text_ma', 'param': None, 'type': 'color', 'default': 3158064, 'label': 'Text color for MA', 'sinput': False}, {'mql': 'i_clr_text_delta', 'py': 'i_clr_text_delta', 'param': None, 'type': 'color', 'default': 6908265, 'label': 'Color text for delta', 'sinput': False}, {'mql': 'i_obj_width', 'py': 'i_obj_width', 'param': 'i_obj_width', 'type': 'uint', 'default': 60, 'label': 'Width', 'sinput': False}, {'mql': 'i_obj_height', 'py': 'i_obj_height', 'param': 'i_obj_height', 'type': 'uint', 'default': 18, 'label': 'Height', 'sinput': False}, {'mql': 'i_font_size', 'py': 'i_font_size', 'param': 'i_font_size', 'type': 'uint', 'default': 9, 'label': 'Font size', 'sinput': False}, {'mql': 'i_behind', 'py': 'i_behind', 'param': 'i_behind', 'type': 'bool', 'default': True, 'label': 'Table of the indicator behind bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter

# enum enum_Digits
auto = -1
dig0 = 0
dig1 = 1
dig2 = 2
dig3 = 3
dig4 = 4
dig5 = 5
dig6 = 6
dig7 = 7
dig8 = 8
_enum('enum_Digits', {-1: 'auto', 0: 'dig0', 1: 'dig1', 2: 'dig2', 3: 'dig3', 4: 'dig4', 5: 'dig5', 6: 'dig6', 7: 'dig7', 8: 'dig8'})

# enum enum_DisplayTable
NO_ = 0
IS_ = 1
MINIMIZED = 2
_enum('enum_DisplayTable', {0: 'NO_', 1: 'IS_', 2: 'MINIMIZED'})

# enum enum_UsePrice
HANDLE = 0
HIGH = 1
LOW = 2
OPEN = 3
CLOSE = 4
_enum('enum_UsePrice', {0: 'HANDLE', 1: 'HIGH', 2: 'LOW', 3: 'OPEN', 4: 'CLOSE'})

# ---- inputs and global variables
i_show_lines = _input('i_show_lines', False)  # Show lines MA
i_ma_0_indent = _input('i_ma_0_indent', 0)  # Shift in points from MA1 (-/+ Down or Up)
i_ma_1_indent = _input('i_ma_1_indent', 0)  # Shift in points from MA2 (-/+ Down or Up)
i_digits = _input('i_digits', auto)  # Decimal digits
i_shift = _input('i_shift', 1)  # Shift (bar for first value):
i_stripe_0 = _input('i_stripe_0', '+++++++++++++++++++++')  # +++++++++++++++++++++
i_ma_0_period = _input('i_ma_0_period', 1)  # Period Moving Averages (1)>= 1 or <= 3000:
i_ma_0_method = _input('i_ma_0_method', MODE_SMA)  # MA method (1):
i_ma_0_applied_price = _input('i_ma_0_applied_price', PRICE_HIGH)  # Apply to (1):
i_stripe_1 = _input('i_stripe_1', '+++++++++++++++++++++')  # +++++++++++++++++++++
i_ma_1_period = _input('i_ma_1_period', 1)  # Period Moving Averages (2)>= 1 or <= 3000:
i_ma_1_method = _input('i_ma_1_method', MODE_SMA)  # MA method (2):
i_ma_1_applied_price = _input('i_ma_1_applied_price', PRICE_LOW)  # Apply to (2):
i_stripe_2 = _input('i_stripe_2', '+++++++++++++++++++++')  # +++++++++++++++++++++
i_distance_x = _input('i_distance_x', 3)  # X coordinate
i_distance_y = _input('i_distance_y', 3)  # Y coordinate
i_clr_back_main = _input('i_clr_back_main', 0xE0E0E0)  # Background color (table and Equal)
i_clr_back_up = _input('i_clr_back_up', clrCornflowerBlue)  # Background color (Up)
i_clr_back_down = _input('i_clr_back_down', 0x5555FF)  # Background color (Down)
i_clr_text_ma = _input('i_clr_text_ma', 0x303030)  # Text color for MA
i_clr_text_delta = _input('i_clr_text_delta', clrDimGray)  # Color text for delta
i_obj_width = _input('i_obj_width', 60)  # Width
i_obj_height = _input('i_obj_height', 18)  # Height
i_font_size = _input('i_font_size', 9)  # Font size
i_behind = _input('i_behind', True)  # Table of the indicator behind bars
ma_0_buff = Arr(0, 0.0)
ma_1_buff = Arr(0, 0.0)
gp_symbol = ""
gp_ind_shortname = ""
gp_name_butt = ""
ga_name = Arr(5, "", dyn=False, dims=(9,))
ga_text_odd_row = Arr(3, "", dyn=False, dims=(9,))
ga_text_even_row = Arr(2, "", dyn=False, dims=(9,))
ga_clr_back_odd_row = Arr(3, 0, dyn=False, dims=(9,))
ga_clr_text_even_row = Arr(2, 0, dyn=False, dims=(9,))
gp_first_bar = 0
gp_min_rates_total = 0
ga_ma_handle = Arr(2, 0, dyn=False)
gp_first = False
gp_tf = 0
gp_display_table = NO_
ga_use_price = Arr.of([HANDLE, HANDLE], fill=0, dyn=False, size=2)

def OnInit():
    if not InitAny():
        return REASON_CHARTCHANGE
    BuffersInit()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if reason != REASON_CHARTCHANGE:
        ObjectsDeleteAll(0, gp_ind_shortname)
    for i in range(2 - 1, 0 - 1, -1):
        if ga_use_price[i] == HANDLE:
            IndicatorRelease(ga_ma_handle[i])
    if reason == REASON_INITFAILED:
        ChIndicatorDelete(gp_ind_shortname)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_digits, _s_OnCalculate_limit, _s_OnCalculate_ma_0_indent, _s_OnCalculate_ma_1_indent, _s_OnCalculate_point_pow, _s_OnCalculate_time_new_bar, gp_display_table, gp_first
    if gp_first:
        if (rates_total - 1) < gp_min_rates_total or prev_calculated < 0:
            return rates_total
    if _s_OnCalculate_digits is _UNSET:
        _s_OnCalculate_digits = DigitsSet(i_digits)
    if _s_OnCalculate_point_pow is _UNSET:
        _s_OnCalculate_point_pow = _int(MathPow(10, _s_OnCalculate_digits))
    if _s_OnCalculate_ma_0_indent is _UNSET:
        _s_OnCalculate_ma_0_indent = IndentDoubleSet(i_ma_0_indent, _s_OnCalculate_point_pow, _s_OnCalculate_digits)
    if _s_OnCalculate_ma_1_indent is _UNSET:
        _s_OnCalculate_ma_1_indent = IndentDoubleSet(i_ma_1_indent, _s_OnCalculate_point_pow, _s_OnCalculate_digits)
    ArraySetAsSeries(time, True)
    if prev_calculated == 0:
        if not StopDataClear():
            _s_OnCalculate_time_new_bar = 0
            ArrayInitialize(ma_0_buff, 0.0)
            ArrayInitialize(ma_1_buff, 0.0)
        _s_OnCalculate_limit = 9 + gp_first_bar + 1
    else:
        _s_OnCalculate_limit = rates_total - prev_calculated + 1
    if _s_OnCalculate_time_new_bar != time[0]:
        _s_OnCalculate_time_new_bar = time[0]
        if ga_use_price[0] != HANDLE:
            if not CopyPrice(gp_symbol, gp_tf, gp_first_bar, _s_OnCalculate_limit, ma_0_buff, _s_OnCalculate_ma_0_indent, _s_OnCalculate_digits, ga_use_price[0]):
                return 0
        else:
            if not CopyIMA(ga_ma_handle[0], 0, gp_first_bar, _s_OnCalculate_limit, _s_OnCalculate_ma_0_indent, _s_OnCalculate_digits, ma_0_buff):
                return 0
        if ga_use_price[1] != HANDLE:
            if not CopyPrice(gp_symbol, gp_tf, gp_first_bar, _s_OnCalculate_limit, ma_1_buff, _s_OnCalculate_ma_1_indent, _s_OnCalculate_digits, ga_use_price[1]):
                return 0
        else:
            if not CopyIMA(ga_ma_handle[1], 0, gp_first_bar, _s_OnCalculate_limit, _s_OnCalculate_ma_1_indent, _s_OnCalculate_digits, ma_1_buff):
                return 0
        count = MathMin(_s_OnCalculate_limit, 9)
        if count > 0:
            TableValuesSet(0, ma_0_buff, _s_OnCalculate_point_pow, 0, count, _s_OnCalculate_digits, _s_OnCalculate_ma_0_change_clr_arr, gp_first)
            TableValuesSet(2, ma_1_buff, _s_OnCalculate_point_pow, 1, count, _s_OnCalculate_digits, _s_OnCalculate_ma_1_change_clr_arr, gp_first)
            TableDeltaBetweenBuffers(2 * 2, ma_0_buff, ma_1_buff, _s_OnCalculate_point_pow, 2, count, gp_first)
            if gp_first:
                gp_first = False
                gp_display_table = IS_
                TableCreate()
            if i_show_lines:
                BuffersLineClrChange()
            BufferBegin(rates_total - (9 + gp_first_bar + 1))
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global gp_display_table
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if StringFind(sparam, gp_ind_shortname) == 0:
            clickedChartObject = sparam
            if gp_display_table == IS_:
                if StringCompare(clickedChartObject, gp_name_butt, True) == 0:
                    gp_display_table = MINIMIZED
                    ObjectsDeleteAll(0, gp_ind_shortname)
                    TableButtonsSet(gp_display_table, gp_name_butt, i_distance_x + i_obj_height, i_distance_y, i_obj_height)
                    ChartRedraw()
                    return
            elif gp_display_table == MINIMIZED:
                gp_display_table = IS_
                TableCreate()
                ChartRedraw()
                return
            return
        return
    return

def InitAny():
    global gp_display_table, gp_first, gp_first_bar, gp_min_rates_total, gp_symbol, gp_tf
    gp_display_table = NO_
    gp_first = True
    gp_symbol = Symbol()
    gp_tf = Period()
    gp_first_bar = (1 if (i_shift < 1) else _int(i_shift))
    IndicatorShortNameSet(_GlobRef(globals(), 'gp_ind_shortname'), gp_symbol)
    if 9 < 2 or 9 > 30:
        Print('Line: ', 260, ', ', 'Error code: COLUMNS.')
        return False
    ma_period_arr = Arr.of([1, 1], fill=0, dyn=False, size=2)
    if not MADataInit(ma_period_arr):
        return False
    gp_min_rates_total = MinRatesTotalNumberSet(ma_period_arr)
    for row in range(0, 2 + 1):
        for i in range(0, 9):
            ga_clr_back_odd_row[row][i] = i_clr_back_main
    StringConcatenate(_GlobRef(globals(), 'gp_name_butt'), gp_ind_shortname, '_butt')
    ObjNameTwoDArray(5, ga_name, '_edit_')
    return True

def IndicatorShortNameSet(name, symbol):
    IndicatorShortNameCreate(name, symbol)
    IndicatorSetString(INDICATOR_SHORTNAME, name.v)
    return

def IndicatorShortNameCreate(name, symbol):
    return StringConcatenate(name, 'MA(table): ', symbol, ', x', i_distance_x, ', y', i_distance_y)

def MADataInit(ma_period_arr):
    if not MaPeriodSet(i_ma_0_period, 0 + 1, _ElemRef(ma_period_arr, 0)):
        return False
    if not MaPeriodSet(i_ma_1_period, 1 + 1, _ElemRef(ma_period_arr, 1)):
        return False
    PriseUse(ma_period_arr[0], i_ma_0_method, i_ma_0_applied_price, _ElemRef(ga_use_price, 0))
    PriseUse(ma_period_arr[1], i_ma_1_method, i_ma_1_applied_price, _ElemRef(ga_use_price, 1))
    if ga_use_price[0] == HANDLE:
        if not HandleIMACreate(_ElemRef(ga_ma_handle, 0), gp_symbol, gp_tf, ma_period_arr[0], 0, i_ma_0_method, i_ma_0_applied_price):
            return False
    if ga_use_price[1] == HANDLE:
        if not HandleIMACreate(_ElemRef(ga_ma_handle, 1), gp_symbol, gp_tf, ma_period_arr[1], 0, i_ma_1_method, i_ma_1_applied_price):
            return False
    return True

def MaPeriodSet(ma_period, index, result):
    if ma_period < 1 or ma_period > 3000:
        Alert('Indicator removed. Period Moving Averages (', IntegerToString(index), ': < 1 or > ', 3000, ')')
        return False
    result.v = ma_period
    return True

def PriseUse(ma_period, method, applied_price, use_price):
    if ma_period == 1 and method == MODE_SMA:
        if applied_price == PRICE_HIGH:
            use_price.v = HIGH
            return
        elif applied_price == PRICE_LOW:
            use_price.v = LOW
            return
        elif applied_price == PRICE_OPEN:
            use_price.v = OPEN
            return
        elif applied_price == PRICE_CLOSE:
            use_price.v = CLOSE
            return
    return

def HandleIMACreate(handle, symbol, tf, ma_period, ma_shift, ma_method, applied_price):
    handle.v = iMA(symbol, tf, ma_period, ma_shift, ma_method, applied_price)
    if handle.v == INVALID_HANDLE:
        Print('Line: ', 348, ', ', 'Failed to create handle of the iMA indicator: ', EnumToString(tf, 'ENUM_TIMEFRAMES'), ', error: ', GetLastError())
        return False
    return True

def MinRatesTotalNumberSet(period_arr):
    min_ = Arr.of([1, 1], fill=0, dyn=False, size=2)
    for i in range(2 - 1, 0 - 1, -1):
        min_[i] = period_arr[i] + 9 + gp_first_bar + 5
    return min_[ArrayMaximum(min_)]

def ObjNameTwoDArray(rows, array, pr='_'):
    text = Box(pr)
    for row in range(0, rows):
        for i in range(0, 9):
            StringConcatenate(text, gp_ind_shortname, pr, IntegerToString(row), IntegerToString(i))
            array[row][i] = text.v
    return

def ChIndicatorDelete(short_name, chart_id=0, sub_window=0):
    res = ChartIndicatorDelete(chart_id, sub_window, short_name)
    if not res:
        Print('Failed to delete indicator:"', short_name, '". Error: ', GetLastError())
        return False
    return True

def BuffersInit():
    IndicatorSetInteger(INDICATOR_DIGITS, DigitsSet(i_digits))
    SetIndexBuffer(0, ma_0_buff, INDICATOR_DATA)
    SetIndexBuffer(1, ma_1_buff, INDICATOR_DATA)
    name_buff_arr = Arr(2, "", dyn=False)
    BufferMaNameSet(_ElemRef(name_buff_arr, 0), 0 + 1, i_ma_0_period)
    BufferMaNameSet(_ElemRef(name_buff_arr, 1), 1 + 1, i_ma_1_period)
    for i in range(2 - 1, 0 - 1, -1):
        PlotIndexSetString(i, PLOT_LABEL, name_buff_arr[i])
    BufferBegin(9 + gp_first_bar + 1)
    for i in range(2 - 1, 0 - 1, -1):
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, clrNONE)
    for i in range(2 - 1, 0 - 1, -1):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    return

def DigitsSet(variant):
    return (Digits() if (i_digits == auto) else i_digits)

def BufferMaNameSet(name, index, ma_period):
    return StringConcatenate(name, index, ' MA(', IntegerToString(ma_period), '):')

def BufferBegin(count):
    for i in range(2 - 1, 0 - 1, -1):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, count)
    return

def ArrayResizeAndSetAsSeries(array, new_size, reserve_size=-1, flag=True):
    ArrayResize(array, new_size, reserve_size)
    array_size = ArraySize(array)
    if array_size > 1:
        ArraySetAsSeries(array, flag)
    elif array_size < 0:
        return False
    return True

def IndentDoubleSet(indent, point_pow, digits):
    max_value = 100 * point_pow
    int_value = MathAbs(indent)
    return (0.0 if (int_value == 0 or int_value >= max_value) else (indent * Point()))

def CopyPrice(symbol, tf, start_pos, count, buffer, indent, digits, use):
    dt = Arr(0, 0.0)
    if not ArrayResizeAndSetAsSeries(dt, count + start_pos, count + start_pos):
        Print('Line: ', 469, ', ', 'Error code = ', GetLastError())
        return False
    copied = -1
    if use == HIGH:
        copied = CopyHigh(symbol, tf, start_pos - 1, count, dt)
    elif use == LOW:
        copied = CopyLow(symbol, tf, start_pos - 1, count, dt)
    elif use == OPEN:
        copied = CopyOpen(symbol, tf, start_pos - 1, count, dt)
    elif use == CLOSE:
        copied = CopyClose(symbol, tf, start_pos - 1, count, dt)
    if copied < count:
        Print('Line: ', 480, ', ', 'Error code = ', GetLastError())
        return False
    else:
        IndentAdd(buffer, dt, indent, digits, start_pos, count)
    return True

def CopyIMA(indicator_handle, buffer_num, start_pos, count, indent, digits, buffer):
    dt = Arr(0, 0.0)
    if not ArrayResizeAndSetAsSeries(dt, count + start_pos, count + start_pos):
        Print('Line: ', 498, ', ', 'Error code = ', GetLastError())
        return (-1 != 0)
    if CopyBuffer(indicator_handle, buffer_num, start_pos - 1, count, dt) < 0:
        Print('Line: ', 502, ', ', 'Failed to copy data from the iMA indicator, error code: ', GetLastError())
        return False
    IndentAdd(buffer, dt, indent, digits, start_pos, count)
    return True

def IndentAdd(buffer, array, indent, digits, start_pos, count):
    ArraySetAsSeries(buffer, True)
    for i in range(count - 1, start_pos - 1, -1):
        buffer[i] = NormalizeDouble(array[i] + indent, digits)
    for i in range(start_pos - 1, 0 - 1, -1):
        buffer[i] = 0.0
    return

def BuffersLineClrChange():
    for i in range(2 - 1, 0 - 1, -1):
        if _s_BuffersLineClrChange_clr_arr[i] != ga_clr_back_odd_row[i][0] or _s_BuffersLineClrChange_clr_arr[i] == clrNONE:
            _s_BuffersLineClrChange_clr_arr[i] = ga_clr_back_odd_row[i][0]
            PlotIndexSetInteger(i, PLOT_LINE_COLOR, _s_BuffersLineClrChange_clr_arr[i])
    return

def TableValuesSet(row, buffers, point_pow, index, count, digits, change_clr, flag_first, chart_ID=0):
    delta_arr = Arr(9, 0.0, dyn=False)
    copy_old = 9 - count
    if copy_old > 0:
        if not flag_first:
            for i in range(9 - 1, count - 1, -1):
                ga_text_odd_row[index][i] = ga_text_odd_row[index][i - 1]
            for i in range(9 - 1, count - 1, -1):
                if ga_clr_back_odd_row[index][i] != ga_clr_back_odd_row[index][i - 1]:
                    ga_clr_back_odd_row[index][i] = ga_clr_back_odd_row[index][i - 1]
                    ga_clr_text_even_row[index][i] = ga_clr_text_even_row[index][i - 1]
                    change_clr[i] = True
                else:
                    if change_clr[i]:
                        change_clr[i] = False
            for i in range(9 - 1, count - 1, -1):
                ga_text_even_row[index][i] = ga_text_even_row[index][i - 1]
        else:
            for i in range(9 - 1, count - 1, -1):
                change_clr[i] = True
    for i in range(count - 1, 0 - 1, -1):
        ga_text_odd_row[index][i] = DoubleToString(buffers[i + gp_first_bar], digits)
    for i in range(count - 1, 0 - 1, -1):
        delta_arr[i] = NormalizeDouble((buffers[i + gp_first_bar] - buffers[i + gp_first_bar + 1]) * point_pow, 0)
        ga_text_even_row[index][i] = DoubleToString(delta_arr[i], 0)
    ClrChangeInArrays(index, count, delta_arr, ga_clr_back_odd_row, ga_clr_text_even_row, change_clr, 0)
    if gp_display_table == IS_:
        for i in range(9 - 1, 0 - 1, -1):
            if ObjectFind(0, ga_name[row][i]) > -1:
                ObjSetString(0, ga_name[row][i], _int(OBJPROP_TEXT), ga_text_odd_row[index][i])
            if change_clr[i] == True:
                ObjSetIntegerColor(0, ga_name[row][i], OBJPROP_BGCOLOR, ga_clr_back_odd_row[index][i])
        for i in range(9 - 1, 0 - 1, -1):
            if ObjectFind(0, ga_name[row + 1][i]) > -1:
                ObjSetString(0, ga_name[row + 1][i], _int(OBJPROP_TEXT), ga_text_even_row[index][i])
            if change_clr[i] == True:
                ObjSetIntegerColor(0, ga_name[row + 1][i], OBJPROP_COLOR, ga_clr_text_even_row[index][i])
                change_clr[i] = False
    return

def TableDeltaBetweenBuffers(row, buffers0, buffers1, point_pow, index_text, count, flag_first, chart_ID=0):
    delta_value = 0.0
    copy_old = 9 - count
    if copy_old > 0:
        if not flag_first:
            for i in range(9 - 1, count - 1, -1):
                ga_text_odd_row[index_text][i] = ga_text_odd_row[index_text][i - 1]
    for i in range(count - 1, 0 - 1, -1):
        delta_value = MathAbs((buffers0[i + gp_first_bar] - buffers1[i + gp_first_bar]) * point_pow)
        ga_text_odd_row[index_text][i] = DoubleToString(delta_value, 0)
    if gp_display_table == IS_:
        for i in range(9 - 1, 0 - 1, -1):
            if ObjectFind(chart_ID, ga_name[row][i]) > -1:
                ObjSetString(chart_ID, ga_name[row][i], _int(OBJPROP_TEXT), ga_text_odd_row[index_text][i])
        ChartRedraw()
    return

def ObjDelete(chart_ID, name):
    if ObjectFind(chart_ID, name) > -1:
        ObjectDelete(chart_ID, name)
    return

def TableCreate():
    global _s_TableCreate_ma_0_tooltip, _s_TableCreate_ma_1_tooltip
    if _s_TableCreate_ma_0_tooltip is _UNSET:
        _s_TableCreate_ma_0_tooltip = ObjTooltipSet(0, gp_tf, i_ma_0_period, i_ma_0_method, i_ma_0_applied_price)
    if _s_TableCreate_ma_1_tooltip is _UNSET:
        _s_TableCreate_ma_1_tooltip = ObjTooltipSet(1, gp_tf, i_ma_1_period, i_ma_1_method, i_ma_1_applied_price)
    tooltip = _s_TableCreate_ma_0_tooltip
    height = _int(i_obj_height)
    x_dis = TableTitleSet(_s_TableCreate_heigh_small)
    y_dis = _int(i_distance_y) + _s_TableCreate_heigh_small + 1
    y_dis_ch = 0
    row = 0
    step = 0
    TableButtonsSet(gp_display_table, gp_name_butt, x_dis * 9, y_dis, _idiv(_int(i_obj_height), 3) - 1)
    y_dis = y_dis + (1 * 9)
    while True:
        y_dis_ch = y_dis + ((height + _s_TableCreate_heigh_small) * (row - step)) + (1 * 2 * (row - step))
        if row == 2:
            tooltip = _s_TableCreate_ma_1_tooltip
        elif row == (2 * 2):
            tooltip = 'MA1 - MA2'
            height = _s_TableCreate_heigh_small
        for i in range(0, 9):
            if ObjectFind(0, ga_name[row][i]) < 0:
                EditCreate(0, ga_name[row][i], 0, i_distance_x + (x_dis * (i + 1)), y_dis_ch, i_obj_width, height, ga_text_odd_row[row - step][i], tooltip, 'Arial', i_font_size, ALIGN_RIGHT, True, CORNER_RIGHT_UPPER, i_clr_text_ma, ga_clr_back_odd_row[row - step][i], clrSnow, i_behind)
        row += 2
        step += 1
        if not (row < 5 and True):
            break
    width_small = _idiv(_int(i_obj_width), 3) * 2
    height = _int(i_obj_height)
    y_dis = y_dis + (height + 1)
    row = 1
    step = 1
    while True:
        tooltip = (_s_TableCreate_ma_1_tooltip if (row >= 2) else _s_TableCreate_ma_0_tooltip)
        y_dis_ch = y_dis + ((height + _s_TableCreate_heigh_small) * (row - step)) + (1 * 2 * (row - step))
        for i in range(0, 9):
            if ObjectFind(0, ga_name[row][i]) < 0:
                EditCreate(0, ga_name[row][i], 0, i_distance_x + (x_dis * (i + 1)), y_dis_ch, width_small, _s_TableCreate_heigh_small, ga_text_even_row[row - step][i], tooltip, 'Arial', i_font_size - 1, ALIGN_CENTER, True, CORNER_RIGHT_UPPER, ga_clr_text_even_row[row - step][i], i_clr_back_main, clrSnow, i_behind)
        row += 2
        step += 1
        if not (row < 5 and True):
            break
    return

def TableTitleSet(height):
    global _s_TableTitleSet_first
    tooltip = 'Number of bar'
    if _s_TableTitleSet_first:
        _s_TableTitleSet_first = False
        for i in range(9 - 1, 0 - 1, -1):
            StringConcatenate(_ElemRef(_s_TableTitleSet_name_arr, i), gp_ind_shortname, '_title_', i)
    for i in range(0, 9):
        if ObjectFind(0, _s_TableTitleSet_name_arr[i]) < 0:
            EditCreate(0, _s_TableTitleSet_name_arr[i], 0, i_distance_x + (_s_TableTitleSet_x_dis * (i + 1)), i_distance_y, i_obj_width, height, IntegerToString(gp_first_bar + i), tooltip, 'Arial', i_font_size - 1, ALIGN_CENTER, True, CORNER_RIGHT_UPPER, i_clr_text_delta, i_clr_back_main, clrSnow, i_behind)
    return _s_TableTitleSet_x_dis

def ObjTooltipSet(index, tf, ma_period, method, applied_price):
    text = Box('MA ')
    StringConcatenate(text, text.v, IntegerToString(index + 1), ': ', EnumToString(tf, 'ENUM_TIMEFRAMES'), ',\r\n', 'ma_period: ', ma_period, ',\r\n', EnumToString(method, 'ENUM_MA_METHOD'), ',\r\n', EnumToString(applied_price, 'ENUM_APPLIED_PRICE'))
    return text.v

def TableButtonsSet(flag, name, x, y, height):
    ObjDelete(0, name)
    if flag == IS_:
        ButtonCreate(0, name, 0, x, y, i_obj_width * 9, height, CORNER_RIGHT_UPPER, '', '\n', 'Arial', 0, clrBlack, i_clr_back_main, clrNONE, False, i_behind)
    elif flag == MINIMIZED:
        ButtonCreate(0, name, 0, x, y, height, height, CORNER_RIGHT_UPPER, CharToString(229), 'ID Lite Info MA', 'Wingdings', i_font_size + 1, clrBlack, i_clr_back_main, clrNONE, False, i_behind)
    return

def ButtonCreate(chart_ID=0, name='Button', sub_window=0, x=0, y=0, width=50, height=18, corner=CORNER_LEFT_UPPER, text='Button', tooltip='\n', font='Arial', font_size=10, clr=clrBlack, back_clr=0xD8E9EC, border_clr=clrNONE, state=False, back=False, selection=False, hidden=True, z_order=0, timeframes=_int(OBJ_ALL_PERIODS)):
    if not ObjectCreate(chart_ID, name, OBJ_BUTTON, sub_window, 0, 0):
        Print('Line: ', 807, ', ', 'ButtonCreate', ': failed to create the button!Error code=', GetLastError())
        return False
    ObjSetIntegerInt(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_XSIZE, width)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_YSIZE, height)
    ObjSetIntegerCorner(chart_ID, name, corner)
    ObjSetString(chart_ID, name, _int(OBJPROP_TOOLTIP), tooltip)
    ObjSetString(chart_ID, name, _int(OBJPROP_TEXT), text)
    ObjSetString(chart_ID, name, _int(OBJPROP_FONT), font)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjSetIntegerColor(chart_ID, name, OBJPROP_COLOR, clr)
    ObjSetIntegerColor(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
    ObjSetIntegerColor(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_BACK, back)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_STATE, state)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjSetIntegerLong(chart_ID, name, OBJPROP_ZORDER, z_order)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_TIMEFRAMES, timeframes)
    return True

def EditCreate(chart_ID=0, name='Edit', sub_window=0, x=0, y=0, width=50, height=20, text='Text', tooltip='\n', font='Arial', font_size=9, align=ALIGN_CENTER, read_only=False, corner=CORNER_LEFT_UPPER, clr=clrBlack, back_clr=clrWhite, border_clr=clrNONE, back=False, selection=False, hidden=True, z_order=0, timeframes=_int(OBJ_ALL_PERIODS)):
    if not ObjectCreate(chart_ID, name, OBJ_EDIT, sub_window, 0, 0):
        Print('Line: ', 865, ', ', 'EditCreate', ': failed to create "Edit" object! Error code = ', GetLastError())
        return False
    ObjSetIntegerInt(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_XSIZE, width)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_YSIZE, height)
    ObjSetString(chart_ID, name, _int(OBJPROP_TOOLTIP), tooltip)
    ObjSetString(chart_ID, name, _int(OBJPROP_TEXT), text)
    ObjSetString(chart_ID, name, _int(OBJPROP_FONT), font)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjSetIntegerAlign(chart_ID, name, align)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_READONLY, read_only)
    ObjSetIntegerCorner(chart_ID, name, corner)
    ObjSetIntegerColor(chart_ID, name, OBJPROP_COLOR, clr)
    ObjSetIntegerColor(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
    ObjSetIntegerColor(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_BACK, back)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjSetIntegerBool(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjSetIntegerLong(chart_ID, name, OBJPROP_ZORDER, z_order)
    ObjSetIntegerInt(chart_ID, name, OBJPROP_TIMEFRAMES, timeframes)
    return True

def ObjSetIntegerInt(chart_ID, name, pr, dt):
    if not ObjectSetInteger(chart_ID, name, pr, dt):
        Print('Line: ', 897, ', ', 'ObjSetIntegerInt', ', Error Code = ', GetLastError())
        return False
    return True

def ObjSetIntegerCorner(chart_ID, name, corner):
    if not ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner):
        Print('Line: ', 908, ', ', 'ObjSetIntegerCorner', ', Error Code = ', GetLastError())
        return False
    return True

def ObjSetString(chart_ID, name, pr, font):
    if not ObjectSetString(chart_ID, name, pr, font):
        Print('Line: ', 919, ', ', 'ObjSetString', ', Error Code = ', GetLastError())
        return False
    return True

def ObjSetIntegerColor(chart_ID, name, pr, dt):
    if not ObjectSetInteger(chart_ID, name, pr, dt):
        Print('Line: ', 930, ', ', 'ObjSetIntegerColor', ', Error Code = ', GetLastError())
        return False
    return True

def ObjSetIntegerLong(chart_ID, name, pr, dt):
    if not ObjectSetInteger(chart_ID, name, pr, dt):
        Print('Line: ', 941, ', ', 'ObjSetIntegerLong', ', Error Code = ', GetLastError())
        return False
    return True

def ObjSetIntegerBool(chart_ID, name, pr, dt):
    if not ObjectSetInteger(chart_ID, name, pr, dt):
        Print('Line: ', 951, ', ', 'ObjSetIntegerBool', ', Error Code = ', GetLastError())
        return False
    return True

def ObjSetIntegerAlign(chart_ID, name, align):
    if not ObjectSetInteger(chart_ID, name, OBJPROP_ALIGN, align):
        Print('Line: ', 961, ', ', 'ObjSetIntegerAlign', ', Error Code = ', GetLastError())
        return False
    return True

def ClrChangeInArrays(row, columns, price, back_clr, clr, change_clr, digits):
    clr_0 = clrNONE
    clr_1 = clrNONE
    for i in range(columns - 1, 0 - 1, -1):
        if NormalizeDouble(price[i], digits) > 0:
            clr_1 = i_clr_back_up
            clr_0 = clr_1
        elif NormalizeDouble(price[i], digits) < 0:
            clr_1 = i_clr_back_down
            clr_0 = clr_1
        elif NormalizeDouble(price[i], digits) == 0:
            clr_0 = i_clr_back_main
            clr_1 = i_clr_text_delta
        if back_clr[row][i] != clr_0:
            back_clr[row][i] = clr_0
            clr[row][i] = clr_1
            change_clr[i] = True
        else:
            change_clr[i] = False
    return

def StopDataClear():
    global _s_StopDataClear_change
    if _s_StopDataClear_change == 2:
        _s_StopDataClear_change = 0
        return True
    _s_StopDataClear_change += 1
    return False

# ---- static local variables
_s_OnCalculate_time_new_bar = 0
_s_OnCalculate_limit = 0
_s_OnCalculate_digits = _UNSET
_s_OnCalculate_point_pow = _UNSET
_s_OnCalculate_ma_0_indent = _UNSET
_s_OnCalculate_ma_1_indent = _UNSET
_s_OnCalculate_ma_0_change_clr_arr = Arr(9, False, dyn=False)
_s_OnCalculate_ma_1_change_clr_arr = Arr(9, False, dyn=False)
_s_BuffersLineClrChange_clr_arr = Arr.of([clrNONE, clrNONE], fill=0, dyn=False, size=2)
_s_TableCreate_ma_0_tooltip = _UNSET
_s_TableCreate_ma_1_tooltip = _UNSET
_s_TableCreate_heigh_small = _idiv(_int(i_obj_height), 3) * 2
_s_TableTitleSet_x_dis = _int(i_obj_width) + 1
_s_TableTitleSet_name_arr = Arr(9, "", dyn=False)
_s_TableTitleSet_first = True
_s_StopDataClear_change = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IdLiteInfoMa(_MQL5Indicator):
    name = 'id_lite_info_ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'i_show_lines': False,  # Show lines MA
        'i_ma_0_indent': 0,  # Shift in points from MA1 (-/+ Down or Up)
        'i_ma_1_indent': 0,  # Shift in points from MA2 (-/+ Down or Up)
        'i_digits': _Choice({-1: 'current chart', 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}, default=-1),  # Decimal digits
        'i_shift': 1,  # Shift (bar for first value):
        'i_ma_0_period': 1,  # Period Moving Averages (1)>= 1 or <= 3000:
        'i_ma_0_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method (1):
        'i_ma_0_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=3),  # Apply to (1):
        'i_ma_1_period': 1,  # Period Moving Averages (2)>= 1 or <= 3000:
        'i_ma_1_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method (2):
        'i_ma_1_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=4),  # Apply to (2):
        'i_distance_x': 3,  # X coordinate
        'i_distance_y': 3,  # Y coordinate
        'i_obj_width': 60,  # Width
        'i_obj_height': 18,  # Height
        'i_font_size': 9,  # Font size
        'i_behind': True,  # Table of the indicator behind bars
    }

