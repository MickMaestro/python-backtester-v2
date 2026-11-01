"""Half Trend New Alert — converted from MQL5: MQL5 Indicators/Half Trend New Alert/Half Trend New Alert.mq5

Copyright: Copyright © 2021-2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2021-2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [17919, 16760576], 2: [16760576], 3: [17919]}, 'widths': {1: 3, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Line', 2: 'Up', 3: 'Down'}, 'levels': [], 'description': [], 'name': 'Half Trend New Alert', 'source': 'MQL5 Indicators/Half Trend New Alert/Half Trend New Alert.mq5', 'folder': 'Half Trend New Alert', 'inputs': [{'mql': 'InpAmplitude', 'py': 'InpAmplitude', 'param': 'InpAmplitude', 'type': 'int', 'default': 5, 'label': 'Amplitude', 'sinput': False}, {'mql': 'InpCodeUpArrow', 'py': 'InpCodeUpArrow', 'param': 'InpCodeUpArrow', 'type': 'uchar', 'default': 233, 'label': "Arrow code for 'UpArrow' (font Wingdings)", 'sinput': False}, {'mql': 'InpCodeDnArrow', 'py': 'InpCodeDnArrow', 'param': 'InpCodeDnArrow', 'type': 'uchar', 'default': 234, 'label': "Arrow code for 'DnArrow' (font Wingdings)", 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 10, 'label': 'Vertical shift of arrows in pixel', 'sinput': False}, {'mql': 'InpSoundName', 'py': 'InpSoundName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Name', 'sinput': False}, {'mql': 'InpSoundRepetitions', 'py': 'InpSoundRepetitions', 'param': 'InpSoundRepetitions', 'type': 'uchar', 'default': 3, 'label': 'Repetitions', 'sinput': False}, {'mql': 'InpSoundPause', 'py': 'InpSoundPause', 'param': 'InpSoundPause', 'type': 'uchar', 'default': 3, 'label': 'Pause, in seconds', 'sinput': False}, {'mql': 'InpUseSound', 'py': 'InpUseSound', 'param': 'InpUseSound', 'type': 'bool', 'default': False, 'label': 'Use Sound', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'bool', 'default': True, 'label': 'Use Alert', 'sinput': False}, {'mql': 'InpUseMail', 'py': 'InpUseMail', 'param': 'InpUseMail', 'type': 'bool', 'default': True, 'label': 'Use Send mail', 'sinput': False}, {'mql': 'InpUseNotification', 'py': 'InpUseNotification', 'param': 'InpUseNotification', 'type': 'bool', 'default': True, 'label': 'Use Send notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAmplitude = _input('InpAmplitude', 5)  # Amplitude
InpCodeUpArrow = _input('InpCodeUpArrow', 233)  # Arrow code for 'UpArrow' (font Wingdings)
InpCodeDnArrow = _input('InpCodeDnArrow', 234)  # Arrow code for 'DnArrow' (font Wingdings)
InpShift = _input('InpShift', 10)  # Vertical shift of arrows in pixel
InpSoundName = _input('InpSoundName', 'alert.wav')  # Sound Name
InpSoundRepetitions = _input('InpSoundRepetitions', 3)  # Repetitions
InpSoundPause = _input('InpSoundPause', 3)  # Pause, in seconds
InpUseSound = _input('InpUseSound', False)  # Use Sound
InpUseAlert = _input('InpUseAlert', True)  # Use Alert
InpUseMail = _input('InpUseMail', True)  # Use Send mail
InpUseNotification = _input('InpUseNotification', True)  # Use Send notification
LineBuffer = Arr(0, 0.0)
LineColors = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DownBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
MA_PRICE_HIGH_Buffer = Arr(0, 0.0)
MA_PRICE_LOW_Buffer = Arr(0, 0.0)
handle_iMA_PRICE_HIGH = 0  # variable for storing the handle of the iMA indicator
handle_iMA_PRICE_LOW = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0
m_start_bar = 0  # start bar
m_init_error = False  # error on InInit
m_last_sound = 0  # "0" -> D'1970.01.01 00:00';
m_repetitions = 0
m_text = ''
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';

def OnInit():
    global handle_iMA_PRICE_HIGH, handle_iMA_PRICE_LOW, m_init_error, m_start_bar
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LineColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DownBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, MA_PRICE_HIGH_Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, MA_PRICE_LOW_Buffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, InpCodeUpArrow)
    PlotIndexSetInteger(2, PLOT_ARROW, InpCodeDnArrow)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, InpShift)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, -InpShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    handle_iMA_PRICE_HIGH = iMA(Symbol(), Period(), InpAmplitude, 0, MODE_SMA, PRICE_HIGH)
    if handle_iMA_PRICE_HIGH == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA ('High') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_PRICE_LOW = iMA(Symbol(), Period(), InpAmplitude, 0, MODE_SMA, PRICE_LOW)
    if handle_iMA_PRICE_LOW == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA ('Low') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    m_start_bar = (InpAmplitude if (InpAmplitude > m_start_bar) else m_start_bar)
    m_start_bar += 1
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated, m_last_sound, m_prev_bars, m_repetitions, m_text
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_ma_high = BarsCalculated(handle_iMA_PRICE_HIGH)
    if calculated_ma_high <= 0:
        PrintFormat('BarsCalculated(handle_iMA_PRICE_HIGH) returned %d, error code %d', calculated_ma_high, GetLastError())
        return 0
    calculated_ma_low = BarsCalculated(handle_iMA_PRICE_LOW)
    if calculated_ma_low <= 0:
        PrintFormat('BarsCalculated(handle_iMA_PRICE_LOW) returned %d, error code %d', calculated_ma_low, GetLastError())
        return 0
    if calculated_ma_high != calculated_ma_low:
        PrintFormat('BarsCalculated(handle_iMA_PRICE_HIGH) returned %d, BarsCalculated(handle_iMA_PRICE_LOW) returned %d', calculated_ma_high, calculated_ma_low)
        return 0
    calculated = calculated_ma_high
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer_1(MA_PRICE_HIGH_Buffer, 0, handle_iMA_PRICE_HIGH, values_to_copy):
        return 0
    if not FillArrayFromBuffer_1(MA_PRICE_LOW_Buffer, 0, handle_iMA_PRICE_LOW, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = m_start_bar
        for i in range(0, limit):
            LineBuffer[i] = high[i]
            LineColors[i] = 0.0
            UpBuffer[i] = 0.0
            DownBuffer[i] = 0.0
            HighestBuffer[i] = high[i]
            LowestBuffer[i] = low[i]
        highest = high[ArrayMaximum(high, limit - InpAmplitude + 1, InpAmplitude)]
        lowest = low[ArrayMinimum(low, limit - InpAmplitude + 1, InpAmplitude)]
        HighestBuffer[limit] = highest
        LowestBuffer[limit] = lowest
    for i in range(limit, rates_total):
        highest = high[ArrayMaximum(high, i - InpAmplitude + 1, InpAmplitude)]
        lowest = low[ArrayMinimum(low, i - InpAmplitude + 1, InpAmplitude)]
        HighestBuffer[i] = highest
        LowestBuffer[i] = lowest
        UpBuffer[i] = 0.0
        DownBuffer[i] = 0.0
        if (MA_PRICE_HIGH_Buffer[i] < LineBuffer[i - 1] and MA_PRICE_LOW_Buffer[i] < LineBuffer[i - 1]) and HighestBuffer[i] < LineBuffer[i - 1]:
            LineBuffer[i] = HighestBuffer[i]
            LineColors[i] = LineColors[i - 1]
            if LineBuffer[i] < LineBuffer[i - 1]:
                LineColors[i] = 0.0
            if LineBuffer[i] > LineBuffer[i - 1]:
                LineColors[i] = 1.0
            if LineColors[i - 1] == 0.0 and LineColors[i] == 1.0:
                UpBuffer[i] = LineBuffer[i - 1]
            if LineColors[i - 1] == 1.0 and LineColors[i] == 0.0:
                DownBuffer[i] = LineBuffer[i - 1]
            continue
        if (MA_PRICE_HIGH_Buffer[i] > LineBuffer[i - 1] and MA_PRICE_LOW_Buffer[i] > LineBuffer[i - 1]) and LowestBuffer[i] > LineBuffer[i - 1]:
            LineBuffer[i] = LowestBuffer[i]
            LineColors[i] = LineColors[i - 1]
            if LineBuffer[i] < LineBuffer[i - 1]:
                LineColors[i] = 0.0
            if LineBuffer[i] > LineBuffer[i - 1]:
                LineColors[i] = 1.0
            if LineColors[i - 1] == 0.0 and LineColors[i] == 1.0:
                UpBuffer[i] = LineBuffer[i - 1]
            if LineColors[i - 1] == 1.0 and LineColors[i] == 0.0:
                DownBuffer[i] = LineBuffer[i - 1]
            continue
        LineBuffer[i] = LineBuffer[i - 1]
        LineColors[i] = LineColors[i - 1]
        continue
    if time[rates_total - 1] > m_prev_bars:
        m_last_sound = 0
        m_prev_bars = time[rates_total - 1]
        m_repetitions = 0
    if m_repetitions >= InpSoundRepetitions:
        return rates_total
    time_current = TimeCurrent()
    if (time_current - m_last_sound) > InpSoundPause:
        i = rates_total - 1
        if UpBuffer[i] != 0.0:
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
            if DownBuffer[i] != 0.0:
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

def FillArrayFromBuffer_1(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBuffer_2(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iATR indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA_PRICE_HIGH != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_PRICE_HIGH)
    if handle_iMA_PRICE_LOW != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_PRICE_LOW)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HalfTrendNewAlert(_MQL5Indicator):
    name = 'Half Trend New Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAmplitude': 5,  # Amplitude
        'InpCodeUpArrow': 233,  # Arrow code for 'UpArrow' (font Wingdings)
        'InpCodeDnArrow': 234,  # Arrow code for 'DnArrow' (font Wingdings)
        'InpShift': 10,  # Vertical shift of arrows in pixel
        'InpSoundRepetitions': 3,  # Repetitions
        'InpSoundPause': 3,  # Pause, in seconds
        'InpUseSound': False,  # Use Sound
        'InpUseAlert': True,  # Use Alert
        'InpUseMail': True,  # Use Send mail
        'InpUseNotification': True,  # Use Send notification
    }

