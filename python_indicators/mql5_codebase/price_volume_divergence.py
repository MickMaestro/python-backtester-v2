"""Price_Volume_Divergence — converted from MQL5: MQL5 Indicators/Price_Volume_Divergence/Price_Volume_Divergence.mq5

Price volume divergence indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Growing Div', 2: 'Falling Div'}, 'levels': [], 'description': ['Price volume divergence indicator'], 'name': 'Price_Volume_Divergence', 'source': 'MQL5 Indicators/Price_Volume_Divergence/Price_Volume_Divergence.mq5', 'folder': 'Price_Volume_Divergence', 'inputs': [{'mql': 'InpUseAlerts', 'py': 'InpUseAlerts', 'param': 'InpUseAlerts', 'type': 'int', 'default': 1, 'label': 'Use alerts', 'sinput': False}, {'mql': 'InpSendMail', 'py': 'InpSendMail', 'param': 'InpSendMail', 'type': 'int', 'default': 0, 'label': 'Send mail', 'sinput': False}, {'mql': 'InpSendPush', 'py': 'InpSendPush', 'param': 'InpSendPush', 'type': 'int', 'default': 1, 'label': 'Send push-notifications', 'sinput': False}, {'mql': 'InpAppliedVolume', 'py': 'InpAppliedVolume', 'param': 'InpAppliedVolume', 'type': 'int', 'default': 0, 'label': 'Applied volume', 'sinput': False}, {'mql': 'InpShowVolume', 'py': 'InpShowVolume', 'param': 'InpShowVolume', 'type': 'int', 'default': 1, 'label': 'Show volumes bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

CHART_VOLUME_HIDE = 0  # MQL5 constant unknown to the converter
CHART_VOLUME_REAL = 0  # MQL5 constant unknown to the converter
CHART_VOLUME_TICK = 0  # MQL5 constant unknown to the converter

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpUseAlerts = _input('InpUseAlerts', INPUT_YES)  # Use alerts
InpSendMail = _input('InpSendMail', INPUT_NO)  # Send mail
InpSendPush = _input('InpSendPush', INPUT_YES)  # Send push-notifications
InpAppliedVolume = _input('InpAppliedVolume', VOLUME_TICK)  # Applied volume
InpShowVolume = _input('InpShowVolume', INPUT_YES)  # Show volumes bars
BufferDivUP = Arr(0, 0.0)
BufferDivDN = Arr(0, 0.0)
BufferVolume = Arr(0, 0.0)
prev_volume = 0

def OnInit():
    global prev_volume
    prev_volume = ChartGetInteger(0, CHART_SHOW_VOLUMES)
    if InpShowVolume:
        ChartSetInteger(0, CHART_SHOW_VOLUMES, (CHART_VOLUME_TICK if (InpAppliedVolume == VOLUME_TICK) else CHART_VOLUME_REAL))
        ChartRedraw(0)
    else:
        ChartSetInteger(0, CHART_SHOW_VOLUMES, CHART_VOLUME_HIDE)
        ChartRedraw(0)
    SetIndexBuffer(0, BufferDivUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDivDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferVolume, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 225)
    PlotIndexSetInteger(1, PLOT_ARROW, 226)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price volume divergence')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDivUP, True)
    ArraySetAsSeries(BufferDivDN, True)
    ArraySetAsSeries(BufferVolume, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_SHOW_VOLUMES, prev_volume)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(tick_volume, True)
    ArraySetAsSeries(volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferDivUP, EMPTY_VALUE)
        ArrayInitialize(BufferDivDN, EMPTY_VALUE)
        ArrayInitialize(BufferVolume, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVolume[i] = float((tick_volume[i] if (InpAppliedVolume == VOLUME_TICK) else volume[i]))
    for i in range(limit, 0 - 1, -1):
        Range0 = high[i] - low[i]
        Range1 = high[i + 1] - low[i + 1]
        if Range1 > Range0 and BufferVolume[i + 1] < BufferVolume[i]:
            BufferDivDN[i] = low[i]
            if i == 0:
                if _s_OnCalculate_last_time != time[0]:
                    message = Symbol() + ', ' + TimeframeToString(Period()) + ': Falling Price/Volume divergence at ' + TimeToString(TimeCurrent())
                    if InpUseAlerts:
                        Alert(message)
                    if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                        SendMail('Price volume divergence Signal', message)
                    if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                        SendNotification(message)
                    _s_OnCalculate_last_time = time[0]
        else:
            BufferDivDN[i] = EMPTY_VALUE
        if Range1 < Range0 and BufferVolume[i + 1] > BufferVolume[i]:
            BufferDivUP[i] = high[i]
            if i == 0:
                if _s_OnCalculate_last_time != time[0]:
                    message = Symbol() + ', ' + TimeframeToString(Period()) + ': Growing Price/Volume divergence at ' + TimeToString(TimeCurrent())
                    if InpUseAlerts:
                        Alert(message)
                    if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                        SendMail('Price volume divergence Signal', message)
                    if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                        SendNotification(message)
                    _s_OnCalculate_last_time = time[0]
        else:
            BufferDivUP[i] = EMPTY_VALUE
    return rates_total

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceVolumeDivergence(_MQL5Indicator):
    name = 'Price_Volume_Divergence'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpUseAlerts': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use alerts
        'InpSendMail': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Send mail
        'InpSendPush': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Send push-notifications
        'InpAppliedVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Applied volume
        'InpShowVolume': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show volumes bars
    }

