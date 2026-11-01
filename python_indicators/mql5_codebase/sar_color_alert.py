"""SAR Color Alert — converted from MQL5: MQL5 Indicators/SAR Color Alert/SAR Color Alert.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16748574, 17919]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SAR'}, 'levels': [], 'description': [], 'name': 'SAR Color Alert', 'source': 'MQL5 Indicators/SAR Color Alert/SAR Color Alert.mq5', 'folder': 'SAR Color Alert', 'inputs': [{'mql': 'Inp_SAR_step', 'py': 'Inp_SAR_step', 'param': 'Inp_SAR_step', 'type': 'double', 'default': 0.02, 'label': 'SAR: price increment step - acceleration factor', 'sinput': False}, {'mql': 'Inp_SAR_maximum', 'py': 'Inp_SAR_maximum', 'param': 'Inp_SAR_maximum', 'type': 'double', 'default': 0.2, 'label': 'SAR: maximum value of step', 'sinput': False}, {'mql': 'InpSoundName', 'py': 'InpSoundName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Name', 'sinput': False}, {'mql': 'InpSoundRepetitions', 'py': 'InpSoundRepetitions', 'param': 'InpSoundRepetitions', 'type': 'uchar', 'default': 3, 'label': 'Repetitions', 'sinput': False}, {'mql': 'InpSoundPause', 'py': 'InpSoundPause', 'param': 'InpSoundPause', 'type': 'uchar', 'default': 3, 'label': 'Pause, in seconds', 'sinput': False}, {'mql': 'InpUseSound', 'py': 'InpUseSound', 'param': 'InpUseSound', 'type': 'bool', 'default': False, 'label': 'Use Sound', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'bool', 'default': True, 'label': 'Use Alert', 'sinput': False}, {'mql': 'InpUseMail', 'py': 'InpUseMail', 'param': 'InpUseMail', 'type': 'bool', 'default': True, 'label': 'Use Send mail', 'sinput': False}, {'mql': 'InpUseNotification', 'py': 'InpUseNotification', 'param': 'InpUseNotification', 'type': 'bool', 'default': True, 'label': 'Use Send notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_SAR_step = _input('Inp_SAR_step', 0.02)  # SAR: price increment step - acceleration factor
Inp_SAR_maximum = _input('Inp_SAR_maximum', 0.2)  # SAR: maximum value of step
InpSoundName = _input('InpSoundName', 'alert.wav')  # Sound Name
InpSoundRepetitions = _input('InpSoundRepetitions', 3)  # Repetitions
InpSoundPause = _input('InpSoundPause', 3)  # Pause, in seconds
InpUseSound = _input('InpUseSound', False)  # Use Sound
InpUseAlert = _input('InpUseAlert', True)  # Use Alert
InpUseMail = _input('InpUseMail', True)  # Use Send mail
InpUseNotification = _input('InpUseNotification', True)  # Use Send notification
SARBuffer = Arr(0, 0.0)
SARColors = Arr(0, 0.0)
handle_iSAR = 0  # variable for storing the handle of the iSAR indicator
bars_calculated = 0  # we will keep the number of values in the Parabolic SAR indicator
m_last_sound = 0  # "0" -> D'1970.01.01 00:00';
m_repetitions = 0
m_text = ''
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
m_init_error = False  # error on InInit

def OnInit():
    global handle_iSAR, m_init_error
    SetIndexBuffer(0, SARBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SARColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = StringFormat('SAR Alert(%.2f,%.2f)', Inp_SAR_step, Inp_SAR_maximum)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    handle_iSAR = iSAR(Symbol(), Period(), Inp_SAR_step, Inp_SAR_maximum)
    if handle_iSAR == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iSAR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated, m_last_sound, m_prev_bars, m_repetitions, m_text
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iSAR)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(SARBuffer, handle_iSAR, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        if SARBuffer[i] <= low[i]:
            SARColors[i] = 0.0
        if SARBuffer[i] >= high[i]:
            SARColors[i] = 1.0
    if time[rates_total - 1] > m_prev_bars:
        m_last_sound = 0
        m_prev_bars = time[rates_total - 1]
        m_repetitions = 0
    if m_repetitions >= InpSoundRepetitions:
        return rates_total
    time_current = TimeCurrent()
    if rates_total < 3:
        return rates_total
    if (time_current - m_last_sound) > InpSoundPause:
        i = rates_total - 1
        if SARColors[i - 1] == 1.0 and SARColors[i] == 0.0:
            if InpUseSound:
                PlaySound(InpSoundName)
            m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' SAR, Trend UP, ' + TimeToString(time[i])
            if InpUseAlert:
                Alert(m_text)
            m_last_sound = time_current
            m_repetitions += 1
            if InpUseMail:
                SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
            if InpUseNotification:
                SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
        else:
            if SARColors[i - 1] == 0.0 and SARColors[i] == 1.0:
                if InpUseSound:
                    PlaySound(InpSoundName)
                m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' SAR, Trend DOWN, ' + TimeToString(time[i])
                if InpUseAlert:
                    Alert(m_text)
                m_last_sound = time_current
                m_repetitions += 1
                if InpUseMail:
                    SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
                if InpUseNotification:
                    SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
    return rates_total

def FillArrayFromBuffer(sar_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, sar_buffer) < 0:
        PrintFormat('Failed to copy data from the iSAR indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iSAR != INVALID_HANDLE:
        IndicatorRelease(handle_iSAR)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SARColorAlert(_MQL5Indicator):
    name = 'SAR Color Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_SAR_step': 0.02,  # SAR: price increment step - acceleration factor
        'Inp_SAR_maximum': 0.2,  # SAR: maximum value of step
        'InpSoundRepetitions': 3,  # Repetitions
        'InpSoundPause': 3,  # Pause, in seconds
        'InpUseSound': False,  # Use Sound
        'InpUseAlert': True,  # Use Alert
        'InpUseMail': True,  # Use Send mail
        'InpUseNotification': True,  # Use Send notification
    }

