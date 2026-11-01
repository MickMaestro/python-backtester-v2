"""Donchian Ultimate — converted from MQL5: MQL5 Indicators/Donchian Ultimate Indicator for MT5/Donchian Ultimate.mq5

A classic Donchian Channel indicator with extra features:
 * MTF support
 * Multiple boundary calculation options
 * Support and resistance zones
 * Alert system
Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 7, 7: 7}, 'colors': {1: [32768], 2: [255], 3: [16711680], 4: [10025880], 5: [7504122], 6: [10025880, 10025880], 7: [7504122, 7504122]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {4: 2, 5: 2}, 'labels': {1: 'Upper Line', 2: 'Lower Line', 3: 'Mid Line', 4: 'Resistance', 5: 'Support', 6: 'Resistance Span', 7: 'Support Span'}, 'levels': [], 'description': ['A classic Donchian Channel indicator with extra features:', ' * MTF support', ' * Multiple boundary calculation options', ' * Support and resistance zones', ' * Alert system'], 'name': 'Donchian Ultimate', 'source': 'MQL5 Indicators/Donchian Ultimate Indicator for MT5/Donchian Ultimate.mq5', 'folder': 'Donchian Ultimate Indicator for MT5', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 0, 'label': 'Timeframe', 'sinput': False}, {'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'IsShowResistanceSpan', 'py': 'IsShowResistanceSpan', 'param': 'IsShowResistanceSpan', 'type': 'bool', 'default': True, 'label': 'Show Resistance Span', 'sinput': False}, {'mql': 'IsShowSupportSpan', 'py': 'IsShowSupportSpan', 'param': 'IsShowSupportSpan', 'type': 'bool', 'default': True, 'label': 'Show Support Span', 'sinput': False}, {'mql': 'AlertCandle', 'py': 'AlertCandle', 'param': 'AlertCandle', 'type': 'int', 'default': 0, 'label': 'Alert Candle', 'sinput': False}, {'mql': 'IsAlertMidLineBullishCrossing', 'py': 'IsAlertMidLineBullishCrossing', 'param': 'IsAlertMidLineBullishCrossing', 'type': 'bool', 'default': True, 'label': 'Alert About Bullish Crossing of Mid Line', 'sinput': False}, {'mql': 'IsAlertMidLineBearishCrossing', 'py': 'IsAlertMidLineBearishCrossing', 'param': 'IsAlertMidLineBearishCrossing', 'type': 'bool', 'default': True, 'label': 'Alert About Bearish Crossing of Mid Line', 'sinput': False}, {'mql': 'IsAlertCandleCloseInsideResistance', 'py': 'IsAlertCandleCloseInsideResistance', 'param': 'IsAlertCandleCloseInsideResistance', 'type': 'bool', 'default': True, 'label': 'Alert About Candle Close Inside Resistance', 'sinput': False}, {'mql': 'IsAlertCandleCloseInsideSupport', 'py': 'IsAlertCandleCloseInsideSupport', 'param': 'IsAlertCandleCloseInsideSupport', 'type': 'bool', 'default': True, 'label': 'Alert About Candle Close Inside Support', 'sinput': False}, {'mql': 'IsShowAlert', 'py': 'IsShowAlert', 'param': 'IsShowAlert', 'type': 'bool', 'default': False, 'label': 'Show Alert', 'sinput': False}, {'mql': 'IsSendEmail', 'py': 'IsSendEmail', 'param': 'IsSendEmail', 'type': 'bool', 'default': False, 'label': 'Send Email', 'sinput': False}, {'mql': 'IsSendNotification', 'py': 'IsSendNotification', 'param': 'IsSendNotification', 'type': 'bool', 'default': False, 'label': 'Send Notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE_TYPE
PRICE_HH_LL = 0
PRICE_AVER_HHHO_LLLO = 1
PRICE_AVER_HHHC_LLLC = 2
PRICE_HO_LO = 3
PRICE_HC_LC = 4
_enum('ENUM_PRICE_TYPE', {0: 'PRICE_HH_LL', 1: 'PRICE_AVER_HHHO_LLLO', 2: 'PRICE_AVER_HHHC_LLLC', 3: 'PRICE_HO_LO', 4: 'PRICE_HC_LC'})

# enum ENUM_ALERT_CANDLE
ALERT_PREVIOUS_CANDLE = 0
ALERT_CURRENT_CANDLE = 1
_enum('ENUM_ALERT_CANDLE', {0: 'ALERT_PREVIOUS_CANDLE', 1: 'ALERT_CURRENT_CANDLE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpTimeframe = _input('InpTimeframe', PERIOD_CURRENT)  # Timeframe
PriceType = _input('PriceType', PRICE_HH_LL)
Shift = _input('Shift', 0)
IsShowResistanceSpan = _input('IsShowResistanceSpan', True)  # Show Resistance Span
IsShowSupportSpan = _input('IsShowSupportSpan', True)  # Show Support Span
AlertCandle = _input('AlertCandle', ALERT_PREVIOUS_CANDLE)  # Alert Candle
IsAlertMidLineBullishCrossing = _input('IsAlertMidLineBullishCrossing', True)  # Alert About Bullish Crossing of Mid Line
IsAlertMidLineBearishCrossing = _input('IsAlertMidLineBearishCrossing', True)  # Alert About Bearish Crossing of Mid Line
IsAlertCandleCloseInsideResistance = _input('IsAlertCandleCloseInsideResistance', True)  # Alert About Candle Close Inside Resistance
IsAlertCandleCloseInsideSupport = _input('IsAlertCandleCloseInsideSupport', True)  # Alert About Candle Close Inside Support
IsShowAlert = _input('IsShowAlert', False)  # Show Alert
IsSendEmail = _input('IsSendEmail', False)  # Send Email
IsSendNotification = _input('IsSendNotification', False)  # Send Notification
UpBuffer = Arr(0, 0.0)
DownBuffer = Arr(0, 0.0)
ResistanceBuffer = Arr(0, 0.0)
SupportBuffer = Arr(0, 0.0)
ResistanceFillingBuffer = Arr(0, 0.0)
SupportFillingBuffer = Arr(0, 0.0)
MidBuffer = Arr(0, 0.0)
ResistanceFillingAddBuffer = Arr(0, 0.0)
SupportFillingAddBuffer = Arr(0, 0.0)
Timeframe = 0  # Timeframe of operation
deltaHighTF = 0  # Difference in candles count from the higher timeframe
IsMidLineBullishCrossing = False  # Variable for storing that it is bullish crossing of mid line
IsMidLineBearishCrossing = False  # Variable for storing that it is bearish crossing of mid line
IsCandleCloseInsideResistance = False  # Variable for storing that candle closes inside resistance
IsCandleCloseInsideSupport = False  # Variable for storing that candle closes inside support
MidLineBullishCrossingAlertMessage = ""  # Message for alerting that it is bullish crossing of mid line
MidLineBearishCrossingAlertMessage = ""  # Message for alerting that it is bearish crossing of mid line
CandleCloseInsideResistanceAlertMessage = ""  # Message for alerting that candle closes inside resistance
CandleCloseInsideSupportAlertMessage = ""  # Message for alerting that candle closes inside support
RatesTotal = 0
PrevCalculated = 0
AlertPrefix = ""

def OnInit():
    global AlertPrefix, CandleCloseInsideResistanceAlertMessage, CandleCloseInsideSupportAlertMessage, IsCandleCloseInsideResistance, IsCandleCloseInsideSupport, IsMidLineBearishCrossing, IsMidLineBullishCrossing, MidLineBearishCrossingAlertMessage, MidLineBullishCrossingAlertMessage, PrevCalculated, RatesTotal, Timeframe, deltaHighTF
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DownBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, MidBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ResistanceBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, SupportBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ResistanceFillingBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ResistanceFillingAddBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, SupportFillingBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, SupportFillingAddBuffer, INDICATOR_CALCULATIONS)
    for i in range(0, 9):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, InpPeriod - 1 + Shift)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, False)
    ArraySetAsSeries(DownBuffer, False)
    ArraySetAsSeries(MidBuffer, False)
    ArraySetAsSeries(ResistanceBuffer, False)
    ArraySetAsSeries(SupportBuffer, False)
    ArraySetAsSeries(ResistanceFillingBuffer, False)
    ArraySetAsSeries(SupportFillingBuffer, False)
    ArraySetAsSeries(ResistanceFillingAddBuffer, False)
    ArraySetAsSeries(SupportFillingAddBuffer, False)
    MidLineBullishCrossingAlertMessage = 'Bullish Crossing of Mid Line'
    MidLineBearishCrossingAlertMessage = 'Bearish Crossing of Mid Line'
    CandleCloseInsideResistanceAlertMessage = 'Candle Close Inside Resistance'
    CandleCloseInsideSupportAlertMessage = 'Candle Close Inside Support'
    IsMidLineBullishCrossing = False
    IsMidLineBearishCrossing = False
    IsCandleCloseInsideResistance = False
    IsCandleCloseInsideSupport = False
    RatesTotal = 0
    PrevCalculated = 0
    Timeframe = InpTimeframe
    if InpTimeframe < Period():
        Timeframe = Period()
    AlertPrefix = Symbol() + ' @ ' + EnumToString(Period(), 'ENUM_TIMEFRAMES')
    if Timeframe != Period():
        AlertPrefix += ' (' + EnumToString(Timeframe, 'ENUM_TIMEFRAMES') + ')'
    StringReplace(_GlobRef(globals(), 'AlertPrefix'), 'PERIOD_', '')
    deltaHighTF = 0
    if PeriodSeconds(Timeframe) > PeriodSeconds():
        deltaHighTF = _idiv(PeriodSeconds(Timeframe), PeriodSeconds())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global PrevCalculated, RatesTotal
    if rates_total < InpPeriod:
        return 0
    buffer = Arr(0, 0.0)
    toCopy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        toCopy = rates_total
    else:
        toCopy = rates_total - prev_calculated
        if prev_calculated > 0:
            toCopy += 1
    if CopyClose(Symbol(), Timeframe, 0, toCopy, buffer) <= 0:
        return 0
    RatesTotal = rates_total
    PrevCalculated = prev_calculated
    pos = prev_calculated - 1 - deltaHighTF
    startIndex = InpPeriod - 1 + Shift
    if pos < startIndex:
        for i in range(0, startIndex):
            UpBuffer[i] = EMPTY_VALUE
            DownBuffer[i] = EMPTY_VALUE
            ResistanceBuffer[i] = EMPTY_VALUE
            SupportBuffer[i] = EMPTY_VALUE
            MidBuffer[i] = EMPTY_VALUE
            ResistanceFillingBuffer[i] = EMPTY_VALUE
            SupportFillingBuffer[i] = EMPTY_VALUE
            ResistanceFillingAddBuffer[i] = EMPTY_VALUE
            SupportFillingAddBuffer[i] = EMPTY_VALUE
        pos = startIndex
    for i in range(pos, rates_total):
        index = rates_total - 1 - i + Shift
        UpBuffer[i] = GetUpLineValue(index)
        DownBuffer[i] = GetDownLineValue(index)
        ResistanceBuffer[i] = GetResistanceValue(index)
        if IsShowResistanceSpan:
            ResistanceFillingAddBuffer[i] = ResistanceBuffer[i]
            ResistanceFillingBuffer[i] = UpBuffer[i]
        else:
            ResistanceFillingAddBuffer[i] = EMPTY_VALUE
            ResistanceFillingBuffer[i] = EMPTY_VALUE
            ResistanceBuffer[i] = EMPTY_VALUE
        SupportBuffer[i] = GetSupportValue(index)
        if IsShowSupportSpan:
            SupportFillingAddBuffer[i] = DownBuffer[i]
            SupportFillingBuffer[i] = SupportBuffer[i]
        else:
            SupportFillingAddBuffer[i] = EMPTY_VALUE
            SupportFillingBuffer[i] = EMPTY_VALUE
            SupportBuffer[i] = EMPTY_VALUE
        MidBuffer[i] = (UpBuffer[i] + DownBuffer[i]) / 2
    HandleAlerts()
    return rates_total

def GetUpLineValue(index):
    shift = iBarShift(Symbol(), Timeframe, iTime(Symbol(), PERIOD_CURRENT, index))
    _sw1 = PriceType
    if _sw1 == PRICE_HH_LL:
        return iHigh(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift))
    elif _sw1 == PRICE_AVER_HHHO_LLLO:
        return (iHigh(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift)) + iOpen(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_OPEN, InpPeriod, shift))) / 2
    elif _sw1 == PRICE_AVER_HHHC_LLLC:
        return (iHigh(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift)) + iClose(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_CLOSE, InpPeriod, shift))) / 2
    elif _sw1 == PRICE_HO_LO:
        return iOpen(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_OPEN, InpPeriod, shift))
    elif _sw1 == PRICE_HC_LC:
        return iClose(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_CLOSE, InpPeriod, shift))
    else:
        return EMPTY_VALUE

def GetDownLineValue(index):
    shift = iBarShift(Symbol(), Timeframe, iTime(Symbol(), PERIOD_CURRENT, index))
    _sw2 = PriceType
    if _sw2 == PRICE_HH_LL:
        return iLow(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift))
    elif _sw2 == PRICE_AVER_HHHO_LLLO:
        return (iLow(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift)) + iOpen(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_OPEN, InpPeriod, shift))) / 2
    elif _sw2 == PRICE_AVER_HHHC_LLLC:
        return (iLow(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift)) + iClose(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_CLOSE, InpPeriod, shift))) / 2
    elif _sw2 == PRICE_HO_LO:
        return iOpen(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_OPEN, InpPeriod, shift))
    elif _sw2 == PRICE_HC_LC:
        return iClose(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_CLOSE, InpPeriod, shift))
    else:
        return EMPTY_VALUE

def GetResistanceValue(index):
    shift = iBarShift(Symbol(), Timeframe, iTime(Symbol(), PERIOD_CURRENT, index))
    _sw3 = PriceType
    if _sw3 == PRICE_HH_LL:
        return iLow(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift))
    elif _sw3 == PRICE_AVER_HHHO_LLLO:
        return (iLow(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift)) + iOpen(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_OPEN, InpPeriod, shift))) / 2
    elif _sw3 == PRICE_AVER_HHHC_LLLC:
        return (iLow(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift)) + iClose(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_CLOSE, InpPeriod, shift))) / 2
    elif _sw3 in (PRICE_HO_LO, PRICE_HC_LC):
        return iLow(Symbol(), Timeframe, iHighest(Symbol(), Timeframe, MODE_LOW, InpPeriod, shift))
    else:
        return EMPTY_VALUE

def GetSupportValue(index):
    shift = iBarShift(Symbol(), Timeframe, iTime(Symbol(), PERIOD_CURRENT, index))
    _sw4 = PriceType
    if _sw4 == PRICE_HH_LL:
        return iHigh(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift))
    elif _sw4 == PRICE_AVER_HHHO_LLLO:
        return (iHigh(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift)) + iOpen(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_OPEN, InpPeriod, shift))) / 2
    elif _sw4 == PRICE_AVER_HHHC_LLLC:
        return (iHigh(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift)) + iClose(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_CLOSE, InpPeriod, shift))) / 2
    elif _sw4 in (PRICE_HO_LO, PRICE_HC_LC):
        return iHigh(Symbol(), Timeframe, iLowest(Symbol(), Timeframe, MODE_HIGH, InpPeriod, shift))
    else:
        return EMPTY_VALUE

def HandleAlerts():
    global IsCandleCloseInsideResistance, IsCandleCloseInsideSupport, IsMidLineBearishCrossing, IsMidLineBullishCrossing
    if ((not IsShowAlert) and (not IsSendEmail)) and (not IsSendNotification):
        return
    if not PrevCalculated:
        RefreshGlobalVariables()
    elif PrevCalculated != RatesTotal:
        ResetGlobalVariables()
    isMidLineBullishCrossingMessage = ""
    isMidLineBearishCrossingMessage = ""
    isCandleCloseInsideResistanceMessage = ""
    isCandleCloseInsideSupportMessage = ""
    if (IsAlertMidLineBullishCrossing and (not IsMidLineBullishCrossing)) and HasMidLineBullishCrossing():
        isMidLineBullishCrossingMessage = MidLineBullishCrossingAlertMessage
        IsMidLineBullishCrossing = True
    if (IsAlertMidLineBearishCrossing and (not IsMidLineBearishCrossing)) and HasMidLineBearishCrossing():
        isMidLineBearishCrossingMessage = MidLineBearishCrossingAlertMessage
        IsMidLineBearishCrossing = True
    if (IsAlertCandleCloseInsideResistance and (not IsCandleCloseInsideResistance)) and HasCandleCloseInsideResistance():
        isCandleCloseInsideResistanceMessage = CandleCloseInsideResistanceAlertMessage
        IsCandleCloseInsideResistance = True
    if (IsAlertCandleCloseInsideSupport and (not IsCandleCloseInsideSupport)) and HasCandleCloseInsideSupport():
        isCandleCloseInsideSupportMessage = CandleCloseInsideSupportAlertMessage
        IsCandleCloseInsideSupport = True
    IssueAlerts(isMidLineBullishCrossingMessage)
    IssueAlerts(isMidLineBearishCrossingMessage)
    IssueAlerts(isCandleCloseInsideResistanceMessage)
    IssueAlerts(isCandleCloseInsideSupportMessage)

def IssueAlerts(message):
    if message == "":
        return
    if IsShowAlert:
        native_alert = Box(message)
        if Timeframe != Period():
            native_alert.v = '(' + EnumToString(Timeframe, 'ENUM_TIMEFRAMES') + ') ' + native_alert.v
        StringReplace(native_alert, 'PERIOD_', '')
        Alert(native_alert.v)
    message = AlertPrefix + ': ' + message
    if IsSendEmail:
        SendMail('Donchian Ultimate Alert', message)
    if IsSendNotification:
        SendNotification(message)

def HasMidLineBullishCrossing():
    shift = (1 if (AlertCandle == ALERT_PREVIOUS_CANDLE) else 0)
    index = RatesTotal - 1 - shift
    return iOpen(Symbol(), PERIOD_CURRENT, shift) < MidBuffer[index] and iClose(Symbol(), PERIOD_CURRENT, shift) > MidBuffer[index]

def HasMidLineBearishCrossing():
    shift = (1 if (AlertCandle == ALERT_PREVIOUS_CANDLE) else 0)
    index = RatesTotal - 1 - shift
    return iOpen(Symbol(), PERIOD_CURRENT, shift) > MidBuffer[index] and iClose(Symbol(), PERIOD_CURRENT, shift) < MidBuffer[index]

def HasCandleCloseInsideResistance():
    shift = (1 if (AlertCandle == ALERT_PREVIOUS_CANDLE) else 0)
    index = RatesTotal - 1 - shift
    return (iOpen(Symbol(), PERIOD_CURRENT, shift) < ResistanceBuffer[index] and iClose(Symbol(), PERIOD_CURRENT, shift) > ResistanceBuffer[index]) and iClose(Symbol(), PERIOD_CURRENT, shift) < UpBuffer[index]

def HasCandleCloseInsideSupport():
    shift = (1 if (AlertCandle == ALERT_PREVIOUS_CANDLE) else 0)
    index = RatesTotal - 1 - shift
    return (iOpen(Symbol(), PERIOD_CURRENT, shift) > SupportBuffer[index] and iClose(Symbol(), PERIOD_CURRENT, shift) < SupportBuffer[index]) and iClose(Symbol(), PERIOD_CURRENT, shift) > DownBuffer[index]

def ResetGlobalVariables():
    global IsCandleCloseInsideResistance, IsCandleCloseInsideSupport, IsMidLineBearishCrossing, IsMidLineBullishCrossing
    IsMidLineBullishCrossing = False
    IsMidLineBearishCrossing = False
    IsCandleCloseInsideResistance = False
    IsCandleCloseInsideSupport = False

def RefreshGlobalVariables():
    global IsCandleCloseInsideResistance, IsCandleCloseInsideSupport, IsMidLineBearishCrossing, IsMidLineBullishCrossing
    IsMidLineBullishCrossing = HasMidLineBullishCrossing()
    IsMidLineBearishCrossing = HasMidLineBearishCrossing()
    IsCandleCloseInsideResistance = HasCandleCloseInsideResistance()
    IsCandleCloseInsideSupport = HasCandleCloseInsideSupport()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianUltimate(_MQL5Indicator):
    name = 'Donchian Ultimate'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe
        'PriceType': _Choice({0: 'Highest High (Lowest Low)', 1: 'Average Highest High, Highest Open (Lowest Low, Lowest Open)', 2: 'Average Highest High, Highest Close (Lowest Low, Lowest Close)', 3: 'Highest Open (Lowest Open)', 4: 'Highest Close (Lowest Close)'}, default=0),
        'Shift': 0,
        'IsShowResistanceSpan': True,  # Show Resistance Span
        'IsShowSupportSpan': True,  # Show Support Span
        'AlertCandle': _Choice({0: 'Previous', 1: 'Current'}, default=0),  # Alert Candle
        'IsAlertMidLineBullishCrossing': True,  # Alert About Bullish Crossing of Mid Line
        'IsAlertMidLineBearishCrossing': True,  # Alert About Bearish Crossing of Mid Line
        'IsAlertCandleCloseInsideResistance': True,  # Alert About Candle Close Inside Resistance
        'IsAlertCandleCloseInsideSupport': True,  # Alert About Candle Close Inside Support
        'IsShowAlert': False,  # Show Alert
        'IsSendEmail': False,  # Send Email
        'IsSendNotification': False,  # Send Notification
    }

