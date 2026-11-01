"""High Low _luster — converted from MQL5: MQL5 Indicators/High Low Сluster/High Low _luster.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.005

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.005', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329434]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': [], 'name': 'High Low _luster', 'source': 'MQL5 Indicators/High Low Сluster/High Low _luster.mq5', 'folder': 'High Low Сluster', 'inputs': [{'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 9, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_shift', 'py': 'Inp_MA_ma_shift', 'param': 'Inp_MA_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_ma_period = _input('Inp_MA_ma_period', 9)  # MA: averaging period
Inp_MA_ma_shift = _input('Inp_MA_ma_shift', 0)  # MA: horizontal shift
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_CLOSE)  # MA: type of price
iMABuffer = Arr(0, 0.0)
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Moving Average indicator
m_init_error = False  # error on InInit
m_name = ''
m_time_left = 0  # first point time, "0" -> D'1970.01.01 00:00'
m_price_min = DBL_MAX  # first point price
m_time_right = 0  # second point time, "0" -> D'1970.01.01 00:00'
m_price_max = DBL_MIN  # second point price
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
m_prefix = 'HLC_'

def OnInit():
    global handle_iMA, m_init_error
    SetIndexBuffer(0, iMABuffer, INDICATOR_DATA)
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, Inp_MA_ma_shift, Inp_MA_ma_method, Inp_MA_applied_price)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    mode = ""
    _sw1 = Inp_MA_ma_method
    if _sw1 == MODE_EMA:
        mode = 'EMA'
    elif _sw1 == MODE_LWMA:
        mode = 'LWMA'
    elif _sw1 == MODE_SMA:
        mode = 'SMA'
    elif _sw1 == MODE_SMMA:
        mode = 'SMMA'
    else:
        mode = 'unknown mode'
    price = StringSubstr(EnumToString(Inp_MA_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1)
    short_name = StringFormat('High LowCluster(%d,%d,%s,%s)', Inp_MA_ma_period, Inp_MA_ma_shift, mode, price)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated, m_name, m_prev_bars, m_price_max, m_price_min, m_time_left, m_time_right
    if rates_total < 10:
        return 0
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iMA)
    if calculated <= 0:
        PrintFormat('BarsCalculated(handle_iMA) returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iMABuffer, Inp_MA_ma_shift, handle_iMA, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if limit < 4:
        limit = 4
    for i in range(limit, rates_total):
        if time[i] == m_prev_bars:
            continue
        m_prev_bars = time[i]
        if open[i - 1] < iMABuffer[i - 1] and close[i - 1] > iMABuffer[i - 1]:
            VariableInitialization()
            if (open[i - 2] > iMABuffer[i - 2] and close[i - 2] < iMABuffer[i - 2]) or (open[i - 3] > iMABuffer[i - 3] and close[i - 3] < iMABuffer[i - 3]):
                VariableInitialization()
                continue
            m_time_right = time[i - 2]
            for j in range(i - 2, 1 - 1, -1):
                if high[j] > m_price_max:
                    m_price_max = high[j]
                if low[j] < m_price_min:
                    m_price_min = low[j]
                if open[j - 1] > iMABuffer[j - 1] and close[j - 1] < iMABuffer[j - 1]:
                    m_name = TimeToString(time[j], TIME_DATE | TIME_MINUTES) + '-' + TimeToString(m_time_right, TIME_DATE | TIME_MINUTES)
                    m_time_left = time[j]
                    if m_time_right != m_time_left:
                        RectangleCreate(ChartID(), m_prefix + m_name, 0, m_time_left, m_price_min, m_time_right, m_price_max, clrRed, STYLE_DASH, 2)
                        VariableInitialization()
                        break
                    break
            VariableInitialization()
            continue
        else:
            if open[i - 1] > iMABuffer[i - 1] and close[i - 1] < iMABuffer[i - 1]:
                VariableInitialization()
                if (open[i - 2] < iMABuffer[i - 2] and close[i - 2] > iMABuffer[i - 2]) or (open[i - 3] < iMABuffer[i - 3] and close[i - 3] > iMABuffer[i - 3]):
                    VariableInitialization()
                    continue
                m_time_right = time[i - 2]
                for j in range(i - 2, 1 - 1, -1):
                    if high[j] > m_price_max:
                        m_price_max = high[j]
                    if low[j] < m_price_min:
                        m_price_min = low[j]
                    if open[j - 1] < iMABuffer[j - 1] and close[j - 1] > iMABuffer[j - 1]:
                        m_name = TimeToString(time[j], TIME_DATE | TIME_MINUTES) + '-' + TimeToString(m_time_right, TIME_DATE | TIME_MINUTES)
                        m_time_left = time[j]
                        if m_time_right != m_time_left:
                            RectangleCreate(ChartID(), m_prefix + m_name, 0, m_time_left, m_price_min, m_time_right, m_price_max, clrBlue, STYLE_DASH, 2)
                            VariableInitialization()
                            break
                        break
                VariableInitialization()
                continue
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), m_prefix, 0, OBJ_RECTANGLE)
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)

def RectangleCreate(chart_ID=0, name='Rectangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=False, back=False, selection=False, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    ChangeRectangleEmptyPoints(time1, price1, time2, price2)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_RECTANGLE, sub_window, time1.v, price1.v, time2.v, price2.v):
        Print('RectangleCreate', ': failed to create a rectangle! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_FILL, fill)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def RectanglePointChange(chart_ID=0, name='Rectangle', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('RectanglePointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def RectangleDelete(chart_ID=0, name='Rectangle'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('RectangleDelete', ': failed to delete rectangle! Error code = ', GetLastError())
        return False
    return True

def ChangeRectangleEmptyPoints(time1, price1, time2, price2):
    if not time1.v:
        time1.v = TimeCurrent()
    if not price1.v:
        price1.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time2.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time1.v), 10, temp)
        time2.v = temp[0]
    if not price2.v:
        price2.v = price1.v - (300 * SymbolInfoDouble(Symbol(), SYMBOL_POINT))

def VariableInitialization():
    global m_name, m_price_max, m_price_min, m_time_left, m_time_right
    m_name = ''
    m_time_left = 0
    m_price_min = DBL_MAX
    m_time_right = 0
    m_price_max = DBL_MIN


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HighLowLuster(_MQL5Indicator):
    name = 'High Low _luster'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_ma_period': 9,  # MA: averaging period
        'Inp_MA_ma_shift': 0,  # MA: horizontal shift
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
    }

