"""CHO Smoothed Arrow 2 — converted from MQL5: MQL5 Indicators/CHO Smoothed Arrow 2/CHO Smoothed Arrow 2.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 2.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '2.000', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16748574], 2: [4678655]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up', 2: 'Down'}, 'levels': [], 'description': [], 'name': 'CHO Smoothed Arrow 2', 'source': 'MQL5 Indicators/CHO Smoothed Arrow 2/CHO Smoothed Arrow 2.mq5', 'folder': 'CHO Smoothed Arrow 2', 'inputs': [{'mql': 'Inp_CHO_fast_ma_period', 'py': 'Inp_CHO_fast_ma_period', 'param': 'Inp_CHO_fast_ma_period', 'type': 'int', 'default': 3, 'label': 'CHO: fast period', 'sinput': False}, {'mql': 'Inp_CHO_slow_ma_period', 'py': 'Inp_CHO_slow_ma_period', 'param': 'Inp_CHO_slow_ma_period', 'type': 'int', 'default': 10, 'label': 'CHO: slow period', 'sinput': False}, {'mql': 'Inp_CHO_ma_method', 'py': 'Inp_CHO_ma_method', 'param': 'Inp_CHO_ma_method', 'type': 'int', 'default': 1, 'label': 'CHO: smoothing type', 'sinput': False}, {'mql': 'Inp_CHO_applied_volume', 'py': 'Inp_CHO_applied_volume', 'param': 'Inp_CHO_applied_volume', 'type': 'int', 'default': 0, 'label': 'CHO: type of volume', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 6, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}, {'mql': 'Inp_Up_ArrowCode', 'py': 'Inp_Up_ArrowCode', 'param': 'Inp_Up_ArrowCode', 'type': 'uchar', 'default': 200, 'label': "Arrow 'Up': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_Up_ArrowShift', 'py': 'Inp_Up_ArrowShift', 'param': 'Inp_Up_ArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'Up': vertical shift in pixel", 'sinput': False}, {'mql': 'Inp_Down_ArrowCode', 'py': 'Inp_Down_ArrowCode', 'param': 'Inp_Down_ArrowCode', 'type': 'uchar', 'default': 202, 'label': "Arrow 'Down': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_Down_ArrowShift', 'py': 'Inp_Down_ArrowShift', 'param': 'Inp_Down_ArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'Down': vertical shift in pixel", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_CHO_fast_ma_period = _input('Inp_CHO_fast_ma_period', 3)  # CHO: fast period
Inp_CHO_slow_ma_period = _input('Inp_CHO_slow_ma_period', 10)  # CHO: slow period
Inp_CHO_ma_method = _input('Inp_CHO_ma_method', MODE_EMA)  # CHO: smoothing type
Inp_CHO_applied_volume = _input('Inp_CHO_applied_volume', VOLUME_TICK)  # CHO: type of volume
Inp_MA_ma_period = _input('Inp_MA_ma_period', 6)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_CLOSE)  # MA: type of price
Inp_Up_ArrowCode = _input('Inp_Up_ArrowCode', 200)  # Arrow 'Up': code (font Wingdings)
Inp_Up_ArrowShift = _input('Inp_Up_ArrowShift', 10)  # Arrow 'Up': vertical shift in pixel
Inp_Down_ArrowCode = _input('Inp_Down_ArrowCode', 202)  # Arrow 'Down': code (font Wingdings)
Inp_Down_ArrowShift = _input('Inp_Down_ArrowShift', 10)  # Arrow 'Down': vertical shift in pixel
UpBuffer = Arr(0, 0.0)
DownBuffer = Arr(0, 0.0)
CHOBuffer = Arr(0, 0.0)
CHO_SmoothedBuffer = Arr(0, 0.0)
handle_iChaikin = 0  # variable for storing the handle of the iChaikin indicator
handle_iMA_iChaikin = 0  # variable for storing the handle of the iChaikin indicator
bars_calculated = 0  # we will keep the number of values in the Moving Average indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iChaikin, handle_iMA_iChaikin, m_init_error
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DownBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, CHOBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, CHO_SmoothedBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, Inp_Up_ArrowCode)
    PlotIndexSetInteger(1, PLOT_ARROW, Inp_Down_ArrowCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, Inp_Up_ArrowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -Inp_Down_ArrowShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    handle_iChaikin = iChaikin(Symbol(), Period(), Inp_CHO_fast_ma_period, Inp_CHO_slow_ma_period, Inp_CHO_ma_method, Inp_CHO_applied_volume)
    if handle_iChaikin == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iChaikin indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_iChaikin = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iChaikin)
    if handle_iMA_iChaikin == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA iChaikin indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
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
    price = ""
    _sw2 = Inp_MA_applied_price
    if _sw2 == PRICE_CLOSE:
        price = 'Close'
    elif _sw2 == PRICE_OPEN:
        price = 'Open'
    elif _sw2 == PRICE_HIGH:
        price = 'High'
    elif _sw2 == PRICE_LOW:
        price = 'Low'
    elif _sw2 == PRICE_MEDIAN:
        price = 'Median'
    elif _sw2 == PRICE_TYPICAL:
        price = 'Typical'
    elif _sw2 == PRICE_WEIGHTED:
        price = 'Weighted'
    else:
        price = 'unknown ma price'
    short_name = StringFormat('CHO(slow %d,fast %d) Smoothed(%d,%s,%s) Arrow', Inp_CHO_slow_ma_period, Inp_CHO_fast_ma_period, Inp_MA_ma_period, mode, price)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_cho = BarsCalculated(handle_iChaikin)
    if calculated_cho <= 0:
        PrintFormat('BarsCalculated(handle_iChaikin) returned %d, error code %d', calculated_cho, GetLastError())
        return 0
    calculated_ma_cho = BarsCalculated(handle_iMA_iChaikin)
    if calculated_ma_cho <= 0:
        PrintFormat('BarsCalculated(handle_iMA_iChaikin) returned %d, error code %d', calculated_ma_cho, GetLastError())
        return 0
    if calculated_cho != calculated_ma_cho:
        PrintFormat('BarsCalculated(handle_iChaikin) returned %d, BarsCalculated(handle_iMA_iChaikin) returned %d', calculated_cho, calculated_ma_cho)
        return 0
    calculated = calculated_cho
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(CHOBuffer, handle_iChaikin, values_to_copy):
        return 0
    if not FillArrayFromBuffer(CHO_SmoothedBuffer, handle_iMA_iChaikin, values_to_copy):
        return 0
    bars_calculated = calculated
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        UpBuffer[0] = 0.0
        DownBuffer[0] = 0.0
        limit = 1
    for i in range(limit, rates_total):
        UpBuffer[i] = 0.0
        DownBuffer[i] = 0.0
        if CHOBuffer[i - 1] < CHO_SmoothedBuffer[i - 1] and CHOBuffer[i] > CHO_SmoothedBuffer[i]:
            if CHOBuffer[i] < 0.0:
                UpBuffer[i] = low[i]
        if CHOBuffer[i - 1] > CHO_SmoothedBuffer[i - 1] and CHOBuffer[i] < CHO_SmoothedBuffer[i]:
            if CHOBuffer[i] > 0.0:
                DownBuffer[i] = high[i]
    return rates_total

def FillArrayFromBuffer(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA_iChaikin != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_iChaikin)
    if handle_iChaikin != INVALID_HANDLE:
        IndicatorRelease(handle_iChaikin)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CHOSmoothedArrow2(_MQL5Indicator):
    name = 'CHO Smoothed Arrow 2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_CHO_fast_ma_period': 3,  # CHO: fast period
        'Inp_CHO_slow_ma_period': 10,  # CHO: slow period
        'Inp_CHO_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # CHO: smoothing type
        'Inp_CHO_applied_volume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # CHO: type of volume
        'Inp_MA_ma_period': 6,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
        'Inp_Up_ArrowCode': 200,  # Arrow 'Up': code (font Wingdings)
        'Inp_Up_ArrowShift': 10,  # Arrow 'Up': vertical shift in pixel
        'Inp_Down_ArrowCode': 202,  # Arrow 'Down': code (font Wingdings)
        'Inp_Down_ArrowShift': 10,  # Arrow 'Down': vertical shift in pixel
    }

