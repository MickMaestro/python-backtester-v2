"""3_in_1_Stochastic — converted from MQL5: MQL5 Indicators/3_in_1_Stochastic/3_in_1_Stochastic.mq5

3 in 1 MTF Stochastic with MA Smoothing options indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 27, 'indicator_plots': 10}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 5, 10: 5}, 'colors': {1: [9419919, 8894686], 2: [3329434, 42495], 3: [32768], 4: [255], 5: [32768], 6: [255], 7: [32768], 8: [255], 9: [32768], 10: [255]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, 'labels': {1: 'Cloud2', 2: 'Cloud3', 3: 'SK1', 4: 'SD1', 5: 'SK2', 6: 'SD2', 7: 'SK3', 8: 'SD3', 9: 'Up signal', 10: 'Down signal'}, 'levels': [], 'description': ['3 in 1 MTF Stochastic with MA Smoothing options indicator'], 'name': '3_in_1_Stochastic', 'source': 'MQL5 Indicators/3_in_1_Stochastic/3_in_1_Stochastic.mq5', 'folder': '3_in_1_Stochastic', 'inputs': [{'mql': 'InpPeriodK1', 'py': 'InpPeriodK1', 'param': 'InpPeriodK1', 'type': 'uint', 'default': 5, 'label': 'First Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD1', 'py': 'InpPeriodD1', 'param': 'InpPeriodD1', 'type': 'uint', 'default': 3, 'label': 'First Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing1', 'py': 'InpSlowing1', 'param': 'InpSlowing1', 'type': 'uint', 'default': 3, 'label': 'First Stochastic slowing', 'sinput': False}, {'mql': 'InpTypeSmK1', 'py': 'InpTypeSmK1', 'param': 'InpTypeSmK1', 'type': 'int', 'default': 0, 'label': 'First Stochastic %K smoothing type', 'sinput': False}, {'mql': 'InpTypeSmD1', 'py': 'InpTypeSmD1', 'param': 'InpTypeSmD1', 'type': 'int', 'default': 0, 'label': 'First Stochastic %D smoothing type', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second Stochastic timeframe', 'sinput': False}, {'mql': 'InpPeriodK2', 'py': 'InpPeriodK2', 'param': 'InpPeriodK2', 'type': 'uint', 'default': 5, 'label': 'Second Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD2', 'py': 'InpPeriodD2', 'param': 'InpPeriodD2', 'type': 'uint', 'default': 3, 'label': 'Second Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing2', 'py': 'InpSlowing2', 'param': 'InpSlowing2', 'type': 'uint', 'default': 3, 'label': 'Second Stochastic slowing', 'sinput': False}, {'mql': 'InpTypeSmK2', 'py': 'InpTypeSmK2', 'param': 'InpTypeSmK2', 'type': 'int', 'default': 0, 'label': 'Second Stochastic %K smoothing type', 'sinput': False}, {'mql': 'InpTypeSmD2', 'py': 'InpTypeSmD2', 'param': 'InpTypeSmD2', 'type': 'int', 'default': 0, 'label': 'Second Stochastic %D smoothing type', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third Stochastic timeframe', 'sinput': False}, {'mql': 'InpPeriodK3', 'py': 'InpPeriodK3', 'param': 'InpPeriodK3', 'type': 'uint', 'default': 5, 'label': 'Third Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD3', 'py': 'InpPeriodD3', 'param': 'InpPeriodD3', 'type': 'uint', 'default': 3, 'label': 'Third Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing3', 'py': 'InpSlowing3', 'param': 'InpSlowing3', 'type': 'uint', 'default': 3, 'label': 'Third Stochastic slowing', 'sinput': False}, {'mql': 'InpTypeSmK3', 'py': 'InpTypeSmK3', 'param': 'InpTypeSmK3', 'type': 'int', 'default': 0, 'label': 'Third Stochastic %K smoothing type', 'sinput': False}, {'mql': 'InpTypeSmD3', 'py': 'InpTypeSmD3', 'param': 'InpTypeSmD3', 'type': 'int', 'default': 0, 'label': 'Third Stochastic %D smoothing type', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Bigger timeframes drawing mode', 'sinput': False}, {'mql': 'InpShowClouds', 'py': 'InpShowClouds', 'param': 'InpShowClouds', 'type': 'int', 'default': 1, 'label': 'Show clouds', 'sinput': False}, {'mql': 'InpShowAlert', 'py': 'InpShowAlert', 'param': 'InpShowAlert', 'type': 'int', 'default': 1, 'label': 'Show alerts', 'sinput': False}, {'mql': 'InpSendMail', 'py': 'InpSendMail', 'param': 'InpSendMail', 'type': 'int', 'default': 0, 'label': 'Send mail', 'sinput': False}, {'mql': 'InpSendPush', 'py': 'InpSendPush', 'param': 'InpSendPush', 'type': 'int', 'default': 1, 'label': 'Send push', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_TYPE_SMOOTH_K
TYPE_SMOOTH_K_SMA = 0
TYPE_SMOOTH_K_EMA = 1
TYPE_SMOOTH_K_FAST = 2
_enum('ENUM_TYPE_SMOOTH_K', {0: 'TYPE_SMOOTH_K_SMA', 1: 'TYPE_SMOOTH_K_EMA', 2: 'TYPE_SMOOTH_K_FAST'})

# enum ENUM_TYPE_SMOOTH_D
TYPE_SMOOTH_D_SMA = 0
TYPE_SMOOTH_D_EMA = 1
_enum('ENUM_TYPE_SMOOTH_D', {0: 'TYPE_SMOOTH_D_SMA', 1: 'TYPE_SMOOTH_D_EMA'})

# ---- inputs and global variables
InpPeriodK1 = _input('InpPeriodK1', 5)  # First Stochastic %K period
InpPeriodD1 = _input('InpPeriodD1', 3)  # First Stochastic %D period
InpSlowing1 = _input('InpSlowing1', 3)  # First Stochastic slowing
InpTypeSmK1 = _input('InpTypeSmK1', TYPE_SMOOTH_K_SMA)  # First Stochastic %K smoothing type
InpTypeSmD1 = _input('InpTypeSmD1', TYPE_SMOOTH_D_SMA)  # First Stochastic %D smoothing type
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second Stochastic timeframe
InpPeriodK2 = _input('InpPeriodK2', 5)  # Second Stochastic %K period
InpPeriodD2 = _input('InpPeriodD2', 3)  # Second Stochastic %D period
InpSlowing2 = _input('InpSlowing2', 3)  # Second Stochastic slowing
InpTypeSmK2 = _input('InpTypeSmK2', TYPE_SMOOTH_K_SMA)  # Second Stochastic %K smoothing type
InpTypeSmD2 = _input('InpTypeSmD2', TYPE_SMOOTH_D_SMA)  # Second Stochastic %D smoothing type
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third Stochastic timeframe
InpPeriodK3 = _input('InpPeriodK3', 5)  # Third Stochastic %K period
InpPeriodD3 = _input('InpPeriodD3', 3)  # Third Stochastic %D period
InpSlowing3 = _input('InpSlowing3', 3)  # Third Stochastic slowing
InpTypeSmK3 = _input('InpTypeSmK3', TYPE_SMOOTH_K_SMA)  # Third Stochastic %K smoothing type
InpTypeSmD3 = _input('InpTypeSmD3', TYPE_SMOOTH_D_SMA)  # Third Stochastic %D smoothing type
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Bigger timeframes drawing mode
InpShowClouds = _input('InpShowClouds', INPUT_YES)  # Show clouds
InpShowAlert = _input('InpShowAlert', INPUT_YES)  # Show alerts
InpSendMail = _input('InpSendMail', INPUT_NO)  # Send mail
InpSendPush = _input('InpSendPush', INPUT_YES)  # Send push
BufferCloud21 = Arr(0, 0.0)
BufferCloud22 = Arr(0, 0.0)
BufferCloud31 = Arr(0, 0.0)
BufferCloud32 = Arr(0, 0.0)
BufferSK1 = Arr(0, 0.0)
BufferSD1 = Arr(0, 0.0)
BufferSK2 = Arr(0, 0.0)
BufferSD2 = Arr(0, 0.0)
BufferSK3 = Arr(0, 0.0)
BufferSD3 = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferSK2tmp = Arr(0, 0.0)
BufferSD2tmp = Arr(0, 0.0)
BufferSK3tmp = Arr(0, 0.0)
BufferSD3tmp = Arr(0, 0.0)
BufferMin1 = Arr(0, 0.0)
BufferMax1 = Arr(0, 0.0)
BufferFastK1 = Arr(0, 0.0)
BufferMin2 = Arr(0, 0.0)
BufferMax2 = Arr(0, 0.0)
BufferFastK2 = Arr(0, 0.0)
BufferMin3 = Arr(0, 0.0)
BufferMax3 = Arr(0, 0.0)
BufferFastK3 = Arr(0, 0.0)
BufferClose2 = Arr(0, 0.0)
BufferClose3 = Arr(0, 0.0)
timeframe2 = 0
timeframe3 = 0
overbought = 0.0
oversold = 0.0
periodK1 = 0
periodK2 = 0
periodK3 = 0
periodD1 = 0
periodD2 = 0
periodD3 = 0
slowing1 = 0
slowing2 = 0
slowing3 = 0

def OnInit():
    global overbought, oversold, periodD1, periodD2, periodD3, periodK1, periodK2, periodK3, slowing1, slowing2, slowing3, timeframe2, timeframe3
    EventSetTimer(90)
    periodK1 = (1 if (InpPeriodK1 < 1) else InpPeriodK1)
    periodD1 = (1 if (InpPeriodD1 < 1) else InpPeriodD1)
    slowing1 = (1 if (InpSlowing1 < 1) else InpSlowing1)
    periodK2 = (1 if (InpPeriodK2 < 1) else InpPeriodK2)
    periodD2 = (1 if (InpPeriodD2 < 1) else InpPeriodD2)
    slowing2 = (1 if (InpSlowing2 < 1) else InpSlowing2)
    periodK3 = (1 if (InpPeriodK3 < 1) else InpPeriodK3)
    periodD3 = (1 if (InpPeriodD3 < 1) else InpPeriodD3)
    slowing3 = (1 if (InpSlowing3 < 1) else InpSlowing3)
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferCloud21, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCloud22, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCloud31, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCloud32, INDICATOR_DATA)
    SetIndexBuffer(4, BufferSK1, INDICATOR_DATA)
    SetIndexBuffer(5, BufferSD1, INDICATOR_DATA)
    SetIndexBuffer(6, BufferSK2, INDICATOR_DATA)
    SetIndexBuffer(7, BufferSD2, INDICATOR_DATA)
    SetIndexBuffer(8, BufferSK3, INDICATOR_DATA)
    SetIndexBuffer(9, BufferSD3, INDICATOR_DATA)
    SetIndexBuffer(10, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(11, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(12, BufferSK2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferSD2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferSK3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferSD3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferMin1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, BufferMin2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, BufferMin3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(19, BufferMax1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(20, BufferMax2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(21, BufferMax3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(22, BufferFastK1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(23, BufferFastK2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(24, BufferFastK3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(25, BufferClose2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(26, BufferClose3, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(8, PLOT_ARROW, 233)
    PlotIndexSetInteger(9, PLOT_ARROW, 234)
    label = TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' in ' + TimeframeToString(Period()) + ' Stochastic'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(Period()) + ' Stochastic')
    PlotIndexSetString(3, PLOT_LABEL, TimeframeToString(Period()) + ' Signal')
    PlotIndexSetString(4, PLOT_LABEL, TimeframeToString(timeframe2) + ' Stochastic')
    PlotIndexSetString(5, PLOT_LABEL, TimeframeToString(timeframe2) + ' Signal')
    PlotIndexSetString(6, PLOT_LABEL, TimeframeToString(timeframe3) + ' Stochastic')
    PlotIndexSetString(7, PLOT_LABEL, TimeframeToString(timeframe3) + ' Signal')
    ArraySetAsSeries(BufferCloud21, True)
    ArraySetAsSeries(BufferCloud22, True)
    ArraySetAsSeries(BufferCloud31, True)
    ArraySetAsSeries(BufferCloud32, True)
    ArraySetAsSeries(BufferSK1, True)
    ArraySetAsSeries(BufferSD1, True)
    ArraySetAsSeries(BufferSK2, True)
    ArraySetAsSeries(BufferSD2, True)
    ArraySetAsSeries(BufferSK3, True)
    ArraySetAsSeries(BufferSD3, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferSK2tmp, True)
    ArraySetAsSeries(BufferSD2tmp, True)
    ArraySetAsSeries(BufferSK3tmp, True)
    ArraySetAsSeries(BufferSD3tmp, True)
    ArraySetAsSeries(BufferMax1, True)
    ArraySetAsSeries(BufferMax2, True)
    ArraySetAsSeries(BufferMax3, True)
    ArraySetAsSeries(BufferMin1, True)
    ArraySetAsSeries(BufferMin2, True)
    ArraySetAsSeries(BufferMin3, True)
    ArraySetAsSeries(BufferFastK1, True)
    ArraySetAsSeries(BufferFastK2, True)
    ArraySetAsSeries(BufferFastK3, True)
    ArraySetAsSeries(BufferClose2, True)
    ArraySetAsSeries(BufferClose3, True)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if (rates_total < 4 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCloud21, EMPTY_VALUE)
        ArrayInitialize(BufferCloud22, EMPTY_VALUE)
        ArrayInitialize(BufferCloud31, EMPTY_VALUE)
        ArrayInitialize(BufferCloud32, EMPTY_VALUE)
        ArrayInitialize(BufferSK1, 0)
        ArrayInitialize(BufferSD1, 0)
        ArrayInitialize(BufferSK2, 0)
        ArrayInitialize(BufferSD2, 0)
        ArrayInitialize(BufferSK3, 0)
        ArrayInitialize(BufferSD3, 0)
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferSK2tmp, 0)
        ArrayInitialize(BufferSD2tmp, 0)
        ArrayInitialize(BufferSK3tmp, 0)
        ArrayInitialize(BufferSD3tmp, 0)
        ArrayInitialize(BufferMax1, 0)
        ArrayInitialize(BufferMax2, 0)
        ArrayInitialize(BufferMax3, 0)
        ArrayInitialize(BufferMin1, 0)
        ArrayInitialize(BufferMin2, 0)
        ArrayInitialize(BufferMin3, 0)
        ArrayInitialize(BufferFastK1, 0)
        ArrayInitialize(BufferFastK2, 0)
        ArrayInitialize(BufferFastK3, 0)
        ArrayInitialize(BufferClose2, 0)
        ArrayInitialize(BufferClose3, 0)
    for i in range(limit, 0 - 1, -1):
        close2 = Close("", timeframe2, i)
        if close2 == 0:
            continue
        BufferClose2[i] = close2
        close3 = Close("", timeframe3, i)
        if close3 == 0:
            continue
        BufferClose3[i] = close3
        DataPreparing(rates_total, i, periodK1, close, BufferMin1, BufferMax1, BufferFastK1)
        DataPreparing(rates_total, i, periodK2, BufferClose2, BufferMin2, BufferMax2, BufferFastK2)
        DataPreparing(rates_total, i, periodK3, BufferClose3, BufferMin3, BufferMax3, BufferFastK3)
        CalculateSK(rates_total, i, periodK1, slowing1, BufferMin1, BufferMax1, BufferFastK1, BufferSK1)
        CalculateSK(rates_total, i, periodK2, slowing2, BufferMin2, BufferMax2, BufferFastK2, BufferSK2tmp)
        CalculateSK(rates_total, i, periodK3, slowing3, BufferMin3, BufferMax3, BufferFastK3, BufferSK3tmp)
        if InpTypeSmD1 == TYPE_SMOOTH_D_SMA:
            BufferSD1[i] = GetSMA(rates_total, BufferSK1, periodD1, i)
            BufferSD2tmp[i] = GetSMA(rates_total, BufferSK2tmp, periodD2, i)
            BufferSD3tmp[i] = GetSMA(rates_total, BufferSK3tmp, periodD3, i)
        else:
            BufferSD1[i] = GetEMA(rates_total, BufferSK1[i], BufferSD1[i + 1], periodD1, i)
            BufferSD2tmp[i] = GetEMA(rates_total, BufferSK2tmp[i], BufferSD2tmp[i + 1], periodD2, i)
            BufferSD3tmp[i] = GetEMA(rates_total, BufferSK3tmp[i], BufferSD3tmp[i + 1], periodD3, i)
        DataConversion(rates_total, "", timeframe2, i, BufferSK2tmp, BufferSK2, BufferCloud21, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferSD2tmp, BufferSD2, BufferCloud22, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferSK3tmp, BufferSK3, BufferCloud31, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferSD3tmp, BufferSD3, BufferCloud32, InpDrawMode)
    alerts = ''
    for i in range(limit, 0 - 1, -1):
        BufferCloud32[i] = EMPTY_VALUE
        BufferCloud31[i] = BufferCloud32[i]
        BufferCloud22[i] = BufferCloud31[i]
        BufferCloud21[i] = BufferCloud22[i]
        BufferDN[i] = BufferCloud21[i]
        BufferUP[i] = BufferDN[i]
        if InpShowClouds:
            BufferCloud21[i] = BufferSK2[i]
            BufferCloud22[i] = BufferSD2[i]
            BufferCloud31[i] = BufferSK3[i]
            BufferCloud32[i] = BufferSD3[i]
        if ((BufferSK1[i] > BufferSD1[i] and BufferSK1[i + 1] <= BufferSD1[i + 1]) and BufferSK2[i] > BufferSD2[i]) and BufferSK3[i] > BufferSD3[i]:
            BufferUP[i] = BufferSK1[i]
            if i == 0:
                alerts = 'Up Signal'
        if ((BufferSK1[i] < BufferSD1[i] and BufferSK1[i + 1] >= BufferSD1[i + 1]) and BufferSK2[i] < BufferSD2[i]) and BufferSK3[i] < BufferSD3[i]:
            BufferDN[i] = BufferSK1[i]
            if i == 0:
                alerts = 'Down Signal'
        if (i == 0 and time[0] > _s_OnCalculate_last_time) and alerts != '':
            message = Symbol() + ', ' + TimeframeToString(Period()) + ': 3 in 1 Stochastic ' + alerts
            if InpShowAlert:
                Alert(message)
            if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                SendMail('3 in 1 Stochastic Signal', message)
            if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                SendNotification(message)
            _s_OnCalculate_last_time = TimeCurrent()
    return rates_total

def OnTimer():
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)

def DataConversion(rates_total, symbol_name, timeframe_src, shift, buffer_src, buffer_dest, buffer_cloud, mode=DRAW_MODE_STEPS):
    if timeframe_src == Period():
        buffer_dest[shift] = buffer_src[shift]
        return
    bar_curr = BarToCurrent(symbol_name, timeframe_src, shift)
    if bar_curr > (rates_total - 1):
        return
    bar_prev = BarToCurrent(symbol_name, timeframe_src, shift + 1)
    bar_next = (BarToCurrent(symbol_name, timeframe_src, shift - 1) if (shift > 0) else 0)
    if (bar_prev == WRONG_VALUE or bar_curr == WRONG_VALUE) or bar_next == WRONG_VALUE:
        return
    buffer_dest[bar_curr] = buffer_src[shift]
    if mode == DRAW_MODE_STEPS:
        for j in range(bar_curr, bar_next - 1, -1):
            buffer_dest[j] = buffer_dest[bar_curr]
            if InpShowClouds:
                buffer_cloud[j] = buffer_dest[bar_curr]
    else:
        if bar_prev > (rates_total - 1):
            return
        for j in range(bar_prev, bar_curr - 1, -1):
            buffer_dest[j] = EquationDirect(bar_prev, buffer_dest[bar_prev], bar_curr, buffer_dest[bar_curr], j)
            if InpShowClouds:
                buffer_cloud[j] = buffer_dest[j]
        if shift == 0:
            for j in range(bar_curr, 0 - 1, -1):
                buffer_dest[j] = buffer_dest[bar_curr]
                if InpShowClouds:
                    buffer_cloud[j] = buffer_dest[bar_curr]

def BarToCurrent(symbol_name, timeframe_src, shift, exact=False):
    time = Time(symbol_name, timeframe_src, shift)
    return (BarShift(symbol_name, Period(), time, exact) if (time != 0) else WRONG_VALUE)

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Close(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyClose(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

def DataPreparing(rates_total, shift, period_k, buffer_src, buffer_min, buffer_max, buffer_fast_k):
    if shift > (rates_total - period_k - 1):
        return
    max_ = 0.0
    min_ = 0.0
    for j in range(shift + period_k - 1, shift - 1, -1):
        if j == (shift + period_k - 1):
            min_ = buffer_src[j]
            max_ = min_
        else:
            if buffer_src[j] > max_:
                max_ = buffer_src[j]
            if buffer_src[j] < min_:
                min_ = buffer_src[j]
    buffer_min[shift] = buffer_src[shift] - min_
    buffer_max[shift] = max_ - min_
    buffer_fast_k[shift] = ((_fdiv(buffer_min[shift], buffer_max[shift]) * 100.0) if (buffer_max[shift] > 0) else 50.0)

def CalculateSK(rates_total, shift, period_k, slowing, buffer_min, buffer_max, buffer_fast, buffer_sk):
    sum_max = 0.0
    sum_min = 0.0
    if InpTypeSmK1 == TYPE_SMOOTH_K_FAST:
        if shift > (rates_total - period_k - 1):
            return
        for j in range(shift + period_k - 1, shift - 1, -1):
            sum_max += buffer_max[j]
        if sum_max != 0:
            for j in range(shift + period_k - 1, shift - 1, -1):
                sum_min += buffer_min[j]
            buffer_sk[shift] = _fdiv(sum_min, sum_max) * 100.0
        else:
            buffer_sk[shift] = 50.0
    else:
        if shift > (rates_total - slowing - 1):
            return
        if InpTypeSmK1 == TYPE_SMOOTH_K_SMA:
            buffer_sk[shift] = GetSMA(rates_total, buffer_fast, slowing, shift)
        else:
            buffer_sk[shift] = GetEMA(rates_total, buffer_fast[shift], buffer_sk[shift + 1], slowing, shift)

def GetSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def GetEMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3In1Stochastic(_MQL5Indicator):
    name = '3_in_1_Stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodK1': 5,  # First Stochastic %K period
        'InpPeriodD1': 3,  # First Stochastic %D period
        'InpSlowing1': 3,  # First Stochastic slowing
        'InpTypeSmK1': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Fast'}, default=0),  # First Stochastic %K smoothing type
        'InpTypeSmD1': _Choice({0: 'Simple', 1: 'Exponential'}, default=0),  # First Stochastic %D smoothing type
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second Stochastic timeframe
        'InpPeriodK2': 5,  # Second Stochastic %K period
        'InpPeriodD2': 3,  # Second Stochastic %D period
        'InpSlowing2': 3,  # Second Stochastic slowing
        'InpTypeSmK2': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Fast'}, default=0),  # Second Stochastic %K smoothing type
        'InpTypeSmD2': _Choice({0: 'Simple', 1: 'Exponential'}, default=0),  # Second Stochastic %D smoothing type
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third Stochastic timeframe
        'InpPeriodK3': 5,  # Third Stochastic %K period
        'InpPeriodD3': 3,  # Third Stochastic %D period
        'InpSlowing3': 3,  # Third Stochastic slowing
        'InpTypeSmK3': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Fast'}, default=0),  # Third Stochastic %K smoothing type
        'InpTypeSmD3': _Choice({0: 'Simple', 1: 'Exponential'}, default=0),  # Third Stochastic %D smoothing type
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Bigger timeframes drawing mode
        'InpShowClouds': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show clouds
        'InpShowAlert': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show alerts
        'InpSendMail': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Send mail
        'InpSendPush': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Send push
    }

