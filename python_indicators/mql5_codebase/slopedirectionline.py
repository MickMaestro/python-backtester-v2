"""slopedirectionline — converted from MQL5: MQL5 Indicators/Slope Direction Line/slopedirectionline.mq5

Copyright: avoitenko; Link: https://login.mql5.com/en/users/avoitenko; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'avoitenko', 'link': 'https://login.mql5.com/en/users/avoitenko', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SDL'}, 'levels': [], 'description': [], 'name': 'slopedirectionline', 'source': 'MQL5 Indicators/Slope Direction Line/slopedirectionline.mq5', 'folder': 'Slope Direction Line', 'inputs': [{'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'ushort', 'default': 80, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 3, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'short', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpAlert', 'py': 'InpAlert', 'param': 'InpAlert', 'type': 'bool', 'default': True, 'label': 'Alert', 'sinput': False}, {'mql': 'InpMail', 'py': 'InpMail', 'param': 'InpMail', 'type': 'bool', 'default': True, 'label': 'Mail', 'sinput': False}, {'mql': 'InpSound', 'py': 'InpSound', 'param': 'InpSound', 'type': 'bool', 'default': True, 'label': 'Sound', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpMAPeriod = _input('InpMAPeriod', 80)  # Period
InpMAMethod = _input('InpMAMethod', MODE_LWMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Apply to
InpShift = _input('InpShift', 0)  # Shift
InpAlert = _input('InpAlert', True)  # Alert
InpMail = _input('InpMail', True)  # Mail
InpSound = _input('InpSound', True)  # Sound
MABuffer = Arr(0, 0.0)
MAColorBuffer = Arr(0, 0.0)
vect = Arr(0, 0.0)
wma1 = Arr(0, 0.0)
wma2 = Arr(0, 0.0)
ma1_handle = 0
ma2_handle = 0
new_period = 0
new_period_sqrt = 0
time_alert = 0
w = 0
ind_name = ""

def OnInit():
    global ind_name, ma1_handle, ma2_handle, new_period, new_period_sqrt
    new_period_sqrt = _int(fmax(MathSqrt(InpMAPeriod), 1))
    new_period = fmax(_idiv(InpMAPeriod, 2), 1)
    ma1_handle = iMA(None, 0, fmax(InpMAPeriod, 2), 0, InpMAMethod, InpAppliedPrice)
    ma2_handle = iMA(None, 0, new_period, 0, InpMAMethod, InpAppliedPrice)
    if ma1_handle == INVALID_HANDLE or ma2_handle == INVALID_HANDLE:
        Print('Error creating the indicator iMA')
        return -1
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vect, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, wma1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, wma2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(MABuffer, True)
    ArraySetAsSeries(MAColorBuffer, True)
    ArraySetAsSeries(vect, True)
    ArraySetAsSeries(wma1, True)
    ArraySetAsSeries(wma2, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod + new_period_sqrt + 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(0, PLOT_LABEL, StringFormat('SDL(%u)', InpMAPeriod))
    ind_name = StringFormat('Slope Direction Line (%u)', InpMAPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, ind_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global time_alert
    ArraySetAsSeries(time, True)
    if rates_total < (InpMAPeriod + 1):
        return 0
    limit = 0
    if prev_calculated < 0 or prev_calculated > rates_total:
        return 0
    if prev_calculated == 0:
        time_alert = time[0]
        limit = rates_total - InpMAPeriod - 1
        ArrayInitialize(MABuffer, 0)
        ArrayInitialize(MAColorBuffer, 0)
        ArrayInitialize(wma1, 0)
        ArrayInitialize(wma2, 0)
        ArrayInitialize(vect, 0)
    else:
        limit = rates_total - prev_calculated
    if CopyBuffer(ma1_handle, 0, 0, limit + 1, wma1) != (limit + 1):
        return 0
    if CopyBuffer(ma2_handle, 0, 0, limit + 1, wma2) != (limit + 1):
        return 0
    for i in range(limit, 0 - 1, -1):
        vect[i] = (2 * wma2[i]) - wma1[i]
    _sw1 = InpMAMethod
    if _sw1 == MODE_SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, new_period_sqrt, vect, MABuffer)
    elif _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, new_period_sqrt, vect, MABuffer)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, new_period_sqrt, vect, MABuffer)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, new_period_sqrt, vect, MABuffer, _GlobRef(globals(), 'w'))
    for i in range(limit, 0 - 1, -1):
        MAColorBuffer[i] = MAColorBuffer[i + 1]
        if MABuffer[i] > MABuffer[i + 1]:
            MAColorBuffer[i] = 0.0
        if MABuffer[i] < MABuffer[i + 1]:
            MAColorBuffer[i] = 1.0
    if time_alert != time[0]:
        tick = MqlTick()
        if not SymbolInfoTick(Symbol(), tick):
            return 0
        if MAColorBuffer[2] == 0 and MAColorBuffer[1] == 1:
            mask = StringFormat('%%.%df', Digits())
            msg = StringFormat('%s %s %s Signal SELL at ' + mask, TimeToString(tick.time, TIME_DATE | TIME_SECONDS), Symbol(), PeriodToString(), tick.bid)
            if InpAlert:
                Alert(msg)
            if InpMail:
                SendMail(ind_name, msg)
            if InpSound:
                PlaySound('alert.wav')
        if MAColorBuffer[2] == 1 and MAColorBuffer[1] == 0:
            mask = StringFormat('%%.%df', Digits())
            msg = StringFormat('%s %s %s Signal BUY at ' + mask, TimeToString(tick.time, TIME_DATE | TIME_SECONDS), Symbol(), PeriodToString(), tick.ask)
            if InpAlert:
                Alert(msg)
            if InpMail:
                SendMail(ind_name, msg)
            if InpSound:
                PlaySound('alert.wav')
        time_alert = time[0]
    return rates_total

def PeriodToString(period=PERIOD_CURRENT):
    if period == PERIOD_CURRENT:
        period = Period()
    str_ = EnumToString(period, 'ENUM_TIMEFRAMES')
    if StringLen(str_) > 7:
        return StringSubstr(str_, 7)
    return ''


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Slopedirectionline(_MQL5Indicator):
    name = 'slopedirectionline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriod': 80,  # Period
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'InpShift': 0,  # Shift
        'InpAlert': True,  # Alert
        'InpMail': True,  # Mail
        'InpSound': True,  # Sound
    }

