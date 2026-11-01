"""EasyTrendVisualizer — converted from MQL5: MQL5 Indicators/Easy Trend Visualizer MT5/EasyTrendVisualizer.mq5

Easy Trend Visualizer - displays trend strength, direction, and support and resistance levels.
Version: 1.12

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.12', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 11, 2: 5, 3: 5, 4: 1}, 'colors': {1: [255, 11829830], 2: [65280], 3: [65280], 4: [8519755]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {}, 'levels': [], 'description': ['Easy Trend Visualizer - displays trend strength, direction, and support and resistance levels.'], 'name': 'EasyTrendVisualizer', 'source': 'MQL5 Indicators/Easy Trend Visualizer MT5/EasyTrendVisualizer.mq5', 'folder': 'Easy Trend Visualizer MT5', 'inputs': [{'mql': 'ADXperiod1', 'py': 'ADXperiod1', 'param': 'ADXperiod1', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ADXperiod2', 'py': 'ADXperiod2', 'param': 'ADXperiod2', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ADXperiod3', 'py': 'ADXperiod3', 'param': 'ADXperiod3', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'UseAlertHorizontalLine', 'py': 'UseAlertHorizontalLine', 'param': 'UseAlertHorizontalLine', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'UseAlertUpDownArrows', 'py': 'UseAlertUpDownArrows', 'param': 'UseAlertUpDownArrows', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'UseAlertHorizontalLineCrossCurrent', 'py': 'UseAlertHorizontalLineCrossCurrent', 'param': 'UseAlertHorizontalLineCrossCurrent', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'UseAlertHorizontalLineCrossPrevious', 'py': 'UseAlertHorizontalLineCrossPrevious', 'param': 'UseAlertHorizontalLineCrossPrevious', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'NumberPHLtoTrack', 'py': 'NumberPHLtoTrack', 'param': 'NumberPHLtoTrack', 'type': 'int', 'default': 0, 'label': 'How many previous horizontal lines to track for alert purposes?', 'sinput': False}, {'mql': 'IgnorePHLShorterThan', 'py': 'IgnorePHLShorterThan', 'param': 'IgnorePHLShorterThan', 'type': 'int', 'default': 2, 'label': 'Ignore previous horizontal lines shorter than', 'sinput': False}, {'mql': 'PHLC_Arrow_Color', 'py': 'PHLC_Arrow_Color', 'param': None, 'type': 'color', 'default': 1993170, 'label': '', 'sinput': False}, {'mql': 'CHLC_Arrow_Color', 'py': 'CHLC_Arrow_Color', 'param': None, 'type': 'color', 'default': 2237106, 'label': '', 'sinput': False}, {'mql': 'NativeAlerts', 'py': 'NativeAlerts', 'param': 'NativeAlerts', 'type': 'bool', 'default': False, 'label': 'Use pop-up alerts?', 'sinput': False}, {'mql': 'SendEmails', 'py': 'SendEmails', 'param': 'SendEmails', 'type': 'bool', 'default': False, 'label': 'Send alerts via email?', 'sinput': False}, {'mql': 'SendNotifications', 'py': 'SendNotifications', 'param': 'SendNotifications', 'type': 'bool', 'default': False, 'label': 'Send alerts via push notifications?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXperiod1 = _input('ADXperiod1', 10)
ADXperiod2 = _input('ADXperiod2', 14)
ADXperiod3 = _input('ADXperiod3', 20)
UseAlertHorizontalLine = _input('UseAlertHorizontalLine', False)
UseAlertUpDownArrows = _input('UseAlertUpDownArrows', False)
UseAlertHorizontalLineCrossCurrent = _input('UseAlertHorizontalLineCrossCurrent', False)
UseAlertHorizontalLineCrossPrevious = _input('UseAlertHorizontalLineCrossPrevious', False)
NumberPHLtoTrack = _input('NumberPHLtoTrack', 0)  # How many previous horizontal lines to track for alert purposes?
IgnorePHLShorterThan = _input('IgnorePHLShorterThan', 2)  # Ignore previous horizontal lines shorter than
PHLC_Arrow_Color = _input('PHLC_Arrow_Color', clrChocolate)
CHLC_Arrow_Color = _input('CHLC_Arrow_Color', clrFireBrick)
NativeAlerts = _input('NativeAlerts', False)  # Use pop-up alerts?
SendEmails = _input('SendEmails', False)  # Send alerts via email?
SendNotifications = _input('SendNotifications', False)  # Send alerts via push notifications?
MxP = 0
MnP = 0
MdP = 0
was_alert_hl = EMPTY_VALUE  # Horizontal line
was_alert_au = EMPTY_VALUE  # Arrow up
was_alert_ad = EMPTY_VALUE  # Arrow down
was_alert_hlcross = 0  # Horizontal line cross
To = Arr(0, 0.0)
Tc = Arr(0, 0.0)
Color = Arr(0, 0.0)
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Ex = Arr(0, 0.0)
ADX1 = Arr(0, 0.0)
ADX2 = Arr(0, 0.0)
ADX3 = Arr(0, 0.0)
Last_Ex = Arr(0, 0.0)  # Buffer to hold previous "last line levels". Required for price/line alert because imaginary line cross also count.
was_alert_phlc = Arr(0, 0)  # Price crosses and closes above/below previous horizontal line.

def OnInit():
    global MdP, MnP, MxP
    MxP = MathMax(MathMax(ADXperiod1, ADXperiod2), ADXperiod3)
    MnP = MathMin(MathMin(ADXperiod1, ADXperiod2), ADXperiod3)
    if MxP == ADXperiod1:
        MdP = MathMax(ADXperiod2, ADXperiod3)
    elif MxP == ADXperiod2:
        MdP = MathMax(ADXperiod1, ADXperiod3)
    else:
        MdP = MathMax(ADXperiod2, ADXperiod1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ETV(' + IntegerToString(MnP) + '/' + IntegerToString(MdP) + '/' + IntegerToString(MxP) + ')')
    SetIndexBuffer(0, To, INDICATOR_DATA)
    SetIndexBuffer(1, Tc, INDICATOR_DATA)
    SetIndexBuffer(2, Color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, Up, INDICATOR_DATA)
    SetIndexBuffer(4, Dn, INDICATOR_DATA)
    SetIndexBuffer(5, Ex, INDICATOR_DATA)
    SetIndexBuffer(6, ADX1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ADX2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ADX3, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(To, True)
    ArraySetAsSeries(Tc, True)
    ArraySetAsSeries(Color, True)
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Dn, True)
    ArraySetAsSeries(Ex, True)
    ArraySetAsSeries(ADX1, True)
    ArraySetAsSeries(ADX2, True)
    ArraySetAsSeries(ADX3, True)
    PlotIndexSetInteger(1, PLOT_ARROW, 225)
    PlotIndexSetInteger(2, PLOT_ARROW, 226)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MxP)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, MxP)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, MxP)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, MxP + 1)
    PlotIndexSetString(1, PLOT_LABEL, 'Up')
    PlotIndexSetString(2, PLOT_LABEL, 'Down')
    PlotIndexSetString(3, PLOT_LABEL, 'End')
    ArrayResize(Last_Ex, PHLC_Arrow_Color)
    ArrayInitialize(Last_Ex, EMPTY_VALUE)
    ArrayResize(was_alert_phlc, PHLC_Arrow_Color)
    ArrayInitialize(was_alert_phlc, 0)

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'PHLCArrow_', -1, OBJ_ARROW)
    ObjectsDeleteAll(0, 'CHLCArrow_', -1, OBJ_ARROW)

def OnCalculate(rates_total, prev_calculated, Time, Open, high, low, Close, tick_volume, volume, spread):
    global was_alert_ad, was_alert_au, was_alert_hl, was_alert_hlcross
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Time, True)
    limit = rates_total - prev_calculated
    if prev_calculated == 0:
        limit -= MxP
    ADXBuffer1 = Arr(0, 0.0)
    ADXBuffer2 = Arr(0, 0.0)
    ADXBuffer3 = Arr(0, 0.0)
    ADXBuffer1_1 = Arr(0, 0.0)
    ADXBuffer1_2 = Arr(0, 0.0)
    myADX = iADX(None, 0, MnP)
    if CopyBuffer(myADX, MAIN_LINE, 0, rates_total, ADXBuffer1) != rates_total:
        return 0
    if CopyBuffer(myADX, PLUSDI_LINE, 0, rates_total, ADXBuffer1_1) != rates_total:
        return 0
    if CopyBuffer(myADX, MINUSDI_LINE, 0, rates_total, ADXBuffer1_2) != rates_total:
        return 0
    myADX = iADX(None, 0, MdP)
    if CopyBuffer(myADX, MAIN_LINE, 0, rates_total, ADXBuffer2) != rates_total:
        return 0
    myADX = iADX(None, 0, MxP)
    if CopyBuffer(myADX, MAIN_LINE, 0, rates_total, ADXBuffer3) != rates_total:
        return 0
    for i in range(rates_total - 1, 0 - 1, -1):
        ADX1[i] = ADXBuffer1[rates_total - i - 1]
        ADX2[i] = ADXBuffer2[rates_total - i - 1]
        ADX3[i] = ADXBuffer3[rates_total - i - 1]
    if prev_calculated == 0:
        limit -= 1
    if limit < 1:
        limit = 2
    for i in range(limit - 1, 0 - 1, -1):
        f1 = False
        f2 = False
        f3 = False
        To[i] = EMPTY_VALUE
        Tc[i] = EMPTY_VALUE
        Up[i] = EMPTY_VALUE
        Dn[i] = EMPTY_VALUE
        Ex[i] = EMPTY_VALUE
        k = i + 1
        if NumberPHLtoTrack > 0 and (i + 2) < rates_total:
            if (Ex[i + 1] == EMPTY_VALUE and Ex[i + 2] != EMPTY_VALUE) and Last_Ex[0] != Ex[i + 2]:
                length = 1
                for j in range(i + 3, rates_total):
                    if Ex[j] == EMPTY_VALUE:
                        break
                    length += 1
                if length >= IgnorePHLShorterThan:
                    for j in range(NumberPHLtoTrack - 1, 0 - 1, -1):
                        if Time[i + 2] < was_alert_phlc[j]:
                            break
                        if j == 0:
                            Last_Ex[j] = Ex[i + 2]
                            was_alert_phlc[j] = 0
                        else:
                            Last_Ex[j] = Last_Ex[j - 1]
                            was_alert_phlc[j] = was_alert_phlc[j - 1]
        if ADX1[k] < ADX1[i]:
            f1 = True
        if ADX2[k] < ADX2[i]:
            f2 = True
        if ADX3[k] < ADX3[i]:
            f3 = True
        if (((f1 and f2) and f3) and ADX1[i] > 35.0) and ADX2[i] > 30.0:
            di = ADXBuffer1_1[rates_total - i - 1] - ADXBuffer1_2[rates_total - i - 1]
            hi = MathMax(Open[i], Close[i])
            lo = MathMin(Open[i], Close[i])
            op = Open[i]
            if di > 0:
                To[i] = lo
                Tc[i] = hi
                if To[k] == EMPTY_VALUE:
                    Up[i] = op
                Color[i] = 1.0
            else:
                To[i] = hi
                Tc[i] = lo
                if To[k] == EMPTY_VALUE:
                    Dn[i] = op
                Color[i] = 0.0
        else:
            if To[k] != EMPTY_VALUE:
                Ex[i] = Close[i + 1]
            else:
                Ex[i] = Ex[k]
    if ((NativeAlerts or SendEmails) or SendNotifications) and (((UseAlertHorizontalLine or UseAlertUpDownArrows) or UseAlertHorizontalLineCrossCurrent) or UseAlertHorizontalLineCrossPrevious):
        DateTime = TimeToString(Time[0])
        PerStr = EnumToString(Period(), '')
        if UseAlertHorizontalLine:
            if (Ex[1] != EMPTY_VALUE and Ex[1] != was_alert_hl) and Ex[1] != Ex[2]:
                text = 'ETV - HL Start '
                if To[2] < Tc[2]:
                    text += 'After Uptrend'
                elif To[2] > Tc[2]:
                    text += 'After Downtrend'
                if NativeAlerts:
                    Alert(text)
                text += ' ' + Symbol() + ' @ ' + PerStr
                if SendEmails:
                    SendMail(text, text)
                if SendNotifications:
                    SendNotification(text)
                was_alert_hl = Ex[1]
        if UseAlertUpDownArrows:
            if Up[0] != 0 and Up[0] != was_alert_au:
                text = 'ETV - Arrow Up'
                if NativeAlerts:
                    Alert(text)
                text += ' ' + Symbol() + ' @ ' + PerStr
                if SendEmails:
                    SendMail(text, text)
                if SendNotifications:
                    SendNotification(text)
                was_alert_au = Up[0]
            if Dn[0] != 0 and Dn[0] != was_alert_ad:
                text = 'ETV - Arrow Down'
                if NativeAlerts:
                    Alert(text)
                text += ' ' + Symbol() + ' @ ' + PerStr
                if SendEmails:
                    SendMail(text, text)
                if SendNotifications:
                    SendNotification(text)
                was_alert_ad = Dn[0]
        if UseAlertHorizontalLineCrossCurrent:
            if ((Ex[1] != EMPTY_VALUE and Ex[2] != EMPTY_VALUE) and was_alert_hlcross != Time[1]) and ((Close[1] > Ex[1] and Open[1] <= Ex[1]) or (Close[1] <= Ex[1] and Open[1] > Ex[1])):
                text = 'ETV - Current HL Cross '
                if Open[1] < Close[1]:
                    text += 'Up'
                elif Open[1] > Close[1]:
                    text += 'Down'
                if NativeAlerts:
                    Alert(text)
                text += ' ' + Symbol() + ' @ ' + PerStr
                if SendEmails:
                    SendMail(text, text)
                if SendNotifications:
                    SendNotification(text)
                was_alert_hlcross = Time[1]
                obj_name = 'CHLCArrow_' + TimeToString(Time[1])
                ObjectCreate(0, obj_name, OBJ_ARROW, 0, Time[1], Ex[1])
                ObjectSetInteger(0, obj_name, OBJPROP_ARROWCODE, 200)
                ObjectSetInteger(0, obj_name, OBJPROP_COLOR, CHLC_Arrow_Color)
                desc = 'Price crossed: ' + DoubleToString(Ex[1], Digits()) + ' @ ' + PerStr
                ObjectSetString(0, obj_name, OBJPROP_TOOLTIP, desc)
                ObjectSetString(0, obj_name, OBJPROP_TEXT, desc)
                ObjectSetInteger(0, obj_name, OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name, OBJPROP_HIDDEN, False)
        if UseAlertHorizontalLineCrossPrevious and NumberPHLtoTrack > 0:
            DateTime = TimeToString(Time[1])
            CheckImaginaryLinesCrosses(DateTime, PerStr, Time, Open, Close)
    return rates_total

def CheckImaginaryLinesCrosses(DateTime, PerStr, Time, Open, Close):
    for i in range(0, NumberPHLtoTrack):
        if (Last_Ex[i] != EMPTY_VALUE and was_alert_phlc[i] != Time[0]) and ((Close[1] > Last_Ex[i] and Open[1] <= Last_Ex[i]) or (Close[1] <= Last_Ex[i] and Open[1] > Last_Ex[i])):
            text = 'ETV - PHLC Cross '
            if Open[1] < Close[1]:
                text += 'Up'
            elif Open[1] > Close[1]:
                text += 'Down'
            Alert(text)
            text += ' ' + DateTime
            obj_name = 'PHLCArrow_' + DateTime + '-' + IntegerToString(i)
            ObjectCreate(0, obj_name, OBJ_ARROW, 0, Time[1], Last_Ex[i])
            ObjectSetInteger(0, obj_name, OBJPROP_ARROWCODE, 200)
            ObjectSetInteger(0, obj_name, OBJPROP_COLOR, PHLC_Arrow_Color)
            desc = 'Price crossed: ' + DoubleToString(Last_Ex[i], Digits()) + ' @ ' + PerStr
            ObjectSetString(0, obj_name, OBJPROP_TOOLTIP, desc)
            ObjectSetString(0, obj_name, OBJPROP_TEXT, desc)
            ObjectSetInteger(0, obj_name, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, obj_name, OBJPROP_HIDDEN, False)
            text += ' ' + Symbol() + ' @ ' + PerStr
            if SendEmails:
                SendMail(text, text)
            if SendNotifications:
                SendNotification(text)
            was_alert_phlc[i] = Time[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EasyTrendVisualizer(_MQL5Indicator):
    name = 'EasyTrendVisualizer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXperiod1': 10,
        'ADXperiod2': 14,
        'ADXperiod3': 20,
        'UseAlertHorizontalLine': False,
        'UseAlertUpDownArrows': False,
        'UseAlertHorizontalLineCrossCurrent': False,
        'UseAlertHorizontalLineCrossPrevious': False,
        'NumberPHLtoTrack': 0,  # How many previous horizontal lines to track for alert purposes?
        'IgnorePHLShorterThan': 2,  # Ignore previous horizontal lines shorter than
        'NativeAlerts': False,  # Use pop-up alerts?
        'SendEmails': False,  # Send alerts via email?
        'SendNotifications': False,  # Send alerts via push notifications?
    }

