"""Two Stochastic Custom Filling Alert — converted from MQL5: MQL5 Indicators/Two Stochastic Custom Filling Alert/Two Stochastic Custom Filling Alert.mq5

Copyright: Copyright © 2021, Vladimir Karputov; Link: https://www.mql5.com/ru/market/product/43516; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2021, Vladimir Karputov', 'link': 'https://www.mql5.com/ru/market/product/43516', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [8388352], 2: [4678655], 3: [16772332, 15527167]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'STO Fast', 2: 'STO Slow', 3: 'Filling'}, 'levels': [], 'description': [], 'name': 'Two Stochastic Custom Filling Alert', 'source': 'MQL5 Indicators/Two Stochastic Custom Filling Alert/Two Stochastic Custom Filling Alert.mq5', 'folder': 'Two Stochastic Custom Filling Alert', 'inputs': [{'mql': 'Inp_STO_Fast_Kperiod', 'py': 'Inp_STO_Fast_Kperiod', 'param': 'Inp_STO_Fast_Kperiod', 'type': 'int', 'default': 5, 'label': 'Stochastic Fast: K-period (number of bars for calculations)', 'sinput': False}, {'mql': 'Inp_STO_Fast_Dperiod', 'py': 'Inp_STO_Fast_Dperiod', 'param': 'Inp_STO_Fast_Dperiod', 'type': 'int', 'default': 3, 'label': 'Stochastic Fast: D-period (period of first smoothing)', 'sinput': False}, {'mql': 'Inp_STO_Fast_slowing', 'py': 'Inp_STO_Fast_slowing', 'param': 'Inp_STO_Fast_slowing', 'type': 'int', 'default': 3, 'label': 'Stochastic Fast: final smoothing', 'sinput': False}, {'mql': 'Inp_STO_Fast_ma_method', 'py': 'Inp_STO_Fast_ma_method', 'param': 'Inp_STO_Fast_ma_method', 'type': 'int', 'default': 0, 'label': 'Stochastic Fast: type of smoothing', 'sinput': False}, {'mql': 'Inp_STO_Fast_price_field', 'py': 'Inp_STO_Fast_price_field', 'param': 'Inp_STO_Fast_price_field', 'type': 'int', 'default': 0, 'label': 'Stochastic Fast: stochastic calculation method', 'sinput': False}, {'mql': 'Inp_STO_Slow_Kperiod', 'py': 'Inp_STO_Slow_Kperiod', 'param': 'Inp_STO_Slow_Kperiod', 'type': 'int', 'default': 50, 'label': 'Stochastic Slow: K-period (number of bars for calculations)', 'sinput': False}, {'mql': 'Inp_STO_Slow_Dperiod', 'py': 'Inp_STO_Slow_Dperiod', 'param': 'Inp_STO_Slow_Dperiod', 'type': 'int', 'default': 30, 'label': 'Stochastic Slow: D-period (period of first smoothing)', 'sinput': False}, {'mql': 'Inp_STO_Slow_slowing', 'py': 'Inp_STO_Slow_slowing', 'param': 'Inp_STO_Slow_slowing', 'type': 'int', 'default': 30, 'label': 'Stochastic Slow: final smoothing', 'sinput': False}, {'mql': 'Inp_STO_Slow_ma_method', 'py': 'Inp_STO_Slow_ma_method', 'param': 'Inp_STO_Slow_ma_method', 'type': 'int', 'default': 0, 'label': 'Stochastic Slow: type of smoothing', 'sinput': False}, {'mql': 'Inp_STO_Slow_price_field', 'py': 'Inp_STO_Slow_price_field', 'param': 'Inp_STO_Slow_price_field', 'type': 'int', 'default': 0, 'label': 'Stochastic Slow: stochastic calculation method', 'sinput': False}, {'mql': 'Inp_STO_Level1', 'py': 'Inp_STO_Level1', 'param': 'Inp_STO_Level1', 'type': 'double', 'default': 25.0, 'label': 'Value Level #1 (25)', 'sinput': False}, {'mql': 'Inp_STO_Level2', 'py': 'Inp_STO_Level2', 'param': 'Inp_STO_Level2', 'type': 'double', 'default': 75.0, 'label': 'Value Level #2 (75)', 'sinput': False}, {'mql': 'InpSoundName', 'py': 'InpSoundName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Name', 'sinput': False}, {'mql': 'InpSoundRepetitions', 'py': 'InpSoundRepetitions', 'param': 'InpSoundRepetitions', 'type': 'uchar', 'default': 3, 'label': 'Repetitions', 'sinput': False}, {'mql': 'InpSoundPause', 'py': 'InpSoundPause', 'param': 'InpSoundPause', 'type': 'uchar', 'default': 3, 'label': 'Pause, in seconds', 'sinput': False}, {'mql': 'InpUseSound', 'py': 'InpUseSound', 'param': 'InpUseSound', 'type': 'bool', 'default': False, 'label': 'Use Sound', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'bool', 'default': True, 'label': 'Use Alert', 'sinput': False}, {'mql': 'InpUseMail', 'py': 'InpUseMail', 'param': 'InpUseMail', 'type': 'bool', 'default': True, 'label': 'Use Send mail', 'sinput': False}, {'mql': 'InpUseNotification', 'py': 'InpUseNotification', 'param': 'InpUseNotification', 'type': 'bool', 'default': True, 'label': 'Use Send notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_STO_Fast_Kperiod = _input('Inp_STO_Fast_Kperiod', 5)  # Stochastic Fast: K-period (number of bars for calculations)
Inp_STO_Fast_Dperiod = _input('Inp_STO_Fast_Dperiod', 3)  # Stochastic Fast: D-period (period of first smoothing)
Inp_STO_Fast_slowing = _input('Inp_STO_Fast_slowing', 3)  # Stochastic Fast: final smoothing
Inp_STO_Fast_ma_method = _input('Inp_STO_Fast_ma_method', MODE_SMA)  # Stochastic Fast: type of smoothing
Inp_STO_Fast_price_field = _input('Inp_STO_Fast_price_field', STO_LOWHIGH)  # Stochastic Fast: stochastic calculation method
Inp_STO_Slow_Kperiod = _input('Inp_STO_Slow_Kperiod', 50)  # Stochastic Slow: K-period (number of bars for calculations)
Inp_STO_Slow_Dperiod = _input('Inp_STO_Slow_Dperiod', 30)  # Stochastic Slow: D-period (period of first smoothing)
Inp_STO_Slow_slowing = _input('Inp_STO_Slow_slowing', 30)  # Stochastic Slow: final smoothing
Inp_STO_Slow_ma_method = _input('Inp_STO_Slow_ma_method', MODE_SMA)  # Stochastic Slow: type of smoothing
Inp_STO_Slow_price_field = _input('Inp_STO_Slow_price_field', STO_LOWHIGH)  # Stochastic Slow: stochastic calculation method
Inp_STO_Level1 = _input('Inp_STO_Level1', 25.0)  # Value Level #1 (25)
Inp_STO_Level2 = _input('Inp_STO_Level2', 75.0)  # Value Level #2 (75)
InpSoundName = _input('InpSoundName', 'alert.wav')  # Sound Name
InpSoundRepetitions = _input('InpSoundRepetitions', 3)  # Repetitions
InpSoundPause = _input('InpSoundPause', 3)  # Pause, in seconds
InpUseSound = _input('InpUseSound', False)  # Use Sound
InpUseAlert = _input('InpUseAlert', True)  # Use Alert
InpUseMail = _input('InpUseMail', True)  # Use Send mail
InpUseNotification = _input('InpUseNotification', True)  # Use Send notification
StochFastMainBuffer = Arr(0, 0.0)
StochSlowMainBuffer = Arr(0, 0.0)
FillingBuffer1 = Arr(0, 0.0)
FillingBuffer2 = Arr(0, 0.0)
handle_iStochastic_Fast = 0  # variable for storing the handle of the iStochastic indicator
handle_iStochastic_Slow = 0  # variable for storing the handle of the iStochastic indicator
bars_calculated = 0  # we will keep the number of values in the Stochastic Oscillator indicator
m_init_error = False  # error on InInit
m_last_sound = 0  # "0" -> D'1970.01.01 00:00';
m_repetitions = 0
m_text = ''
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';

def OnInit():
    global handle_iStochastic_Fast, handle_iStochastic_Slow, m_init_error
    m_init_error = False
    SetIndexBuffer(0, StochFastMainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, StochSlowMainBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, FillingBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, FillingBuffer2, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_STO_Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_STO_Level2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_STO_Slow_Kperiod + Inp_STO_Slow_Dperiod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_STO_Slow_Kperiod + Inp_STO_Slow_Dperiod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, Inp_STO_Slow_Kperiod + Inp_STO_Slow_Dperiod)
    handle_iStochastic_Fast = iStochastic(Symbol(), Period(), Inp_STO_Fast_Kperiod, Inp_STO_Fast_Dperiod, Inp_STO_Fast_slowing, Inp_STO_Fast_ma_method, Inp_STO_Fast_price_field)
    if handle_iStochastic_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iStochastic ('Fast') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iStochastic_Slow = iStochastic(Symbol(), Period(), Inp_STO_Slow_Kperiod, Inp_STO_Slow_Dperiod, Inp_STO_Slow_slowing, Inp_STO_Slow_ma_method, Inp_STO_Slow_price_field)
    if handle_iStochastic_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iStochastic ('Slow') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated, m_last_sound, m_prev_bars, m_repetitions, m_text
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_fast = BarsCalculated(handle_iStochastic_Fast)
    if calculated_fast <= 0:
        PrintFormat('BarsCalculated(handle_iStochastic_Fast) returned %d, error code %d', calculated_fast, GetLastError())
        return 0
    calculated_slow = BarsCalculated(handle_iStochastic_Fast)
    if calculated_slow <= 0:
        PrintFormat('BarsCalculated(handle_iStochastic_Fast) returned %d, error code %d', calculated_slow, GetLastError())
        return 0
    if calculated_fast != calculated_slow:
        PrintFormat('BarsCalculated(handle_iStochastic_Fast) returned %d, BarsCalculated(handle_iStochastic_Fast) returned %d', calculated_fast, calculated_slow)
        return 0
    calculated = calculated_fast
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArraysFromBuffers(StochFastMainBuffer, handle_iStochastic_Fast, values_to_copy):
        return 0
    if not FillArraysFromBuffers(StochSlowMainBuffer, handle_iStochastic_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = rates_total - values_to_copy
    for i in range(limit, rates_total):
        FillingBuffer1[i] = StochFastMainBuffer[i]
        FillingBuffer2[i] = StochSlowMainBuffer[i]
    if time[rates_total - 1] > m_prev_bars:
        m_last_sound = 0
        m_prev_bars = time[rates_total - 1]
        m_repetitions = 0
    if m_repetitions >= InpSoundRepetitions:
        return rates_total
    time_current = TimeCurrent()
    if (time_current - m_last_sound) > InpSoundPause:
        i = rates_total - 1
        if StochFastMainBuffer[i - 1] < StochSlowMainBuffer[i - 1] and StochFastMainBuffer[i] > StochSlowMainBuffer[i]:
            if InpUseSound:
                PlaySound(InpSoundName)
            m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Two STO, Trend UP, ' + TimeToString(time[i])
            if InpUseAlert:
                Alert(m_text)
            m_last_sound = time_current
            m_repetitions += 1
            if InpUseMail:
                SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
            if InpUseNotification:
                SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
        else:
            if StochFastMainBuffer[i - 1] > StochSlowMainBuffer[i - 1] and StochFastMainBuffer[i] < StochSlowMainBuffer[i]:
                if InpUseSound:
                    PlaySound(InpSoundName)
                m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Two STO, Trend DOWN, ' + TimeToString(time[i])
                if InpUseAlert:
                    Alert(m_text)
                m_last_sound = time_current
                m_repetitions += 1
                if InpUseMail:
                    SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
                if InpUseNotification:
                    SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
    return rates_total

def FillArraysFromBuffers(main_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, MAIN_LINE, 0, amount, main_buffer) < 0:
        PrintFormat('Failed to copy data from the iStochastic indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iStochastic_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iStochastic_Fast)
    if handle_iStochastic_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iStochastic_Slow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TwoStochasticCustomFillingAlert(_MQL5Indicator):
    name = 'Two Stochastic Custom Filling Alert'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_STO_Fast_Kperiod': 5,  # Stochastic Fast: K-period (number of bars for calculations)
        'Inp_STO_Fast_Dperiod': 3,  # Stochastic Fast: D-period (period of first smoothing)
        'Inp_STO_Fast_slowing': 3,  # Stochastic Fast: final smoothing
        'Inp_STO_Fast_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic Fast: type of smoothing
        'Inp_STO_Fast_price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic Fast: stochastic calculation method
        'Inp_STO_Slow_Kperiod': 50,  # Stochastic Slow: K-period (number of bars for calculations)
        'Inp_STO_Slow_Dperiod': 30,  # Stochastic Slow: D-period (period of first smoothing)
        'Inp_STO_Slow_slowing': 30,  # Stochastic Slow: final smoothing
        'Inp_STO_Slow_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic Slow: type of smoothing
        'Inp_STO_Slow_price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic Slow: stochastic calculation method
        'Inp_STO_Level1': 25.0,  # Value Level #1 (25)
        'Inp_STO_Level2': 75.0,  # Value Level #2 (75)
        'InpSoundRepetitions': 3,  # Repetitions
        'InpSoundPause': 3,  # Pause, in seconds
        'InpUseSound': False,  # Use Sound
        'InpUseAlert': True,  # Use Alert
        'InpUseMail': True,  # Use Send mail
        'InpUseNotification': True,  # Use Send notification
    }
    y_range = (0.0, 100.0)

