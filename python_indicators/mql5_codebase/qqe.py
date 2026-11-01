"""QQE — converted from MQL5: MQL5 Indicators/QQE Quantitative Qualitative Estimation MT5/QQE.mq5

QQE - Qualitative Quantitative Estimation.
Calculated as two indicators:
1) MA on RSI
2) Difference of MA on RSI and MA of MA of ATR of MA of RSI
The signal for buy is when blue line crosses level 50 from below after crossing the yellow line from below.
The signal for sell is when blue line crosses level 50 from above after crossing the yellow line from above.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.03', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [65535]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'RSI MA', 2: 'Smoothed'}, 'levels': [50.0], 'description': ['QQE - Qualitative Quantitative Estimation.', 'Calculated as two indicators:', '1) MA on RSI', '2) Difference of MA on RSI and MA of MA of ATR of MA of RSI', 'The signal for buy is when blue line crosses level 50 from below after crossing the yellow line from below.', 'The signal for sell is when blue line crosses level 50 from above after crossing the yellow line from above.'], 'name': 'QQE', 'source': 'MQL5 Indicators/QQE Quantitative Qualitative Estimation MT5/QQE.mq5', 'folder': 'QQE Quantitative Qualitative Estimation MT5', 'inputs': [{'mql': 'SF', 'py': 'SF', 'param': 'SF', 'type': 'int', 'default': 5, 'label': 'Smoothing Factor', 'sinput': False}, {'mql': 'AlertOnCrossover', 'py': 'AlertOnCrossover', 'param': 'AlertOnCrossover', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnLevel', 'py': 'AlertOnLevel', 'param': 'AlertOnLevel', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertLevel', 'py': 'AlertLevel', 'param': 'AlertLevel', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'ArrowsOnCrossover', 'py': 'ArrowsOnCrossover', 'param': 'ArrowsOnCrossover', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'CrossoverUpArrow', 'py': 'CrossoverUpArrow', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'CrossoverDnArrow', 'py': 'CrossoverDnArrow', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'ArrowsOnLevel', 'py': 'ArrowsOnLevel', 'param': 'ArrowsOnLevel', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'LevelUpArrow', 'py': 'LevelUpArrow', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'LevelDnArrow', 'py': 'LevelDnArrow', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'NativeAlerts', 'py': 'NativeAlerts', 'param': 'NativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlerts', 'py': 'EmailAlerts', 'param': 'EmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'NotificationAlerts', 'py': 'NotificationAlerts', 'param': 'NotificationAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'UpperTimeframe', 'py': 'UpperTimeframe', 'param': 'UpperTimeframe', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'QQE-', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SF = _input('SF', 5)  # Smoothing Factor
AlertOnCrossover = _input('AlertOnCrossover', False)
AlertOnLevel = _input('AlertOnLevel', False)
AlertLevel = _input('AlertLevel', 50)
ArrowsOnCrossover = _input('ArrowsOnCrossover', True)
CrossoverUpArrow = _input('CrossoverUpArrow', clrGreen)
CrossoverDnArrow = _input('CrossoverDnArrow', clrRed)
ArrowsOnLevel = _input('ArrowsOnLevel', True)
LevelUpArrow = _input('LevelUpArrow', clrGreen)
LevelDnArrow = _input('LevelDnArrow', clrRed)
NativeAlerts = _input('NativeAlerts', False)
EmailAlerts = _input('EmailAlerts', False)
NotificationAlerts = _input('NotificationAlerts', False)
UpperTimeframe = _input('UpperTimeframe', PERIOD_CURRENT)
ObjectPrefix = _input('ObjectPrefix', 'QQE-')
RSI_Period = 14
Wilders_Period = 0
StartBar = 0
LastAlertTimeCross = 0
LastAlertTimeLevel = 0
QQE_handle = 0
TrLevelSlow = Arr(0, 0.0)
AtrRsi = Arr(0, 0.0)
MaAtrRsi = Arr(0, 0.0)
Rsi = Arr(0, 0.0)
RsiMa = Arr(0, 0.0)
MaMaAtrRsi = Arr(0, 0.0)
myRSI = 0

def OnInit():
    global LastAlertTimeCross, LastAlertTimeLevel, QQE_handle, StartBar, Wilders_Period, myRSI
    LastAlertTimeCross = 0
    LastAlertTimeLevel = 0
    Wilders_Period = (RSI_Period * 2) - 1
    StartBar = MathMax(SF, Wilders_Period)
    SetIndexBuffer(0, RsiMa, INDICATOR_DATA)
    SetIndexBuffer(1, TrLevelSlow, INDICATOR_DATA)
    SetIndexBuffer(2, AtrRsi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, MaAtrRsi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, Rsi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, MaMaAtrRsi, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(RsiMa, True)
    ArraySetAsSeries(TrLevelSlow, True)
    ArraySetAsSeries(AtrRsi, True)
    ArraySetAsSeries(MaAtrRsi, True)
    ArraySetAsSeries(Rsi, True)
    ArraySetAsSeries(MaMaAtrRsi, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBar)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    myRSI = iRSI(Symbol(), Period(), RSI_Period, PRICE_CLOSE)
    if PeriodSeconds(UpperTimeframe) > PeriodSeconds():
        IndicatorFileName = MQLInfoString(MQL_PROGRAM_NAME)
        QQE_handle = iCustom(Symbol(), UpperTimeframe, IndicatorFileName, SF, False, False, AlertLevel, False, LevelUpArrow, LevelDnArrow, False, CrossoverUpArrow, CrossoverDnArrow, False, False, False, UpperTimeframe, ObjectPrefix)
    else:
        QQE_handle = INVALID_HANDLE
        if PeriodSeconds(UpperTimeframe) < PeriodSeconds():
            Print('UpperTimeframe should be above the current timeframe.')
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE(' + IntegerToString(SF) + ')')

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), ObjectPrefix)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    global LastAlertTimeCross, LastAlertTimeLevel
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    if rates_total <= StartBar:
        return 0
    counted = prev_calculated - 1
    if counted < 1:
        for i in range(rates_total - StartBar, rates_total):
            TrLevelSlow[i] = 0.0
            AtrRsi[i] = 0.0
            MaAtrRsi[i] = 0.0
            Rsi[i] = 0.0
            RsiMa[i] = 0.0
            MaMaAtrRsi[i] = 0.0
    rec_only_latest_upper_bar = False
    if counted > 0 and QQE_handle != INVALID_HANDLE:
        counted = prev_calculated - _idiv(PeriodSeconds(UpperTimeframe), PeriodSeconds())
        rec_only_latest_upper_bar = True
    else:
        counted = rates_total - counted - 1
        if counted > (rates_total - StartBar - 1):
            counted = rates_total - StartBar - 1
    if QQE_handle == INVALID_HANDLE:
        if CopyBuffer(myRSI, 0, 0, counted + 2, Rsi) != (counted + 2):
            return 0
        CalculateEMA(counted + 1, SF, Rsi, RsiMa)
        for i in range(counted, 0 - 1, -1):
            AtrRsi[i] = MathAbs(RsiMa[i + 1] - RsiMa[i])
    else:
        for i in range(counted, 0 - 1, -1):
            buf = Arr(1, 0.0, dyn=False)
            if rec_only_latest_upper_bar:
                if Time[i] < iTime(Symbol(), UpperTimeframe, 0):
                    continue
            n = CopyBuffer(QQE_handle, 0, _DT(Time[i]), 1, buf)
            if n == 1:
                RsiMa[i] = buf[0]
            else:
                return prev_calculated
    i = counted + 1
    tr = 0.0
    rsi1 = 0.0
    if QQE_handle == INVALID_HANDLE:
        CalculateEMA(counted, Wilders_Period, AtrRsi, MaAtrRsi)
        tr = TrLevelSlow[i]
        rsi1 = RsiMa[i]
        CalculateEMA(counted, Wilders_Period, MaAtrRsi, MaMaAtrRsi)
    while i > 0:
        i -= 1
        if QQE_handle == INVALID_HANDLE:
            rsi0 = RsiMa[i]
            dar = MaMaAtrRsi[i] * 4.236
            dv = tr
            if rsi0 < tr:
                tr = rsi0 + dar
                if rsi1 < dv and tr > dv:
                    tr = dv
            elif rsi0 > tr:
                tr = rsi0 - dar
                if rsi1 > dv and tr < dv:
                    tr = dv
            TrLevelSlow[i] = tr
            rsi1 = rsi0
        else:
            buf = Arr(1, 0.0, dyn=False)
            if rec_only_latest_upper_bar:
                if Time[i] < iTime(Symbol(), UpperTimeframe, 0):
                    continue
            n = CopyBuffer(QQE_handle, 1, _DT(Time[i]), 1, buf)
            if n == 1:
                TrLevelSlow[i] = buf[0]
            else:
                return prev_calculated
        if i > 0 or QQE_handle != INVALID_HANDLE:
            cur_i = i
            pre_i = i + 1
            if QQE_handle != INVALID_HANDLE and i < _idiv(PeriodSeconds(UpperTimeframe), PeriodSeconds()):
                customIndex = iBarShift(Symbol(), UpperTimeframe, Time[cur_i])
                cur_i += 1
                while cur_i < rates_total and iBarShift(Symbol(), UpperTimeframe, Time[cur_i]) == customIndex:
                    cur_i += 1
                if cur_i == rates_total:
                    return prev_calculated
                customIndex = iBarShift(Symbol(), UpperTimeframe, Time[cur_i])
                pre_i = cur_i + 1
                while pre_i < rates_total and iBarShift(Symbol(), UpperTimeframe, Time[pre_i]) == customIndex:
                    pre_i += 1
                if pre_i == rates_total:
                    return prev_calculated
                cur_i = pre_i - 1
            if ArrowsOnCrossover:
                name = ObjectPrefix + 'CArrow' + TimeToString(Time[cur_i])
                if RsiMa[pre_i] < TrLevelSlow[pre_i] and RsiMa[cur_i] > TrLevelSlow[cur_i]:
                    ObjectCreate(ChartID(), name, OBJ_ARROW_THUMB_UP, 0, Time[cur_i], Low[cur_i] - (1 * Point()))
                    ObjectSetInteger(ChartID(), name, OBJPROP_COLOR, LevelUpArrow)
                    ObjectSetInteger(ChartID(), name, OBJPROP_ANCHOR, ANCHOR_TOP)
                    ObjectSetInteger(ChartID(), name, OBJPROP_WIDTH, 5)
                elif RsiMa[pre_i] > TrLevelSlow[pre_i] and RsiMa[cur_i] < TrLevelSlow[cur_i]:
                    ObjectCreate(ChartID(), name, OBJ_ARROW_THUMB_DOWN, 0, Time[cur_i], High[cur_i] + (1 * Point()))
                    ObjectSetInteger(ChartID(), name, OBJPROP_COLOR, LevelDnArrow)
                    ObjectSetInteger(ChartID(), name, OBJPROP_ANCHOR, ANCHOR_BOTTOM)
                    ObjectSetInteger(ChartID(), name, OBJPROP_WIDTH, 5)
            if ArrowsOnLevel:
                name = ObjectPrefix + 'LArrow' + TimeToString(Time[cur_i])
                if RsiMa[pre_i] < AlertLevel and RsiMa[cur_i] > AlertLevel:
                    ObjectCreate(ChartID(), name, OBJ_ARROW_UP, 0, Time[cur_i], Low[cur_i] - (1 * Point()))
                    ObjectSetInteger(ChartID(), name, OBJPROP_COLOR, LevelUpArrow)
                    ObjectSetInteger(ChartID(), name, OBJPROP_ANCHOR, ANCHOR_TOP)
                    ObjectSetInteger(ChartID(), name, OBJPROP_WIDTH, 5)
                elif RsiMa[pre_i] > AlertLevel and RsiMa[cur_i] < AlertLevel:
                    ObjectCreate(ChartID(), name, OBJ_ARROW_DOWN, 0, Time[cur_i], High[cur_i] + (1 * Point()))
                    ObjectSetInteger(ChartID(), name, OBJPROP_COLOR, LevelDnArrow)
                    ObjectSetInteger(ChartID(), name, OBJPROP_ANCHOR, ANCHOR_BOTTOM)
                    ObjectSetInteger(ChartID(), name, OBJPROP_WIDTH, 5)
    if ((not NativeAlerts) and (not EmailAlerts)) and (not NotificationAlerts):
        return rates_total
    if (not AlertOnCrossover) and (not AlertOnLevel):
        return rates_total
    pre_i = 2
    if QQE_handle != INVALID_HANDLE:
        cnt = 1
        customIndex = iBarShift(Symbol(), UpperTimeframe, Time[0])
        while cnt < rates_total and iBarShift(Symbol(), UpperTimeframe, Time[cnt]) == customIndex:
            cnt += 1
        i = cnt
        customIndex = iBarShift(Symbol(), UpperTimeframe, Time[cnt])
        cnt += 1
        while cnt < rates_total and iBarShift(Symbol(), UpperTimeframe, Time[cnt]) == customIndex:
            cnt += 1
        pre_i = cnt
    else:
        i = 1
    if AlertOnLevel:
        if (LastAlertTimeLevel > 0 and ((RsiMa[pre_i] < AlertLevel and RsiMa[i] > AlertLevel) or (RsiMa[pre_i] > AlertLevel and RsiMa[i] < AlertLevel))) and Time[i - 1] > LastAlertTimeLevel:
            TextNative = IntegerToString(AlertLevel) + ' level Cross '
            if RsiMa[pre_i] > AlertLevel and RsiMa[i] < AlertLevel:
                TextNative += 'Down'
            else:
                TextNative += 'Up'
            Text = 'QQE ' + Symbol() + ', TF: ' + TimeframeToString(Period()) + ' ' + TextNative
            DoAlerts(Text, TextNative)
            LastAlertTimeLevel = Time[i - 1]
    if AlertOnCrossover:
        if (LastAlertTimeCross > 0 and ((RsiMa[pre_i] < TrLevelSlow[pre_i] and RsiMa[i] > TrLevelSlow[i]) or (RsiMa[pre_i] > TrLevelSlow[pre_i] and RsiMa[i] < TrLevelSlow[i]))) and Time[i - 1] > LastAlertTimeCross:
            TextNative = 'RSI MA crossed Smoothed Line from '
            if RsiMa[pre_i] > TrLevelSlow[pre_i] and RsiMa[i] < TrLevelSlow[i]:
                TextNative += 'above.'
            else:
                TextNative += 'below.'
            Text = 'QQE ' + Symbol() + ', TF: ' + TimeframeToString(Period()) + ' ' + TextNative
            DoAlerts(Text, TextNative)
            LastAlertTimeCross = Time[i - 1]
    if LastAlertTimeLevel == 0:
        LastAlertTimeLevel = Time[0]
    if LastAlertTimeCross == 0:
        LastAlertTimeCross = Time[0]
    return rates_total

def DoAlerts(Text, TextNative):
    if NativeAlerts:
        Alert(TextNative)
    if EmailAlerts:
        SendMail(Text, Text)
    if NotificationAlerts:
        SendNotification(Text)

def TimeframeToString(P):
    return StringSubstr(EnumToString(P, 'ENUM_TIMEFRAMES'), 7)

def CalculateEMA(begin, period, price, result):
    SmoothFactor = _fdiv(2.0, 1.0 + period)
    for i in range(begin, 0 - 1, -1):
        if price[i] == EMPTY_VALUE:
            result[i] = 0.0
        else:
            result[i] = (price[i] * SmoothFactor) + (result[i + 1] * (1.0 - SmoothFactor))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class QQE(_MQL5Indicator):
    name = 'QQE'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SF': 5,  # Smoothing Factor
        'AlertOnCrossover': False,
        'AlertOnLevel': False,
        'AlertLevel': 50,
        'ArrowsOnCrossover': True,
        'ArrowsOnLevel': True,
        'NativeAlerts': False,
        'EmailAlerts': False,
        'NotificationAlerts': False,
        'UpperTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
    }

