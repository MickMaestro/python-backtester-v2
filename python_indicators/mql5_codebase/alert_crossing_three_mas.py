"""Alert Crossing Three MAs — converted from MQL5: MQL5 Indicators/Alert Crossing Three MAs/Alert Crossing Three MAs.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.501

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.501', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [36095], 2: [8388736], 3: [9470064], 4: [11829830], 5: [255]}, 'widths': {1: 3, 2: 2, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'MA Fast', 2: 'MA Medium', 3: 'MA Slow', 4: 'UP', 5: 'DOWN'}, 'levels': [], 'description': [], 'name': 'Alert Crossing Three MAs', 'source': 'MQL5 Indicators/Alert Crossing Three MAs/Alert Crossing Three MAs.mq5', 'folder': 'Alert Crossing Three MAs', 'inputs': [{'mql': 'Inp_MA_Fast_ma_period', 'py': 'Inp_MA_Fast_ma_period', 'param': 'Inp_MA_Fast_ma_period', 'type': 'int', 'default': 50, 'label': 'MA Fast: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_shift', 'py': 'Inp_MA_Fast_ma_shift', 'param': 'Inp_MA_Fast_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Fast: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_method', 'py': 'Inp_MA_Fast_ma_method', 'param': 'Inp_MA_Fast_ma_method', 'type': 'int', 'default': 1, 'label': 'MA Fast: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Fast_applied_price', 'py': 'Inp_MA_Fast_applied_price', 'param': 'Inp_MA_Fast_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Fast: type of price', 'sinput': False}, {'mql': 'Inp_MA_Medium_ma_period', 'py': 'Inp_MA_Medium_ma_period', 'param': 'Inp_MA_Medium_ma_period', 'type': 'int', 'default': 100, 'label': 'MA Medium: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Medium_ma_shift', 'py': 'Inp_MA_Medium_ma_shift', 'param': 'Inp_MA_Medium_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Medium: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Medium_ma_method', 'py': 'Inp_MA_Medium_ma_method', 'param': 'Inp_MA_Medium_ma_method', 'type': 'int', 'default': 1, 'label': 'MA Medium: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Medium_applied_price', 'py': 'Inp_MA_Medium_applied_price', 'param': 'Inp_MA_Medium_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Medium: type of price', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_period', 'py': 'Inp_MA_Slow_ma_period', 'param': 'Inp_MA_Slow_ma_period', 'type': 'int', 'default': 240, 'label': 'MA Slow: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_shift', 'py': 'Inp_MA_Slow_ma_shift', 'param': 'Inp_MA_Slow_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Slow: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_method', 'py': 'Inp_MA_Slow_ma_method', 'param': 'Inp_MA_Slow_ma_method', 'type': 'int', 'default': 3, 'label': 'MA Slow: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Slow_applied_price', 'py': 'Inp_MA_Slow_applied_price', 'param': 'Inp_MA_Slow_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Slow: type of price', 'sinput': False}, {'mql': 'Inp_UP_Arrow_Code', 'py': 'Inp_UP_Arrow_Code', 'param': 'Inp_UP_Arrow_Code', 'type': 'uchar', 'default': 241, 'label': "Arrow 'UP': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_UP_Arrow_Shift', 'py': 'Inp_UP_Arrow_Shift', 'param': 'Inp_UP_Arrow_Shift', 'type': 'int', 'default': 10, 'label': "Arrow 'UP': vertical shift in pixel", 'sinput': False}, {'mql': 'Inp_DOWN_Arrow_Code', 'py': 'Inp_DOWN_Arrow_Code', 'param': 'Inp_DOWN_Arrow_Code', 'type': 'uchar', 'default': 242, 'label': "Arrow 'DOWN': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_DOWN_Arrow_Shift', 'py': 'Inp_DOWN_Arrow_Shift', 'param': 'Inp_DOWN_Arrow_Shift', 'type': 'int', 'default': 10, 'label': "Arrow 'DOWN': vertical shift in pixel", 'sinput': False}, {'mql': 'InpSoundName', 'py': 'InpSoundName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Name', 'sinput': False}, {'mql': 'InpSoundRepetitions', 'py': 'InpSoundRepetitions', 'param': 'InpSoundRepetitions', 'type': 'uchar', 'default': 3, 'label': 'Repetitions', 'sinput': False}, {'mql': 'InpSoundPause', 'py': 'InpSoundPause', 'param': 'InpSoundPause', 'type': 'uchar', 'default': 3, 'label': 'Pause, in seconds', 'sinput': False}, {'mql': 'InpUseSound', 'py': 'InpUseSound', 'param': 'InpUseSound', 'type': 'bool', 'default': False, 'label': 'Use Sound', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'bool', 'default': True, 'label': 'Use Alert', 'sinput': False}, {'mql': 'InpUseMail', 'py': 'InpUseMail', 'param': 'InpUseMail', 'type': 'bool', 'default': True, 'label': 'Use Send mail', 'sinput': False}, {'mql': 'InpUseNotification', 'py': 'InpUseNotification', 'param': 'InpUseNotification', 'type': 'bool', 'default': True, 'label': 'Use Send notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_Fast_ma_period = _input('Inp_MA_Fast_ma_period', 50)  # MA Fast: averaging period
Inp_MA_Fast_ma_shift = _input('Inp_MA_Fast_ma_shift', 0)  # MA Fast: horizontal shift
Inp_MA_Fast_ma_method = _input('Inp_MA_Fast_ma_method', MODE_EMA)  # MA Fast: smoothing type
Inp_MA_Fast_applied_price = _input('Inp_MA_Fast_applied_price', PRICE_CLOSE)  # MA Fast: type of price
Inp_MA_Medium_ma_period = _input('Inp_MA_Medium_ma_period', 100)  # MA Medium: averaging period
Inp_MA_Medium_ma_shift = _input('Inp_MA_Medium_ma_shift', 0)  # MA Medium: horizontal shift
Inp_MA_Medium_ma_method = _input('Inp_MA_Medium_ma_method', MODE_EMA)  # MA Medium: smoothing type
Inp_MA_Medium_applied_price = _input('Inp_MA_Medium_applied_price', PRICE_CLOSE)  # MA Medium: type of price
Inp_MA_Slow_ma_period = _input('Inp_MA_Slow_ma_period', 240)  # MA Slow: averaging period
Inp_MA_Slow_ma_shift = _input('Inp_MA_Slow_ma_shift', 0)  # MA Slow: horizontal shift
Inp_MA_Slow_ma_method = _input('Inp_MA_Slow_ma_method', MODE_LWMA)  # MA Slow: smoothing type
Inp_MA_Slow_applied_price = _input('Inp_MA_Slow_applied_price', PRICE_CLOSE)  # MA Slow: type of price
Inp_UP_Arrow_Code = _input('Inp_UP_Arrow_Code', 241)  # Arrow 'UP': code (font Wingdings)
Inp_UP_Arrow_Shift = _input('Inp_UP_Arrow_Shift', 10)  # Arrow 'UP': vertical shift in pixel
Inp_DOWN_Arrow_Code = _input('Inp_DOWN_Arrow_Code', 242)  # Arrow 'DOWN': code (font Wingdings)
Inp_DOWN_Arrow_Shift = _input('Inp_DOWN_Arrow_Shift', 10)  # Arrow 'DOWN': vertical shift in pixel
InpSoundName = _input('InpSoundName', 'alert.wav')  # Sound Name
InpSoundRepetitions = _input('InpSoundRepetitions', 3)  # Repetitions
InpSoundPause = _input('InpSoundPause', 3)  # Pause, in seconds
InpUseSound = _input('InpUseSound', False)  # Use Sound
InpUseAlert = _input('InpUseAlert', True)  # Use Alert
InpUseMail = _input('InpUseMail', True)  # Use Send mail
InpUseNotification = _input('InpUseNotification', True)  # Use Send notification
MA_Fast_Buffer = Arr(0, 0.0)
MA_Medium_Buffer = Arr(0, 0.0)
MA_Slow_Buffer = Arr(0, 0.0)
UPBuffer = Arr(0, 0.0)
DOWNBuffer = Arr(0, 0.0)
handle_iMA_Fast = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Medium = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Slow = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Moving Averages Convergence/Divergence indicator
start = 0
m_last_sound = 0  # "0" -> D'1970.01.01 00:00';
m_repetitions = 0
m_text = ''
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA_Fast, handle_iMA_Medium, handle_iMA_Slow, m_init_error, start
    SetIndexBuffer(0, MA_Fast_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MA_Medium_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, MA_Slow_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, UPBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, DOWNBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, Inp_UP_Arrow_Code)
    PlotIndexSetInteger(4, PLOT_ARROW, Inp_DOWN_Arrow_Code)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, Inp_UP_Arrow_Shift)
    PlotIndexSetInteger(4, PLOT_ARROW_SHIFT, -Inp_DOWN_Arrow_Shift)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    handle_iMA_Fast = iMA(Symbol(), Period(), Inp_MA_Fast_ma_period, Inp_MA_Fast_ma_shift, Inp_MA_Fast_ma_method, Inp_MA_Fast_applied_price)
    if handle_iMA_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('Fast') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_Medium = iMA(Symbol(), Period(), Inp_MA_Medium_ma_period, Inp_MA_Medium_ma_shift, Inp_MA_Medium_ma_method, Inp_MA_Medium_applied_price)
    if handle_iMA_Medium == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('Medium') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_Slow = iMA(Symbol(), Period(), Inp_MA_Slow_ma_period, Inp_MA_Slow_ma_shift, Inp_MA_Slow_ma_method, Inp_MA_Slow_applied_price)
    if handle_iMA_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('Slow') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    fast = Inp_MA_Fast_ma_period + Inp_MA_Fast_ma_shift
    medium = Inp_MA_Medium_ma_period + Inp_MA_Medium_ma_shift
    slow = Inp_MA_Slow_ma_period + Inp_MA_Slow_ma_shift
    start = (medium if (fast < medium) else fast)
    start = (slow if (start < slow) else start)
    ArrayInitialize(UPBuffer, 0.0)
    ArrayInitialize(DOWNBuffer, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated, m_last_sound, m_prev_bars, m_repetitions, m_text
    if m_init_error:
        return 0
    if rates_total < (start + 1):
        return 0
    values_to_copy = 0
    calculated_fast = BarsCalculated(handle_iMA_Fast)
    if calculated_fast <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, error code %d', calculated_fast, GetLastError())
        return 0
    calculated_medium = BarsCalculated(handle_iMA_Medium)
    if calculated_medium <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Medium) returned %d, error code %d', calculated_medium, GetLastError())
        return 0
    calculated_slow = BarsCalculated(handle_iMA_Slow)
    if calculated_slow <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Slow) returned %d, error code %d', calculated_slow, GetLastError())
        return 0
    if calculated_fast != calculated_medium:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, BarsCalculated(handle_iMA_Medium) returned %d', calculated_fast, calculated_medium)
        return 0
    if calculated_medium != calculated_slow:
        PrintFormat('BarsCalculated(handle_iMA_Medium) returned %d, BarsCalculated(handle_iMA_Slow) returned %d', calculated_medium, calculated_slow)
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
    if not FillArrayFromBuffer(MA_Medium_Buffer, Inp_MA_Fast_ma_shift, handle_iMA_Medium, values_to_copy):
        return 0
    if not FillArrayFromBuffer(MA_Slow_Buffer, Inp_MA_Slow_ma_shift, handle_iMA_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        ArrayInitialize(UPBuffer, 0.0)
        ArrayInitialize(DOWNBuffer, 0.0)
        limit = start
        for i in range(0, limit):
            UPBuffer[i] = 0.0
            DOWNBuffer[i] = 0.0
    for i in range(limit, rates_total):
        if MA_Fast_Buffer[i - 1] < MA_Medium_Buffer[i - 1] and MA_Fast_Buffer[i] > MA_Medium_Buffer[i]:
            UPBuffer[i] = low[i]
        if MA_Fast_Buffer[i - 1] > MA_Medium_Buffer[i - 1] and MA_Fast_Buffer[i] < MA_Medium_Buffer[i]:
            DOWNBuffer[i] = high[i]
    if time[rates_total - 1] > m_prev_bars:
        m_last_sound = 0
        m_prev_bars = time[rates_total - 1]
        m_repetitions = 0
    if m_repetitions >= InpSoundRepetitions:
        return rates_total
    time_current = TimeCurrent()
    if (time_current - m_last_sound) > InpSoundPause:
        i = rates_total - 1
        if MA_Fast_Buffer[i - 1] < MA_Medium_Buffer[i - 1] and MA_Fast_Buffer[i] > MA_Medium_Buffer[i]:
            if InpUseSound:
                PlaySound(InpSoundName)
            m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Three MAs, Trend UP, ' + TimeToString(time[i])
            if InpUseAlert:
                Alert(m_text)
            m_last_sound = time_current
            m_repetitions += 1
            if InpUseMail:
                SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
            if InpUseNotification:
                SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
        else:
            if MA_Fast_Buffer[i - 1] > MA_Medium_Buffer[i - 1] and MA_Fast_Buffer[i] < MA_Medium_Buffer[i]:
                if InpUseSound:
                    PlaySound(InpSoundName)
                m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Three MAs, Trend DOWN, ' + TimeToString(time[i])
                if InpUseAlert:
                    Alert(m_text)
                m_last_sound = time_current
                m_repetitions += 1
                if InpUseMail:
                    SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
                if InpUseNotification:
                    SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Fast)
    if handle_iMA_Medium != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Medium)
    if handle_iMA_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Slow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlertCrossingThreeMAs(_MQL5Indicator):
    name = 'Alert Crossing Three MAs'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_Fast_ma_period': 50,  # MA Fast: averaging period
        'Inp_MA_Fast_ma_shift': 0,  # MA Fast: horizontal shift
        'Inp_MA_Fast_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Fast: smoothing type
        'Inp_MA_Fast_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Fast: type of price
        'Inp_MA_Medium_ma_period': 100,  # MA Medium: averaging period
        'Inp_MA_Medium_ma_shift': 0,  # MA Medium: horizontal shift
        'Inp_MA_Medium_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Medium: smoothing type
        'Inp_MA_Medium_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Medium: type of price
        'Inp_MA_Slow_ma_period': 240,  # MA Slow: averaging period
        'Inp_MA_Slow_ma_shift': 0,  # MA Slow: horizontal shift
        'Inp_MA_Slow_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # MA Slow: smoothing type
        'Inp_MA_Slow_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Slow: type of price
        'Inp_UP_Arrow_Code': 241,  # Arrow 'UP': code (font Wingdings)
        'Inp_UP_Arrow_Shift': 10,  # Arrow 'UP': vertical shift in pixel
        'Inp_DOWN_Arrow_Code': 242,  # Arrow 'DOWN': code (font Wingdings)
        'Inp_DOWN_Arrow_Shift': 10,  # Arrow 'DOWN': vertical shift in pixel
        'InpSoundRepetitions': 3,  # Repetitions
        'InpSoundPause': 3,  # Pause, in seconds
        'InpUseSound': False,  # Use Sound
        'InpUseAlert': True,  # Use Alert
        'InpUseMail': True,  # Use Send mail
        'InpUseNotification': True,  # Use Send notification
    }

