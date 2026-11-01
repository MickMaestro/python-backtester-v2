"""Elliott Wave Oscillator — converted from MQL5: MQL5 Indicators/Elliott Wave Oscillator/Elliott Wave Oscillator.mq5

Fully Coded By Hossein Nouri
Email : hsn.nouri@gmail.com
Skype : hsn.nouri
Telegram : @hypernova1990
Website : http://www.metatraderprogrammer.ir
MQL5 Profile : https://www.mql5.com/en/users/hsnnouri
 
Feel free to contact me for MQL4/MQL5/Pine coding.
Copyright: Copyright 2016-2021, Hossein Nouri; Link: https://www.mql5.com/en/users/hsnnouri; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016-2021, Hossein Nouri', 'link': 'https://www.mql5.com/en/users/hsnnouri', 'version': '1.20', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 65280, 255, 128], 2: [16748574]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'EWO', 2: 'MA'}, 'levels': [], 'description': ['Fully Coded By Hossein Nouri', 'Email : hsn.nouri@gmail.com', 'Skype : hsn.nouri', 'Telegram : @hypernova1990', 'Website : http://www.metatraderprogrammer.ir', 'MQL5 Profile : https://www.mql5.com/en/users/hsnnouri', ' ', 'Feel free to contact me for MQL4/MQL5/Pine coding.'], 'name': 'Elliott Wave Oscillator', 'source': 'MQL5 Indicators/Elliott Wave Oscillator/Elliott Wave Oscillator.mq5', 'folder': 'Elliott Wave Oscillator', 'inputs': [{'mql': 'DescEWO', 'py': 'DescEWO', 'param': None, 'type': 'string', 'default': '========== EWO ==========', 'label': 'Description', 'sinput': False}, {'mql': 'InpFastMA', 'py': 'InpFastMA', 'param': 'InpFastMA', 'type': 'int', 'default': 5, 'label': 'Fast Period', 'sinput': False}, {'mql': 'InpSlowMA', 'py': 'InpSlowMA', 'param': 'InpSlowMA', 'type': 'int', 'default': 35, 'label': 'Slow Period', 'sinput': False}, {'mql': 'InpPriceSource', 'py': 'InpPriceSource', 'param': 'InpPriceSource', 'type': 'int', 'default': 5, 'label': 'Apply to', 'sinput': False}, {'mql': 'InpSmoothingMethod', 'py': 'InpSmoothingMethod', 'param': 'InpSmoothingMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'DescMA', 'py': 'DescMA', 'param': None, 'type': 'string', 'default': '=========== MA ===========', 'label': 'Description', 'sinput': False}, {'mql': 'InpShowMA', 'py': 'InpShowMA', 'param': 'InpShowMA', 'type': 'bool', 'default': True, 'label': 'Show MA', 'sinput': False}, {'mql': 'InpMaPeriod', 'py': 'InpMaPeriod', 'param': 'InpMaPeriod', 'type': 'int', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'InpMaMethod', 'py': 'InpMaMethod', 'param': 'InpMaMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'DescAlertEvents', 'py': 'DescAlertEvents', 'param': None, 'type': 'string', 'default': '======= Alert Events =======', 'label': 'Description', 'sinput': False}, {'mql': 'InpAlertOnZeroLineCross', 'py': 'InpAlertOnZeroLineCross', 'param': 'InpAlertOnZeroLineCross', 'type': 'bool', 'default': False, 'label': 'Zero Line Cross', 'sinput': False}, {'mql': 'InpAlertOnFallingGrowing', 'py': 'InpAlertOnFallingGrowing', 'param': 'InpAlertOnFallingGrowing', 'type': 'bool', 'default': False, 'label': 'Falling/Growing', 'sinput': False}, {'mql': 'InpAlertOnMACross', 'py': 'InpAlertOnMACross', 'param': 'InpAlertOnMACross', 'type': 'bool', 'default': False, 'label': 'MA Cross', 'sinput': False}, {'mql': 'DescAlertSettings', 'py': 'DescAlertSettings', 'param': None, 'type': 'string', 'default': '======= Alert Settings =======', 'label': 'Description', 'sinput': False}, {'mql': 'InpAlertShowPopup', 'py': 'InpAlertShowPopup', 'param': 'InpAlertShowPopup', 'type': 'bool', 'default': True, 'label': 'Show Pop-up', 'sinput': False}, {'mql': 'InpAlertSendEmail', 'py': 'InpAlertSendEmail', 'param': 'InpAlertSendEmail', 'type': 'bool', 'default': False, 'label': 'Send Email', 'sinput': False}, {'mql': 'InpAlertSendNotification', 'py': 'InpAlertSendNotification', 'param': 'InpAlertSendNotification', 'type': 'bool', 'default': False, 'label': 'Send Notification', 'sinput': False}, {'mql': 'InpAlertPlaySound', 'py': 'InpAlertPlaySound', 'param': 'InpAlertPlaySound', 'type': 'bool', 'default': False, 'label': 'Play Sound', 'sinput': False}, {'mql': 'InpAlertSoundFile', 'py': 'InpAlertSoundFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound File', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
DescEWO = _input('DescEWO', '========== EWO ==========')  # Description
InpFastMA = _input('InpFastMA', 5)  # Fast Period
InpSlowMA = _input('InpSlowMA', 35)  # Slow Period
InpPriceSource = _input('InpPriceSource', PRICE_MEDIAN)  # Apply to
InpSmoothingMethod = _input('InpSmoothingMethod', MODE_SMA)  # Method
DescMA = _input('DescMA', '=========== MA ===========')  # Description
InpShowMA = _input('InpShowMA', True)  # Show MA
InpMaPeriod = _input('InpMaPeriod', 5)  # Period
InpMaMethod = _input('InpMaMethod', MODE_SMA)  # Method
DescAlertEvents = _input('DescAlertEvents', '======= Alert Events =======')  # Description
InpAlertOnZeroLineCross = _input('InpAlertOnZeroLineCross', False)  # Zero Line Cross
InpAlertOnFallingGrowing = _input('InpAlertOnFallingGrowing', False)  # Falling/Growing
InpAlertOnMACross = _input('InpAlertOnMACross', False)  # MA Cross
DescAlertSettings = _input('DescAlertSettings', '======= Alert Settings =======')  # Description
InpAlertShowPopup = _input('InpAlertShowPopup', True)  # Show Pop-up
InpAlertSendEmail = _input('InpAlertSendEmail', False)  # Send Email
InpAlertSendNotification = _input('InpAlertSendNotification', False)  # Send Notification
InpAlertPlaySound = _input('InpAlertPlaySound', False)  # Play Sound
InpAlertSoundFile = _input('InpAlertSoundFile', 'alert.wav')  # Sound File
EWOBuffer = Arr(0, 0.0)
EWOColors = Arr(0, 0.0)
MABuffer = Arr(0, 0.0)
FastMABuffer = Arr(0, 0.0)
SlowMABuffer = Arr(0, 0.0)
FastMaHandle = 0
SlowMaHandle = 0
Begin = 0
WeightedSum = 0

def OnInit():
    global Begin, FastMaHandle, SlowMaHandle
    Begin = MathMax(InpFastMA, InpSlowMA)
    SetIndexBuffer(0, EWOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, EWOColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MABuffer, INDICATOR_DATA)
    SetIndexBuffer(3, FastMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, SlowMABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Begin + InpMaPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EWO(' + _str(InpFastMA) + ',' + _str(InpSlowMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'EWO(' + _str(InpFastMA) + ',' + _str(InpSlowMA) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'MA(' + _str(InpMaPeriod) + ')')
    FastMaHandle = iMA(Symbol(), Period(), InpFastMA, 0, InpSmoothingMethod, InpPriceSource)
    SlowMaHandle = iMA(Symbol(), Period(), InpSlowMA, 0, InpSmoothingMethod, InpPriceSource)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (MathMax(InpSlowMA, InpFastMA) + InpMaPeriod):
        return 0
    calculated = BarsCalculated(FastMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(SlowMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(FastMaHandle, 0, 0, to_copy, FastMABuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
    if CopyBuffer(SlowMaHandle, 0, 0, to_copy, SlowMABuffer) <= 0:
        Print('Getting slow SMA is failed! Error', GetLastError())
    limit = 0
    if prev_calculated == 0:
        limit = MathMax(InpSlowMA, InpFastMA)
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        CalculateValue(i)
    CalculateMA(rates_total, prev_calculated, limit)
    if IsNewBar():
        if InpAlertOnZeroLineCross:
            if EWOBuffer[rates_total - 3] <= 0 and EWOBuffer[rates_total - 2] > 0:
                TriggerAlert('EWO crossed above zero line.')
            elif EWOBuffer[rates_total - 3] >= 0 and EWOBuffer[rates_total - 2] < 0:
                TriggerAlert('EWO crossed below zero line.')
        if InpAlertOnFallingGrowing:
            if EWOBuffer[rates_total - 2] > EWOBuffer[rates_total - 3] and (EWOBuffer[rates_total - 3] < EWOBuffer[rates_total - 4] or (EWOBuffer[rates_total - 3] == EWOBuffer[rates_total - 4] and EWOBuffer[rates_total - 4] < EWOBuffer[rates_total - 5])):
                TriggerAlert('EWO started growing.')
            elif EWOBuffer[rates_total - 2] < EWOBuffer[rates_total - 3] and (EWOBuffer[rates_total - 3] > EWOBuffer[rates_total - 4] or (EWOBuffer[rates_total - 3] == EWOBuffer[rates_total - 4] and EWOBuffer[rates_total - 4] > EWOBuffer[rates_total - 5])):
                TriggerAlert('EWO started falling.')
        if InpAlertOnMACross:
            if EWOBuffer[rates_total - 3] <= MABuffer[rates_total - 3] and EWOBuffer[rates_total - 2] > MABuffer[rates_total - 2]:
                TriggerAlert('EWO crossed above MA line.')
            elif EWOBuffer[rates_total - 3] >= MABuffer[rates_total - 3] and EWOBuffer[rates_total - 2] < MABuffer[rates_total - 2]:
                TriggerAlert('EWO crossed below MA line.')
    return rates_total

def CalculateValue(index):
    EWOBuffer[index] = FastMABuffer[index] - SlowMABuffer[index]
    if EWOBuffer[index] == EWOBuffer[index - 1]:
        EWOColors[index] = EWOColors[index - 1]
        return
    if EWOBuffer[index] > 0:
        if EWOBuffer[index] > EWOBuffer[index - 1]:
            EWOColors[index] = 1.0
            return
        if EWOBuffer[index] < EWOBuffer[index - 1]:
            EWOColors[index] = 0.0
            return
    if EWOBuffer[index] < 0:
        if EWOBuffer[index] > EWOBuffer[index - 1]:
            EWOColors[index] = 3.0
            return
        if EWOBuffer[index] < EWOBuffer[index - 1]:
            EWOColors[index] = 2.0
            return

def CalculateMA(rates_total, prev_calculated, limit):
    if InpShowMA == True:
        if InpMaMethod == MODE_SMA:
            SimpleMAOnBuffer(rates_total, prev_calculated, Begin + InpMaPeriod, InpMaPeriod, EWOBuffer, MABuffer)
            return
        if InpMaMethod == MODE_LWMA:
            LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, Begin + InpMaPeriod, InpMaPeriod, EWOBuffer, MABuffer, _GlobRef(globals(), 'WeightedSum'))
            return
        if InpMaMethod == MODE_EMA:
            ExponentialMAOnBuffer(rates_total, prev_calculated, Begin + InpMaPeriod, InpMaPeriod, EWOBuffer, MABuffer)
            return
        if InpMaMethod == MODE_SMMA:
            SmoothedMAOnBuffer(rates_total, prev_calculated, Begin + InpMaPeriod, InpMaPeriod, EWOBuffer, MABuffer)
            return
    ArrayInitialize(MABuffer, EMPTY_VALUE)

def IsNewBar():
    global _s_IsNewBar_CountedBars, _s_IsNewBar_PrevClose, _s_IsNewBar_PrevTime
    Rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(Rates, True)
    Copied = CopyRates(Symbol(), Period(), 0, 2, Rates)
    if Copied > 0:
        if _s_IsNewBar_CountedBars is _UNSET:
            _s_IsNewBar_CountedBars = Bars(Symbol(), PERIOD_CURRENT)
        if _s_IsNewBar_PrevClose is _UNSET:
            _s_IsNewBar_PrevClose = Rates[1].close
        if _s_IsNewBar_PrevTime is _UNSET:
            _s_IsNewBar_PrevTime = Rates[1].time
        if (Bars(Symbol(), PERIOD_CURRENT) != _s_IsNewBar_CountedBars or Rates[1].close != _s_IsNewBar_PrevClose) or _s_IsNewBar_PrevTime != Rates[1].time:
            _s_IsNewBar_CountedBars = Bars(Symbol(), PERIOD_CURRENT)
            _s_IsNewBar_PrevClose = Rates[1].close
            _s_IsNewBar_PrevTime = Rates[1].time
            return True
    return False

def GetTFName():
    Result = Arr(0, "")
    if StringSplit(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 95, Result) > 0:
        return Result[1]
    else:
        return ''

def TriggerAlert(_OP):
    message = Box('')
    StringConcatenate(message, Symbol(), '(', GetTFName(), ') ', _OP)
    if InpAlertShowPopup:
        Alert(message.v)
    if InpAlertSendEmail:
        if not SendMail('Elliott Wave Oscillator', message.v):
            Print('Send email failed with error #', GetLastError())
    if InpAlertPlaySound:
        PlaySound(InpAlertSoundFile)
    if InpAlertSendNotification:
        if not SendNotification(message.v):
            Print('Send notification failed with error #', GetLastError())

# ---- static local variables
_s_IsNewBar_CountedBars = _UNSET
_s_IsNewBar_PrevClose = _UNSET
_s_IsNewBar_PrevTime = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ElliottWaveOscillator(_MQL5Indicator):
    name = 'Elliott Wave Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastMA': 5,  # Fast Period
        'InpSlowMA': 35,  # Slow Period
        'InpPriceSource': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Apply to
        'InpSmoothingMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpShowMA': True,  # Show MA
        'InpMaPeriod': 5,  # Period
        'InpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAlertOnZeroLineCross': False,  # Zero Line Cross
        'InpAlertOnFallingGrowing': False,  # Falling/Growing
        'InpAlertOnMACross': False,  # MA Cross
        'InpAlertShowPopup': True,  # Show Pop-up
        'InpAlertSendEmail': False,  # Send Email
        'InpAlertSendNotification': False,  # Send Notification
        'InpAlertPlaySound': False,  # Play Sound
    }

