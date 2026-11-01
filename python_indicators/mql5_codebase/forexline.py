"""forexline — converted from MQL5: MQL5 Indicators/ForexLine/forexline.mq5

ForexLine is the indicator for the MT5, base on ForexLine indicator on MT4.
ForexLine indicator provides signals for trade,
white line (sell signal) and the blue line (buy signal).
Copyright: Copyright 2016,  3rjfx ~ 24/01/2016; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016,  3rjfx ~ 24/01/2016', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 6}, 'types': {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0}, 'colors': {}, 'widths': {5: 3, 6: 3}, 'styles': {5: 0, 6: 0}, 'labels': {5: 'Rice Above: ', 6: 'Down Below: '}, 'levels': [], 'description': ['ForexLine is the indicator for the MT5, base on ForexLine indicator on MT4.', 'ForexLine indicator provides signals for trade,', 'white line (sell signal) and the blue line (buy signal).'], 'name': 'forexline', 'source': 'MQL5 Indicators/ForexLine/forexline.mq5', 'folder': 'ForexLine', 'inputs': [{'mql': 'SoundAlerts', 'py': 'SoundAlerts', 'param': 'SoundAlerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'MsgAlerts', 'py': 'MsgAlerts', 'param': 'MsgAlerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'eMailAlerts', 'py': 'eMailAlerts', 'param': 'eMailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SoundAlertFile', 'py': 'SoundAlertFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': '', 'sinput': False}, {'mql': 'ForexLineColor1', 'py': 'ForexLineColor1', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Line Up', 'sinput': False}, {'mql': 'ForexLineColor2', 'py': 'ForexLineColor2', 'param': None, 'type': 'color', 'default': 255, 'label': 'Line Down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
SoundAlerts = _input('SoundAlerts', True)
MsgAlerts = _input('MsgAlerts', True)
eMailAlerts = _input('eMailAlerts', False)
SoundAlertFile = _input('SoundAlertFile', 'alert.wav')
ForexLineColor1 = _input('ForexLineColor1', clrBlue)  # Line Up
ForexLineColor2 = _input('ForexLineColor2', clrRed)  # Line Down
lwma05Buffers = Arr(0, 0.0)
lwma10Buffers = Arr(0, 0.0)
lwma20Buffers = Arr(0, 0.0)
line20Buffers = Arr(0, 0.0)
uplineBuffers = Arr(0, 0.0)
dnlineBuffers = Arr(0, 0.0)
macdMnBuffers = Arr(0, 0.0)
macdSgBuffers = Arr(0, 0.0)
curMnt = 0
prvMnt = 0
mafast = 5
maslow = 10
mdma20 = 20
cural = 0
prval = 0
prvAlertBar = 0
ExtMaFastHandle = 0
ExtMaSlowHandle = 0
ExtMACDHandle = 0
lup = False
ldn = False
short_name = ""
alBase = ""
alSubj = ""
alMsg = ""

def OnInit():
    global ExtMACDHandle, ExtMaFastHandle, ExtMaSlowHandle, short_name
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, lwma05Buffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, lwma10Buffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, lwma20Buffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, line20Buffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, uplineBuffers, INDICATOR_DATA)
    SetIndexBuffer(5, dnlineBuffers, INDICATOR_DATA)
    SetIndexBuffer(6, macdMnBuffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, macdSgBuffers, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, ForexLineColor1)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, ForexLineColor2)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, maslow)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, maslow)
    short_name = 'FXLine,' + Symbol() + ',' + 'TF:' + strTF(Period())
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    ExtMaFastHandle = iMA(Symbol(), PERIOD_CURRENT, mafast, 0, MODE_LWMA, PRICE_MEDIAN)
    if ExtMaFastHandle == INVALID_HANDLE:
        printf('Error creating indicator Fast(5) LWMA for ', Symbol())
        return INIT_FAILED
    ExtMaSlowHandle = iMA(Symbol(), PERIOD_CURRENT, mdma20, 0, MODE_SMA, PRICE_MEDIAN)
    if ExtMaSlowHandle == INVALID_HANDLE:
        printf('Error creating indicator Slow(20) SMA Median Price for ', Symbol())
        return INIT_FAILED
    ExtMACDHandle = iMACD(Symbol(), PERIOD_CURRENT, 12, 26, 9, PRICE_CLOSE)
    if ExtMACDHandle == INVALID_HANDLE:
        printf('Failed to create handle of the iMACD indicator for ', Symbol())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), 0, -1)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global cural, ldn, lup
    i = 0
    xlimit = 0
    cural = -1
    lup = False
    ldn = False
    FLOpen = 0.0
    FLClos = 0.0
    if rates_total <= maslow:
        return 0
    ResetLastError()
    ArraySetAsSeries(lwma05Buffers, True)
    ArraySetAsSeries(lwma10Buffers, True)
    ArraySetAsSeries(lwma20Buffers, True)
    ArraySetAsSeries(line20Buffers, True)
    ArraySetAsSeries(uplineBuffers, True)
    ArraySetAsSeries(dnlineBuffers, True)
    ArraySetAsSeries(macdMnBuffers, True)
    ArraySetAsSeries(macdSgBuffers, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    calculated = BarsCalculated(ExtMaFastHandle)
    if calculated < rates_total:
        Print('Not all data of ExtMaFastHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtMaSlowHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtMACDHandle)
    if calculated < rates_total:
        Print('Not all data of ExtMACDHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = Box(0)
    values_to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        values_to_copy = rates_total
        to_copy.v = values_to_copy
    else:
        values_to_copy = rates_total - prev_calculated
        to_copy.v = values_to_copy
        if prev_calculated > 0:
            to_copy.v += 1
        values_to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtMaFastHandle, 0, 0, to_copy.v, lwma05Buffers) < 0:
        Print('Getting ExtMaFastHandle buffers is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtMaSlowHandle, 0, 0, to_copy.v, line20Buffers) < 0:
        Print('Getting ExtMaSlowHandle buffers is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtMACDHandle, 0, 0, values_to_copy, macdMnBuffers) < 0:
        Print('Getting MACD Main buffers is failed! Error', GetLastError())
        return 0
    if CopyBuffer(ExtMACDHandle, 1, 0, values_to_copy, macdSgBuffers) < 0:
        Print('Getting MACD Signal buffers is failed! Error', GetLastError())
        return 0
    xlimit = rates_total - prev_calculated
    if prev_calculated > 0:
        xlimit += 1
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, maslow, lwma05Buffers, lwma10Buffers, to_copy)
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, mdma20, lwma10Buffers, lwma20Buffers, to_copy)
    i = xlimit - 1
    for i in range(i, 0 - 1, -1):
        if lwma05Buffers[i] > lwma20Buffers[i]:
            lup = True
            ldn = False
        if lwma05Buffers[i] < lwma20Buffers[i]:
            ldn = True
            lup = False
        if lup == True:
            uplineBuffers[i] = line20Buffers[i]
            dnlineBuffers[i] = EMPTY_VALUE
        if ldn == True:
            dnlineBuffers[i] = line20Buffers[i]
            uplineBuffers[i] = EMPTY_VALUE
        if i == 0:
            flmacd0 = macdMnBuffers[i] - macdSgBuffers[i]
            flmacd1 = macdMnBuffers[i + 1] - macdSgBuffers[i + 1]
            macdfm0 = macdMnBuffers[i]
            macdfm1 = macdMnBuffers[i + 1]
            FLOpen = (high[i + 1] + low[i + 1] + close[i + 1] + close[i + 1]) / 4
            FLClos = (high[i] + low[i] + close[i] + close[i]) / 4
            flmacdup = flmacd0 > flmacd1 and macdfm0 > macdfm1
            flmacddn = flmacd0 < flmacd1 and macdfm0 < macdfm1
            if ((((lup == True and lwma05Buffers[0] > lwma05Buffers[1]) and flmacdup) and FLClos > FLOpen) and close[0] > open[0]) and close[0] > lwma05Buffers[0]:
                cural = 3
            if (((lup == True and lwma05Buffers[0] > lwma05Buffers[1]) and flmacddn) and FLClos < FLOpen) and close[0] < lwma05Buffers[0]:
                cural = 1
            if (((lup == True and lwma05Buffers[0] <= lwma05Buffers[1]) and flmacddn) and FLClos < FLOpen) and close[0] < lwma05Buffers[0]:
                cural = 5
            if ((((ldn == True and lwma05Buffers[0] < lwma05Buffers[1]) and flmacddn) and FLClos < FLOpen) and close[0] < open[0]) and close[0] < lwma05Buffers[0]:
                cural = 2
            if (((ldn == True and lwma05Buffers[0] < lwma05Buffers[1]) and flmacdup) and FLClos > FLOpen) and close[0] > lwma05Buffers[0]:
                cural = 0
            if (((ldn == True and lwma05Buffers[0] >= lwma05Buffers[1]) and flmacdup) and FLClos > FLOpen) and close[0] > lwma05Buffers[0]:
                cural = 4
    else:
        i = _range_end(i, 0 - 1, -1)
    ChartRedraw(0)
    posAlerts(cural)
    return rates_total

def doAlerts(msgText, eMailSub):
    if MsgAlerts:
        Alert(msgText)
    if SoundAlerts:
        PlaySound(SoundAlertFile)
    if eMailAlerts:
        SendMail(eMailSub, msgText)

def strTF(tf):
    _sw1 = tf
    if _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN1'
    return 'Unknown TF'

def posAlerts(alerts):
    global alBase, alMsg, alSubj, curMnt, prvMnt, prval
    curMnt = TIME_MINUTES
    if curMnt != prvMnt:
        if cural != prval and alerts == 3:
            alBase = short_name + ' @ ' + TimeToString(TimeLocal(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Up,'
            alMsg = alSubj + ' Action: Open BUY.!!'
            prvMnt = curMnt
            prval = cural
            doAlerts(alMsg, alSubj)
        if cural != prval and alerts == 2:
            alBase = short_name + ' @ ' + TimeToString(TimeLocal(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Down,'
            alMsg = alSubj + ' Action: Open SELL.!!'
            prvMnt = curMnt
            prval = cural
            doAlerts(alMsg, alSubj)
        if cural != prval and alerts == 0:
            alBase = short_name + ' @ ' + TimeToString(TimeLocal(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Feasibility Up,'
            alMsg = alSubj + ' Action: Wait and See.!!'
            prvMnt = curMnt
            prval = cural
            doAlerts(alMsg, alSubj)
        if cural != prval and alerts == 1:
            alBase = short_name + ' @ ' + TimeToString(TimeLocal(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Feasibility Down,'
            alMsg = alSubj + ' Action: Wait and See.!!'
            prvMnt = curMnt
            prval = cural
            doAlerts(alMsg, alSubj)
        if cural != prval and alerts == 4:
            alBase = short_name + ' @ ' + TimeToString(TimeLocal(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + ' The Price Began to Up,'
            alMsg = alSubj + ' Action: Wait and See.!!'
            prvMnt = curMnt
            prval = cural
            doAlerts(alMsg, alSubj)
        if cural != prval and alerts == 5:
            alBase = short_name + ' @ ' + TimeToString(TimeLocal(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + ' The Price Began to Down,'
            alMsg = alSubj + ' Action: Wait and See.!!'
            prvMnt = curMnt
            prval = cural
            doAlerts(alMsg, alSubj)
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forexline(_MQL5Indicator):
    name = 'forexline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SoundAlerts': True,
        'MsgAlerts': True,
        'eMailAlerts': False,
    }

