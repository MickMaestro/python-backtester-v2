"""Super trend - simple Alert — converted from MQL5: MQL5 Indicators/Super trend - simple Alert/Super trend - simple Alert.mq5

Super trend - \\"CCI based\\" - simple
Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 255, 16711680]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Super trend'}, 'levels': [], 'description': ['Super trend - \\"CCI based\\" - simple'], 'name': 'Super trend - simple Alert', 'source': 'MQL5 Indicators/Super trend - simple Alert/Super trend - simple Alert.mq5', 'folder': 'Super trend - simple Alert', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpAtrDevPeriod', 'py': 'inpAtrDevPeriod', 'param': 'inpAtrDevPeriod', 'type': 'int', 'default': 5, 'label': 'Atr / standard deviation period', 'sinput': False}, {'mql': 'inpUseWhat', 'py': 'inpUseWhat', 'param': 'inpUseWhat', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}, {'mql': 'InpSoundName', 'py': 'InpSoundName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Name', 'sinput': False}, {'mql': 'InpSoundRepetitions', 'py': 'InpSoundRepetitions', 'param': 'InpSoundRepetitions', 'type': 'uchar', 'default': 3, 'label': 'Repetitions', 'sinput': False}, {'mql': 'InpSoundPause', 'py': 'InpSoundPause', 'param': 'InpSoundPause', 'type': 'uchar', 'default': 3, 'label': 'Pause, in seconds', 'sinput': False}, {'mql': 'InpUseSound', 'py': 'InpUseSound', 'param': 'InpUseSound', 'type': 'bool', 'default': False, 'label': 'Use Sound', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'bool', 'default': True, 'label': 'Use Alert', 'sinput': False}, {'mql': 'InpUseMail', 'py': 'InpUseMail', 'param': 'InpUseMail', 'type': 'bool', 'default': True, 'label': 'Use Send mail', 'sinput': False}, {'mql': 'InpUseNotification', 'py': 'InpUseNotification', 'param': 'InpUseNotification', 'type': 'bool', 'default': True, 'label': 'Use Send notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enUseWhat
use_atr = 0
use_dev = 1
_enum('enUseWhat', {0: 'use_atr', 1: 'use_dev'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpAtrDevPeriod = _input('inpAtrDevPeriod', 5)  # Atr / standard deviation period
inpUseWhat = _input('inpUseWhat', use_atr)  # Calculation method
InpSoundName = _input('InpSoundName', 'alert.wav')  # Sound Name
InpSoundRepetitions = _input('InpSoundRepetitions', 3)  # Repetitions
InpSoundPause = _input('InpSoundPause', 3)  # Pause, in seconds
InpUseSound = _input('InpUseSound', False)  # Use Sound
InpUseAlert = _input('InpUseAlert', True)  # Use Alert
InpUseMail = _input('InpUseMail', True)  # Use Send mail
InpUseNotification = _input('InpUseNotification', True)  # Use Send notification
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
trend = Arr(0, 0.0)
ade = Arr(0, 0.0)
ma = Arr(0, 0.0)
price = Arr(0, 0.0)
ª_adHandle = 0
ª_maHandle = 0
ª_prHandle = 0
m_last_sound = 0  # "0" -> D'1970.01.01 00:00';
m_repetitions = 0
m_text = ''
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';

def OnInit():
    global ª_adHandle, ª_maHandle, ª_prHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ade, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, price, INDICATOR_CALCULATIONS)
    if inpUseWhat == use_atr:
        ª_adHandle = iATR(Symbol(), 0, inpAtrDevPeriod)
        if not _checkHandle(ª_adHandle, 'ATR'):
            return INIT_FAILED
    else:
        ª_adHandle = iStdDev(Symbol(), 0, inpAtrDevPeriod, 0, MODE_SMA, inpPrice)
        if not _checkHandle(ª_adHandle, 'Standard deviation'):
            return INIT_FAILED
    ª_maHandle = iMA(Symbol(), 0, inpPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    ª_prHandle = iMA(Symbol(), 0, 1, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_prHandle, 'Prices'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Super trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_last_sound, m_prev_bars, m_repetitions, m_text
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_adHandle, 0, 0, _copyCount, ade) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, ma) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_prHandle, 0, 0, _copyCount, price) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        trend[i] = (1 if (price[i] > ma[i]) else -1 if (price[i] < ma[i]) else trend[i - 1] if (i > 0) else 0)
        val[i] = ((MathMax(low[i] - ade[i], val[i - 1]) if (trend[i] == 1) else MathMin(high[i] + ade[i], val[i - 1])) if (i > 0) else close[i])
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    if time[rates_total - 1] > m_prev_bars:
        m_last_sound = 0
        m_prev_bars = time[rates_total - 1]
        m_repetitions = 0
    if m_repetitions >= InpSoundRepetitions:
        return rates_total
    time_current = TimeCurrent()
    if (time_current - m_last_sound) > InpSoundPause:
        k = rates_total - 1
        if valc[k - 1] != 1.0 and valc[k] == 1.0:
            if InpUseSound:
                PlaySound(InpSoundName)
            m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' RSI adaptive EMA, Trend UP, ' + TimeToString(time[k])
            if InpUseAlert:
                Alert(m_text)
            m_last_sound = time_current
            m_repetitions += 1
            if InpUseMail:
                SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
            if InpUseNotification:
                SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
        else:
            if valc[k - 1] != 2.0 and valc[k] == 2.0:
                if InpUseSound:
                    PlaySound(InpSoundName)
                m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Three MAs, Trend DOWN, ' + TimeToString(time[k])
                if InpUseAlert:
                    Alert(m_text)
                m_last_sound = time_current
                m_repetitions += 1
                if InpUseMail:
                    SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
                if InpUseNotification:
                    SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperTrendSimpleAlert(_MQL5Indicator):
    name = 'Super trend - simple Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 50,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpAtrDevPeriod': 5,  # Atr / standard deviation period
        'inpUseWhat': _Choice({0: 'Use ATR for calculation', 1: 'Use standard deviation for calculation'}, default=0),  # Calculation method
        'InpSoundRepetitions': 3,  # Repetitions
        'InpSoundPause': 3,  # Pause, in seconds
        'InpUseSound': False,  # Use Sound
        'InpUseAlert': True,  # Use Alert
        'InpUseMail': True,  # Use Send mail
        'InpUseNotification': True,  # Use Send notification
    }

