"""Bollinger Squeeze Advanced — converted from MQL5: MQL5 Indicators/Bollinger Squeeze Advanced MT5/Bollinger Squeeze Advanced.mq5

Advanced version of the Bollinger Squeeze with alerts.
BB / Keltner channel squeeze is show with the wide blue bars.
Trend strength and direction histogram can be based on one of the following indicators:
Stochastic, CCI, RSI, MACD, Momentum, Williams % Range, ADX, DeMarker.
Supports multi-timeframe operation.
Copyright: www.Wolfforex.com, 2025; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 10, 2: 3, 3: 1, 4: 1}, 'colors': {1: [32768, 6053069], 2: [16711680], 3: [255], 4: [8421504]}, 'widths': {1: 1, 2: 2}, 'styles': {}, 'labels': {1: 'BS Histo Trending', 2: 'BS Histo Sideways', 3: 'MACD MA', 4: 'BS Histo Line'}, 'levels': [], 'description': ['Advanced version of the Bollinger Squeeze with alerts.', 'BB / Keltner channel squeeze is show with the wide blue bars.', 'Trend strength and direction histogram can be based on one of the following indicators:', 'Stochastic, CCI, RSI, MACD, Momentum, Williams % Range, ADX, DeMarker.', 'Supports multi-timeframe operation.'], 'name': 'Bollinger Squeeze Advanced', 'source': 'MQL5 Indicators/Bollinger Squeeze Advanced MT5/Bollinger Squeeze Advanced.mq5', 'folder': 'Bollinger Squeeze Advanced MT5', 'inputs': [{'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 0, 'label': 'Timeframe', 'sinput': False}, {'mql': 'TriggerType', 'py': 'TriggerType', 'param': 'TriggerType', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MACDFastEMAPeriod', 'py': 'MACDFastEMAPeriod', 'param': 'MACDFastEMAPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'MACDSlowEMAPeriod', 'py': 'MACDSlowEMAPeriod', 'param': 'MACDSlowEMAPeriod', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'MACDMACDEMAPeriod', 'py': 'MACDMACDEMAPeriod', 'param': 'MACDMACDEMAPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'WilliamsPRPeriod', 'py': 'WilliamsPRPeriod', 'param': 'WilliamsPRPeriod', 'type': 'int', 'default': 24, 'label': '', 'sinput': False}, {'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'DeMarkerPeriod', 'py': 'DeMarkerPeriod', 'param': 'DeMarkerPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'AlertOnSidewaysTrending', 'py': 'AlertOnSidewaysTrending', 'param': 'AlertOnSidewaysTrending', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnZeroCross', 'py': 'AlertOnZeroCross', 'param': 'AlertOnZeroCross', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertAboveLevel', 'py': 'AlertAboveLevel', 'param': 'AlertAboveLevel', 'type': 'double', 'default': 0.0, 'label': 'AlertAboveLevel: If you want alerts above a non-zero level.', 'sinput': False}, {'mql': 'AlertBelowLevel', 'py': 'AlertBelowLevel', 'param': 'AlertBelowLevel', 'type': 'double', 'default': 0.0, 'label': 'AlertBelowLevel: If you want alerts below a non-zero level.', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_trigger_types
Stochastic = 0
CCI = 1
RSI = 2
MACD = 3
Momentum = 4
Williams = 5
ADX = 6
DeMarker = 7
_enum('enum_trigger_types', {0: 'Stochastic', 1: 'CCI', 2: 'RSI', 3: 'MACD', 4: 'Momentum', 5: 'Williams', 6: 'ADX', 7: 'DeMarker'})

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
BB_Period = 20
BB_Deviation = 2.0
KeltnerPeriod = 20
KeltnerFactor = 1.5
InpTimeframe = _input('InpTimeframe', PERIOD_CURRENT)  # Timeframe
TriggerType = _input('TriggerType', DeMarker)
StochasticPeriod = _input('StochasticPeriod', 14)
CCIPeriod = _input('CCIPeriod', 50)
RSIPeriod = _input('RSIPeriod', 14)
MACDFastEMAPeriod = _input('MACDFastEMAPeriod', 12)
MACDSlowEMAPeriod = _input('MACDSlowEMAPeriod', 26)
MACDMACDEMAPeriod = _input('MACDMACDEMAPeriod', 9)
MomentumPeriod = _input('MomentumPeriod', 14)
WilliamsPRPeriod = _input('WilliamsPRPeriod', 24)
ADXPeriod = _input('ADXPeriod', 14)
DeMarkerPeriod = _input('DeMarkerPeriod', 13)
AlertOnSidewaysTrending = _input('AlertOnSidewaysTrending', False)
AlertOnZeroCross = _input('AlertOnZeroCross', False)
AlertAboveLevel = _input('AlertAboveLevel', 0.0)  # AlertAboveLevel: If you want alerts above a non-zero level.
AlertBelowLevel = _input('AlertBelowLevel', 0.0)  # AlertBelowLevel: If you want alerts below a non-zero level.
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
HistoTrending = Arr(0, 0.0)
HistoTrendingColor = Arr(0, 0.0)
HistoSideways = Arr(0, 0.0)
MACD_MA = Arr(0, 0.0)
HistoLine = Arr(0, 0.0)
Buffer = Arr(0, 0.0)
MACD_Signal_Buffer = Arr(0, 0.0)
ATR_Buffer = Arr(0, 0.0)
StdDev_Buffer = Arr(0, 0.0)
MaxPeriod = 0
Handle_v = 0
ATR_Handle = 0
StdDev_Handle = 0
Timeframe = 0  # Timeframe of operation
deltaHighTF = 1  # Difference in candles count from the higher timeframe
PrevCalculated = 0
IsTrending = False
IsSideways = False
IsHistogramAboveZero = False
IsHistogramBelowZero = False

def OnInit():
    global ATR_Handle, Handle_v, MaxPeriod, StdDev_Handle, Timeframe, deltaHighTF
    SetIndexBuffer(0, HistoTrending, INDICATOR_DATA)
    SetIndexBuffer(1, HistoTrendingColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, HistoSideways, INDICATOR_DATA)
    SetIndexBuffer(3, MACD_MA, INDICATOR_DATA)
    SetIndexBuffer(4, HistoLine, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(HistoTrending, True)
    ArraySetAsSeries(HistoTrendingColor, True)
    ArraySetAsSeries(HistoSideways, True)
    ArraySetAsSeries(MACD_MA, True)
    ArraySetAsSeries(HistoLine, True)
    Timeframe = InpTimeframe
    if InpTimeframe < Period():
        Timeframe = Period()
    _sw1 = TriggerType
    if _sw1 == Stochastic:
        MaxPeriod = StochasticPeriod
        Handle_v = iStochastic(Symbol(), Timeframe, StochasticPeriod, 3, 3, MODE_SMA, STO_CLOSECLOSE)
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -30)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Stochastic (' + IntegerToString(StochasticPeriod) + ', 3, 3)')
    elif _sw1 == CCI:
        MaxPeriod = CCIPeriod
        Handle_v = iCCI(Symbol(), Timeframe, CCIPeriod, PRICE_CLOSE)
        IndicatorSetInteger(INDICATOR_LEVELS, 4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, -200)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -100)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 100)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, 200)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with CCI (' + IntegerToString(CCIPeriod) + ', CLOSE)')
    elif _sw1 == RSI:
        MaxPeriod = RSIPeriod
        Handle_v = iRSI(Symbol(), Timeframe, RSIPeriod, PRICE_CLOSE)
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 20)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -20)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with RSI (' + IntegerToString(RSIPeriod) + ', CLOSE)')
    elif _sw1 == MACD:
        MaxPeriod = MathMax(MathMax(MACDFastEMAPeriod, MACDSlowEMAPeriod), MACDMACDEMAPeriod)
        Handle_v = iMACD(Symbol(), Timeframe, 12, 26, 9, PRICE_CLOSE)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with MACD (' + IntegerToString(MACDFastEMAPeriod) + ', ' + IntegerToString(MACDSlowEMAPeriod) + ', ' + IntegerToString(MACDMACDEMAPeriod) + ', CLOSE)')
    elif _sw1 == Momentum:
        MaxPeriod = MomentumPeriod
        Handle_v = iMomentum(Symbol(), Timeframe, MomentumPeriod, PRICE_CLOSE)
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -1)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Momentum (' + IntegerToString(MomentumPeriod) + ', CLOSE)')
    elif _sw1 == Williams:
        MaxPeriod = WilliamsPRPeriod
        Handle_v = iWPR(Symbol(), Timeframe, WilliamsPRPeriod)
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -30)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Williams% (' + IntegerToString(WilliamsPRPeriod) + ')')
    elif _sw1 == ADX:
        MaxPeriod = ADXPeriod
        Handle_v = iADX(Symbol(), Timeframe, ADXPeriod)
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 15)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 40)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with ADX (' + IntegerToString(ADXPeriod) + ')')
    elif _sw1 == DeMarker:
        MaxPeriod = DeMarkerPeriod
        Handle_v = iDeMarker(Symbol(), Timeframe, DeMarkerPeriod)
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.25)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -0.25)
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Demarker (' + IntegerToString(DeMarkerPeriod) + ')')
    ATR_Handle = iATR(Symbol(), Timeframe, KeltnerPeriod)
    StdDev_Handle = iStdDev(Symbol(), Timeframe, BB_Period, MODE_SMA, 0, PRICE_CLOSE)
    ArraySetAsSeries(Buffer, True)
    ArraySetAsSeries(MACD_Signal_Buffer, True)
    ArraySetAsSeries(ATR_Buffer, True)
    ArraySetAsSeries(StdDev_Buffer, True)
    MaxPeriod = MathMax(MathMax(MaxPeriod, KeltnerPeriod), BB_Period)
    if PeriodSeconds(Timeframe) > PeriodSeconds():
        deltaHighTF = _idiv(PeriodSeconds(Timeframe), PeriodSeconds())
    ResetGlobalVariables()

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, close, tick_volume, volume, spread):
    global PrevCalculated, _s_OnCalculate_upper_prev_counted
    ArraySetAsSeries(Time, True)
    counted_bars = prev_calculated
    if counted_bars > 0:
        counted_bars -= 1
    PrevCalculated = prev_calculated
    upper_limit = 0
    calculated_start = 0
    if Timeframe != Period():
        upper_limit = iBars(Symbol(), Timeframe) - _s_OnCalculate_upper_prev_counted + 1
        if upper_limit >= (iBars(Symbol(), Timeframe) - MaxPeriod):
            upper_limit = iBars(Symbol(), Timeframe) - MaxPeriod - 1
        if upper_limit > (rates_total - MaxPeriod):
            upper_limit = rates_total - MaxPeriod
        calculated_start = iBarShift(Symbol(), PERIOD_CURRENT, iTime(Symbol(), Timeframe, upper_limit))
    else:
        limit = rates_total - counted_bars
        if limit >= (rates_total - MaxPeriod):
            limit = rates_total - MaxPeriod - 1
        upper_limit = limit
        calculated_start = limit
    copied_Buffer = CopyBuffer(Handle_v, 0, 0, upper_limit, Buffer)
    if copied_Buffer <= 0:
        return 0
    copied_MACD = 0
    if TriggerType == MACD:
        copied_MACD = CopyBuffer(Handle_v, 1, 0, upper_limit, MACD_Signal_Buffer)
        if copied_MACD <= 0:
            return 0
    copied_ATR = CopyBuffer(ATR_Handle, 0, 0, upper_limit, ATR_Buffer)
    if copied_ATR <= 0:
        return 0
    copied_StdDev = CopyBuffer(StdDev_Handle, 0, 0, upper_limit, StdDev_Buffer)
    if copied_StdDev <= 0:
        return 0
    for shift in range(calculated_start, 0 - 1, -1):
        index = iBarShift(Symbol(), Timeframe, Time[shift])
        if (index >= copied_Buffer or index >= copied_ATR) or index >= copied_StdDev:
            continue
        d = 0.0
        MACD_MA[shift] = 0.0
        _sw2 = TriggerType
        if _sw2 == Stochastic:
            d = Buffer[index] - 50
        elif _sw2 == CCI:
            d = Buffer[index]
        elif _sw2 == RSI:
            d = Buffer[index] - 50
        elif _sw2 == MACD:
            d = Buffer[index]
            if index >= copied_MACD:
                continue
            MACD_MA[shift] = MACD_Signal_Buffer[index]
        elif _sw2 == Momentum:
            d = Buffer[index] - 100
        elif _sw2 == Williams:
            d = Buffer[index] + 50
        elif _sw2 == ADX:
            d = Buffer[index]
        elif _sw2 == DeMarker:
            d = Buffer[index] - 0.5
        HistoLine[shift] = d
        diff = ATR_Buffer[index] * KeltnerFactor
        std = StdDev_Buffer[index]
        bbs = _fdiv(BB_Deviation * std, diff)
        if bbs < 1:
            if d > 0:
                HistoSideways[shift] = d
                HistoTrending[shift] = 0.0
            else:
                HistoSideways[shift] = d
                HistoTrending[shift] = 0.0
        else:
            if d > 0:
                HistoTrending[shift] = d
                HistoTrendingColor[shift] = 0.0
                HistoSideways[shift] = 0.0
            else:
                HistoTrending[shift] = d
                HistoTrendingColor[shift] = 1.0
                HistoSideways[shift] = 0.0
    DoAlerts()
    _s_OnCalculate_upper_prev_counted = iBars(Symbol(), Timeframe)
    return rates_total

def DoAlerts():
    global IsHistogramAboveZero, IsHistogramBelowZero, IsSideways, IsTrending
    if ((not EnableEmailAlerts) and (not EnableNativeAlerts)) and (not EnablePushAlerts):
        return
    if not PrevCalculated:
        RefreshGlobalVariables()
    isTrendingMessage = ""
    isSidewaysMessage = ""
    isHistogramAboveZeroMessage = ""
    isHistogramBelowZeroMessage = ""
    if (AlertOnSidewaysTrending and (not IsTrending)) and HasTrending():
        isTrendingMessage = 'Trending'
        IsTrending = True
        IsSideways = False
    if (AlertOnSidewaysTrending and (not IsSideways)) and HasSideways():
        isSidewaysMessage = 'Sideways'
        IsSideways = True
        IsTrending = False
    if (AlertOnZeroCross and (not IsHistogramAboveZero)) and HasHistogramAboveZero():
        isHistogramAboveZeroMessage = 'Histogram Above '
        if AlertAboveLevel == 0:
            isHistogramAboveZeroMessage += 'Zero.'
        else:
            isHistogramAboveZeroMessage += DoubleToString(AlertAboveLevel, 2) + '.'
        IsHistogramAboveZero = True
        IsHistogramBelowZero = False
    if (AlertOnZeroCross and (not IsHistogramBelowZero)) and HasHistogramBelowZero():
        isHistogramBelowZeroMessage = 'Histogram Below '
        if AlertBelowLevel == 0:
            isHistogramBelowZeroMessage += 'Zero.'
        else:
            isHistogramBelowZeroMessage += DoubleToString(AlertBelowLevel, 2) + '.'
        IsHistogramBelowZero = True
        IsHistogramAboveZero = False
    IssueAlerts(isSidewaysMessage)
    IssueAlerts(isTrendingMessage)
    IssueAlerts(isHistogramAboveZeroMessage)
    IssueAlerts(isHistogramBelowZeroMessage)

def ResetGlobalVariables():
    global IsHistogramAboveZero, IsHistogramBelowZero, IsSideways, IsTrending
    IsTrending = False
    IsSideways = False
    IsHistogramAboveZero = False
    IsHistogramBelowZero = False

def RefreshGlobalVariables():
    global IsHistogramAboveZero, IsHistogramBelowZero, IsSideways, IsTrending
    IsTrending = HasTrending()
    IsSideways = HasSideways()
    IsHistogramAboveZero = HasHistogramAboveZero()
    IsHistogramBelowZero = HasHistogramBelowZero()

def IssueAlerts(message):
    if message == "":
        return
    if EnableNativeAlerts:
        Alert(message)
    message = 'BSA: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Timeframe, 'ENUM_TIMEFRAMES'), 7) + ' - ' + message + '.'
    if EnableEmailAlerts:
        SendMail('BSA Alert', message)
    if EnablePushAlerts:
        SendNotification(message)

def HasTrending():
    return HistoTrending[TriggerCandle * deltaHighTF] != 0

def HasSideways():
    return HistoSideways[TriggerCandle * deltaHighTF] != 0

def HasHistogramAboveZero():
    return HistoLine[TriggerCandle * deltaHighTF] > AlertAboveLevel

def HasHistogramBelowZero():
    return HistoLine[TriggerCandle * deltaHighTF] < AlertBelowLevel

# ---- static local variables
_s_OnCalculate_upper_prev_counted = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerSqueezeAdvanced(_MQL5Indicator):
    name = 'Bollinger Squeeze Advanced'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe
        'TriggerType': _Choice({0: 'Stochastic', 1: 'CCI', 2: 'RSI', 3: 'MACD', 4: 'Momentum', 5: 'Williams % Range', 6: 'ADX', 7: 'DeMarker'}, default=7),
        'StochasticPeriod': 14,
        'CCIPeriod': 50,
        'RSIPeriod': 14,
        'MACDFastEMAPeriod': 12,
        'MACDSlowEMAPeriod': 26,
        'MACDMACDEMAPeriod': 9,
        'MomentumPeriod': 14,
        'WilliamsPRPeriod': 24,
        'ADXPeriod': 14,
        'DeMarkerPeriod': 13,
        'AlertOnSidewaysTrending': False,
        'AlertOnZeroCross': False,
        'AlertAboveLevel': 0.0,  # AlertAboveLevel: If you want alerts above a non-zero level.
        'AlertBelowLevel': 0.0,  # AlertBelowLevel: If you want alerts below a non-zero level.
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

