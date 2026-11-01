"""SAR_ADX_Signal — converted from MQL5: MQL5 Indicators/SAR ADX Signal/SAR_ADX_Signal.mq5

This indicator may be repainted
Copyright: Copyright © 2024, Nomocp.; Link: https://t.me/nomocp; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2024, Nomocp.', 'link': 'https://t.me/nomocp', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {}, 'colors': {1: [1692881], 2: [7394329]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['This indicator may be repainted'], 'name': 'SAR_ADX_Signal', 'source': 'MQL5 Indicators/SAR ADX Signal/SAR_ADX_Signal.mq5', 'folder': 'SAR ADX Signal', 'inputs': [{'mql': 'inpEnableNotifyTerminal', 'py': 'inpEnableNotifyTerminal', 'param': 'inpEnableNotifyTerminal', 'type': 'bool', 'default': False, 'label': 'Terminal Push Notification?', 'sinput': True}, {'mql': 'inpEnableNotifyMobile', 'py': 'inpEnableNotifyMobile', 'param': 'inpEnableNotifyMobile', 'type': 'bool', 'default': False, 'label': 'Mobile Push Notification?', 'sinput': True}, {'mql': 'inpSARPeriod', 'py': 'inpSARPeriod', 'param': 'inpSARPeriod', 'type': 'int', 'default': 10, 'label': 'SAR Period', 'sinput': False}, {'mql': 'inpSARMaxStep', 'py': 'inpSARMaxStep', 'param': 'inpSARMaxStep', 'type': 'double', 'default': 0.5, 'label': 'SAR Step', 'sinput': False}, {'mql': 'inpADXPeriod', 'py': 'inpADXPeriod', 'param': 'inpADXPeriod', 'type': 'int', 'default': 7, 'label': 'ADX Period', 'sinput': False}, {'mql': 'inpADXThresHold', 'py': 'inpADXThresHold', 'param': 'inpADXThresHold', 'type': 'double', 'default': 20.0, 'label': 'ADX Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpEnableNotifyTerminal = _input('inpEnableNotifyTerminal', False)  # Terminal Push Notification?
inpEnableNotifyMobile = _input('inpEnableNotifyMobile', False)  # Mobile Push Notification?
inpSARPeriod = _input('inpSARPeriod', 10)  # SAR Period
inpSARMaxStep = _input('inpSARMaxStep', 0.5)  # SAR Step
inpADXPeriod = _input('inpADXPeriod', 7)  # ADX Period
inpADXThresHold = _input('inpADXThresHold', 20.0)  # ADX Threshold
bufferSignalBuy = Arr(0, 0.0)
bufferSignalSell = Arr(0, 0.0)
bufferSAR = Arr(0, 0.0)
bufferADX = Arr(0, 0.0)
handleSAR = 0
handleADX = 0
minInit = 0
isNotify = False

def OnInit():
    global handleADX, handleSAR, minInit
    if inpSARPeriod < 2 or inpADXPeriod < 2:
        return INIT_FAILED
    if inpEnableNotifyMobile and (not TERMINAL_NOTIFICATIONS_ENABLED):
        Alert('Please enable push notification feature at Tools > Option > Notifications')
    SetIndexBuffer(0, bufferSignalSell, INDICATOR_DATA)
    SetIndexBuffer(1, bufferSignalBuy, INDICATOR_DATA)
    SetIndexBuffer(2, bufferSAR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, bufferADX, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'SELL SIGN')
    PlotIndexSetString(1, PLOT_LABEL, 'BUY SIGN')
    ArraySetAsSeries(bufferSignalBuy, True)
    ArraySetAsSeries(bufferSignalSell, True)
    ArraySetAsSeries(bufferSAR, True)
    ArraySetAsSeries(bufferADX, True)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 10)
    minInit = MathMax(inpSARPeriod, inpADXPeriod)
    PlotIndexGetInteger(0, PLOT_DRAW_BEGIN, minInit)
    PlotIndexGetInteger(1, PLOT_DRAW_BEGIN, minInit)
    for i in range(0, 4):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0)
    handleSAR = iSAR(Symbol(), Period(), NormalizeDouble(_fdiv(1, (10 * inpSARPeriod) + 1e-05), 3), inpSARMaxStep)
    handleADX = iADX(Symbol(), Period(), inpADXPeriod)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(handleSAR)
    IndicatorRelease(handleADX)

def isNewBar():
    global _s_isNewBar_lastTime
    lastBarTime = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE)
    if _s_isNewBar_lastTime is _UNSET:
        _s_isNewBar_lastTime = lastBarTime
    if _s_isNewBar_lastTime == lastBarTime:
        return False
    _s_isNewBar_lastTime = lastBarTime
    return True

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global isNotify
    if rates_total < minInit:
        return 0
    if isNewBar():
        isNotify = False
    limit = rates_total - prev_calculated
    if prev_calculated < 1:
        limit = rates_total - minInit
    if limit == 0:
        limit += 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if CopyBuffer(handleADX, MAIN_LINE, 0, limit, bufferADX) < 1 or CopyBuffer(handleSAR, 0, 0, limit, bufferSAR) < 1:
        return prev_calculated
    for bar in range(limit - 1, -1, -1):
        bufferSignalSell[bar] = 0.0
        bufferSignalBuy[bar] = 0.0
        if (bufferSAR[bar] > close[bar] and bufferSAR[bar + 1] < close[bar + 1]) and bufferADX[bar] > inpADXThresHold:
            bufferSignalSell[bar] = high[bar]
            if not isNotify:
                SendMobileNotify(False)
        elif (bufferSAR[bar] < close[bar] and bufferSAR[bar + 1] > close[bar + 1]) and bufferADX[bar] > inpADXThresHold:
            bufferSignalBuy[bar] = low[bar]
            if not isNotify:
                SendMobileNotify(True)
    return rates_total

def SendMobileNotify(isBuy):
    global isNotify
    if (not inpEnableNotifyMobile) and (not inpEnableNotifyTerminal):
        return
    isNotify = True
    pos = ('Buy' if isBuy else 'Sell')
    msg = StringFormat('[%s][%s] %s Signal Appeared!', Symbol(), StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1), pos)
    if inpEnableNotifyMobile:
        SendNotification(msg)
    if inpEnableNotifyTerminal:
        Alert(msg)

# ---- static local variables
_s_isNewBar_lastTime = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SARADXSignal(_MQL5Indicator):
    name = 'SAR_ADX_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpEnableNotifyTerminal': False,  # Terminal Push Notification?
        'inpEnableNotifyMobile': False,  # Mobile Push Notification?
        'inpSARPeriod': 10,  # SAR Period
        'inpSARMaxStep': 0.5,  # SAR Step
        'inpADXPeriod': 7,  # ADX Period
        'inpADXThresHold': 20.0,  # ADX Threshold
    }

