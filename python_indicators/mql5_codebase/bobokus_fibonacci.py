"""Bobokus_Fibonacci — converted from MQL5: MQL5 Indicators/Bobokus Fibonacci/Bobokus_Fibonacci.mq5

Bobokus Fibonacci Retracement
Copyright: Copyright © 2021, Dark Ryd3r; Link: https://twitter.com/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2021, Dark Ryd3r', 'link': 'https://twitter.com/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Bobokus Fibonacci Retracement'], 'name': 'Bobokus_Fibonacci', 'source': 'MQL5 Indicators/Bobokus Fibonacci/Bobokus_Fibonacci.mq5', 'folder': 'Bobokus Fibonacci', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': 'Chart period', 'sinput': False}, {'mql': 'Fib_Levels', 'py': 'Fib_Levels', 'param': None, 'type': 'string', 'default': '0.382, 0.5, 0.618', 'label': 'Add any other levels seperated by commas', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
hideit = False
m_fibo_name = 'BobokusFibo'
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
TimeFrame = _input('TimeFrame', PERIOD_D1)  # Chart period
Fib_Levels = _input('Fib_Levels', '0.382, 0.5, 0.618')  # Add any other levels seperated by commas
Levelclr = clrCornflowerBlue
LevelStyle = STYLE_DASHDOT
levels_values = Arr(0, 0.0)  # Array of level values
levels_descriptions = Arr(0, "")  # Array of level descriptions
level_names = 'Short Resistance %$,Pivot %$,Long Support %$'  # Array of level descriptions

def OnInit():
    global hideit
    if Period() >= TimeFrame:
        hideit = True
        return INIT_SUCCEEDED
    ArraySetAsSeries(m_rates_W1, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bobokus_Fibonacci')
    ChartRedraw()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, m_fibo_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_prev_bars
    if hideit:
        return 0
    if rates_total < 10:
        return 0
    start_pos = 0
    count = 3
    if CopyRates(Symbol(), TimeFrame, start_pos, count, m_rates_W1) != count:
        return rates_total
    time_0 = m_rates_W1[0].time
    if time_0 == m_prev_bars:
        return rates_total
    m_prev_bars = time_0
    m_rates_M1 = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(m_rates_M1, True)
    count_M1 = CopyRates(Symbol(), PERIOD_M1, _DT(m_rates_W1[1].time), _DT(m_rates_W1[0].time), m_rates_M1)
    if count_M1 < 2:
        time_0 = 0
        return rates_total
    time_high = 0
    time_low = 0
    price_high = DBL_MIN
    price_low = DBL_MAX
    for i in range(0, count_M1):
        if m_rates_M1[i].high > price_high:
            time_high = m_rates_M1[i].time
            price_high = m_rates_M1[i].high
        if m_rates_M1[i].low < price_low:
            time_low = m_rates_M1[i].time
            price_low = m_rates_M1[i].low
    fibo_price_start = (price_high if (time_high < time_low) else price_low)
    fibo_price_end = (price_low if (time_high < time_low) else price_high)
    fibo_time_start = (time_high if (time_high < time_low) else time_low)
    fibo_time_end = (time_low if (time_high < time_low) else time_high)
    if ObjectFind(0, m_fibo_name) < 0:
        FiboLevelsCreate(0, m_fibo_name, 0, fibo_time_start, fibo_price_start, fibo_time_end, fibo_price_end)
        SetFiboLevels(m_fibo_name, levels_values)
        SetFiboDescriptions(m_fibo_name, levels_descriptions)
    else:
        FiboLevelsPointChange(0, m_fibo_name, 0, fibo_time_start, fibo_price_start)
        FiboLevelsPointChange(0, m_fibo_name, 1, fibo_time_end, fibo_price_end)
    ChartRedraw()
    return rates_total

def FiboLevelsCreate(chart_ID=0, name='Fibo_Bobokus', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrSnow, style=STYLE_DASHDOT, width=2, back=False, selection=True, ray_left=False, ray_right=True, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    ChangeFiboLevelsEmptyPoints(time1, price1, time2, price2)
    StringToDoubleArray(Fib_Levels, levels_values)
    StringToStringArray(level_names, levels_descriptions)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_FIBO, sub_window, time1.v, price1.v, time2.v, price2.v):
        Print('FiboLevelsCreate', ': failed to create "Fibonacci Retracement"! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    levels = ObjectGetInteger(chart_ID, name, OBJPROP_LEVELS)
    for i in range(0, levels):
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, i, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def ChangeFiboLevelsEmptyPoints(time1, price1, time2, price2):
    if not time2.v:
        time2.v = TimeCurrent()
    if not price2.v:
        price2.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time1.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time2.v), 10, temp)
        time1.v = temp[0]
    if not price1.v:
        price1.v = price2.v - (200 * SymbolInfoDouble(Symbol(), SYMBOL_POINT))

def FiboLevelsPointChange(chart_ID=0, name='Fibo_W1', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('FiboLevelsPointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def StringToDoubleArray(_haystack, _result, _delimiter=','):
    haystack_pieces = Arr(0, "")
    pieces_count = 0
    i = 0
    current_number = ''
    pieces_count = StringSplit(_haystack, StringGetCharacter(_delimiter, 0), haystack_pieces)
    if pieces_count > 0:
        ArrayResize(_result, pieces_count)
        i = 0
        for i in range(i, pieces_count):
            StringTrimLeft(_ElemRef(haystack_pieces, i))
            StringTrimRight(_ElemRef(haystack_pieces, i))
            _result[i] = StringToDouble(haystack_pieces[i])
        else:
            i = _range_end(i, pieces_count, 1)
    else:
        ArrayResize(_result, 1)
        _result[0] = 0.0

def StringToStringArray(_haystack, _result, _delimiter=','):
    haystack_pieces = Arr(0, "")
    pieces_count = 0
    i = 0
    current_number = ''
    pieces_count = StringSplit(_haystack, StringGetCharacter(_delimiter, 0), haystack_pieces)
    if pieces_count > 0:
        ArrayResize(_result, pieces_count)
        i = 0
        for i in range(i, pieces_count):
            StringTrimLeft(_ElemRef(haystack_pieces, i))
            StringTrimRight(_ElemRef(haystack_pieces, i))
            _result[i] = haystack_pieces[i]
        else:
            i = _range_end(i, pieces_count, 1)
    else:
        ArrayResize(_result, 1)
        _result[0] = ""

def SetFiboLevels(_object_name, _levels_values):
    i = 0
    levels_count = ArraySize(_levels_values)
    ObjectSetInteger(0, _object_name, OBJPROP_LEVELS, levels_count)
    i = 0
    for i in range(i, levels_count):
        ObjectSetDouble(0, _object_name, OBJPROP_LEVELVALUE, i, _levels_values[i])
        ObjectSetInteger(0, _object_name, OBJPROP_LEVELCOLOR, i, Levelclr)
        ObjectSetInteger(0, _object_name, OBJPROP_LEVELSTYLE, i, LevelStyle)
    else:
        i = _range_end(i, levels_count, 1)
    ChartRedraw(0)

def SetFiboDescriptions(_object_name, _levels_descriptions):
    i = 0
    levels_count = _int(ObjectGetInteger(0, _object_name, OBJPROP_LEVELS))
    array_size = ArraySize(_levels_descriptions)
    i = 0
    for i in range(i, levels_count):
        Cuttext = DoubleToString(levels_values[i])
        if array_size > 0 and i < array_size:
            ObjectSetString(0, _object_name, OBJPROP_LEVELTEXT, i, _levels_descriptions[i])
        else:
            ObjectSetString(0, _object_name, OBJPROP_LEVELTEXT, i, StringSubstr(Cuttext, 0, StringLen(Cuttext) - 5) + ' %$')
    else:
        i = _range_end(i, levels_count, 1)
    ChartRedraw(0)

# ---- global variables initialised from expressions
m_rates_W1 = Arr(0, 0, factory=MqlRates)  # rates W1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BobokusFibonacci(_MQL5Indicator):
    name = 'Bobokus_Fibonacci'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Chart period
    }

