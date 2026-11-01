"""PinbarDetector — converted from MQL5: MQL5 Indicators/Pinbar Detector MT5/PinbarDetector.mq5

Pinbar Detector - detects Pinbars on charts.
Fully modifiable parameters of Pinbar pattern.
Usage instructions:
Link: https://t.me/ForexEaPremium; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '2.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [65280, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Pinbar Detector - detects Pinbars on charts.', 'Fully modifiable parameters of Pinbar pattern.', 'Usage instructions:'], 'name': 'PinbarDetector', 'source': 'MQL5 Indicators/Pinbar Detector MT5/PinbarDetector.mq5', 'folder': 'Pinbar Detector MT5', 'inputs': [{'mql': 'CountBars', 'py': 'CountBars', 'param': 'CountBars', 'type': 'int', 'default': 0, 'label': 'CountBars - number of bars to count on, 0 = all.', 'sinput': False}, {'mql': 'DisplayDistance', 'py': 'DisplayDistance', 'param': 'DisplayDistance', 'type': 'int', 'default': 5, 'label': 'DisplayDistance - the higher it is the the distance from faces to candles.', 'sinput': False}, {'mql': 'UseAlerts', 'py': 'UseAlerts', 'param': 'UseAlerts', 'type': 'bool', 'default': True, 'label': 'Use Alerts', 'sinput': False}, {'mql': 'UseEmailAlerts', 'py': 'UseEmailAlerts', 'param': 'UseEmailAlerts', 'type': 'bool', 'default': False, 'label': 'Use Email Alerts (configure SMTP parameters in Tools->Options->Emails)', 'sinput': False}, {'mql': 'UseNotificationAlerts', 'py': 'UseNotificationAlerts', 'param': 'UseNotificationAlerts', 'type': 'bool', 'default': False, 'label': 'Use Notification Alerts (configure push-notifications in Tools->Options->Notifications)', 'sinput': False}, {'mql': 'UseCustomSettings', 'py': 'UseCustomSettings', 'param': 'UseCustomSettings', 'type': 'bool', 'default': False, 'label': 'Use Custom Settings - if true = use below parameters:', 'sinput': False}, {'mql': 'CustomMaxNoseBodySize', 'py': 'CustomMaxNoseBodySize', 'param': 'CustomMaxNoseBodySize', 'type': 'double', 'default': 0.33, 'label': 'Max. Body / Candle length ratio of the Nose Bar', 'sinput': False}, {'mql': 'CustomNoseBodyPosition', 'py': 'CustomNoseBodyPosition', 'param': 'CustomNoseBodyPosition', 'type': 'double', 'default': 0.4, 'label': 'Body position in Nose Bar (e.g. top/bottom 40%)', 'sinput': False}, {'mql': 'CustomLeftEyeOppositeDirection', 'py': 'CustomLeftEyeOppositeDirection', 'param': 'CustomLeftEyeOppositeDirection', 'type': 'bool', 'default': True, 'label': 'true = Direction of Left Eye Bar should be opposite to pattern (bearish bar for bullish Pinbar pattern and vice versa)', 'sinput': False}, {'mql': 'CustomNoseSameDirection', 'py': 'CustomNoseSameDirection', 'param': 'CustomNoseSameDirection', 'type': 'bool', 'default': False, 'label': 'true = Direction of Nose Bar should be the same as of pattern (bullish bar for bullish Pinbar pattern and vice versa)', 'sinput': False}, {'mql': 'CustomNoseBodyInsideLeftEyeBody', 'py': 'CustomNoseBodyInsideLeftEyeBody', 'param': 'CustomNoseBodyInsideLeftEyeBody', 'type': 'bool', 'default': False, 'label': 'true = Nose Body should be contained inside Left Eye Body', 'sinput': False}, {'mql': 'CustomLeftEyeMinBodySize', 'py': 'CustomLeftEyeMinBodySize', 'param': 'CustomLeftEyeMinBodySize', 'type': 'double', 'default': 0.1, 'label': 'Min. Body / Candle length ratio of the Left Eye Bar', 'sinput': False}, {'mql': 'CustomNoseProtruding', 'py': 'CustomNoseProtruding', 'param': 'CustomNoseProtruding', 'type': 'double', 'default': 0.5, 'label': 'Minimum protrusion of Nose Bar compared to Nose Bar length', 'sinput': False}, {'mql': 'CustomNoseBodyToLeftEyeBody', 'py': 'CustomNoseBodyToLeftEyeBody', 'param': 'CustomNoseBodyToLeftEyeBody', 'type': 'double', 'default': 1.0, 'label': 'Maximum relative size of the Nose Bar Body to Left Eye Bar Body', 'sinput': False}, {'mql': 'CustomNoseLengthToLeftEyeLength', 'py': 'CustomNoseLengthToLeftEyeLength', 'param': 'CustomNoseLengthToLeftEyeLength', 'type': 'double', 'default': 0.0, 'label': 'Minimum relative size of the Nose Bar Length to Left Eye Bar Length', 'sinput': False}, {'mql': 'CustomLeftEyeDepth', 'py': 'CustomLeftEyeDepth', 'param': 'CustomLeftEyeDepth', 'type': 'double', 'default': 0.1, 'label': "Minimum relative depth of the Left Eye to its length; depth is difference with Nose's back", 'sinput': False}, {'mql': 'CustomMinimumNoseLength', 'py': 'CustomMinimumNoseLength', 'param': 'CustomMinimumNoseLength', 'type': 'int', 'default': 1, 'label': 'Minimum nose candlestick length in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CountBars = _input('CountBars', 0)  # CountBars - number of bars to count on, 0 = all.
DisplayDistance = _input('DisplayDistance', 5)  # DisplayDistance - the higher it is the the distance from faces to candles.
UseAlerts = _input('UseAlerts', True)  # Use Alerts
UseEmailAlerts = _input('UseEmailAlerts', False)  # Use Email Alerts (configure SMTP parameters in Tools->Options->Emails)
UseNotificationAlerts = _input('UseNotificationAlerts', False)  # Use Notification Alerts (configure push-notifications in Tools->Options->Notifications)
UseCustomSettings = _input('UseCustomSettings', False)  # Use Custom Settings - if true = use below parameters:
CustomMaxNoseBodySize = _input('CustomMaxNoseBodySize', 0.33)  # Max. Body / Candle length ratio of the Nose Bar
CustomNoseBodyPosition = _input('CustomNoseBodyPosition', 0.4)  # Body position in Nose Bar (e.g. top/bottom 40%)
CustomLeftEyeOppositeDirection = _input('CustomLeftEyeOppositeDirection', True)  # true = Direction of Left Eye Bar should be opposite to pattern (bearish bar for bullish Pinbar pattern and vice versa)
CustomNoseSameDirection = _input('CustomNoseSameDirection', False)  # true = Direction of Nose Bar should be the same as of pattern (bullish bar for bullish Pinbar pattern and vice versa)
CustomNoseBodyInsideLeftEyeBody = _input('CustomNoseBodyInsideLeftEyeBody', False)  # true = Nose Body should be contained inside Left Eye Body
CustomLeftEyeMinBodySize = _input('CustomLeftEyeMinBodySize', 0.1)  # Min. Body / Candle length ratio of the Left Eye Bar
CustomNoseProtruding = _input('CustomNoseProtruding', 0.5)  # Minimum protrusion of Nose Bar compared to Nose Bar length
CustomNoseBodyToLeftEyeBody = _input('CustomNoseBodyToLeftEyeBody', 1.0)  # Maximum relative size of the Nose Bar Body to Left Eye Bar Body
CustomNoseLengthToLeftEyeLength = _input('CustomNoseLengthToLeftEyeLength', 0.0)  # Minimum relative size of the Nose Bar Length to Left Eye Bar Length
CustomLeftEyeDepth = _input('CustomLeftEyeDepth', 0.1)  # Minimum relative depth of the Left Eye to its length; depth is difference with Nose's back
CustomMinimumNoseLength = _input('CustomMinimumNoseLength', 1)  # Minimum nose candlestick length in points
UpDown = Arr(0, 0.0)
Color = Arr(0, 0.0)
LastBars = 0
MaxNoseBodySize = 0.33
NoseBodyPosition = 0.4
LeftEyeOppositeDirection = True
NoseSameDirection = False
NoseBodyInsideLeftEyeBody = False
LeftEyeMinBodySize = 0.1
NoseProtruding = 0.5
NoseBodyToLeftEyeBody = 1.0
NoseLengthToLeftEyeLength = 0.0
LeftEyeDepth = 0.1
MinimumCandlestickLength = 1

def OnInit():
    global LeftEyeDepth, LeftEyeMinBodySize, LeftEyeOppositeDirection, MaxNoseBodySize, MinimumCandlestickLength, NoseBodyPosition, NoseBodyToLeftEyeBody, NoseLengthToLeftEyeLength, NoseProtruding, NoseSameDirection
    SetIndexBuffer(0, UpDown, INDICATOR_DATA)
    SetIndexBuffer(1, Color, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(UpDown, True)
    ArraySetAsSeries(Color, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 74)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, 'Pinbar')
    if UseCustomSettings:
        MaxNoseBodySize = CustomMaxNoseBodySize
        NoseBodyPosition = CustomNoseBodyPosition
        LeftEyeOppositeDirection = CustomLeftEyeOppositeDirection
        NoseSameDirection = CustomNoseSameDirection
        LeftEyeMinBodySize = CustomLeftEyeMinBodySize
        NoseProtruding = CustomNoseProtruding
        NoseBodyToLeftEyeBody = CustomNoseBodyToLeftEyeBody
        NoseLengthToLeftEyeLength = CustomNoseLengthToLeftEyeLength
        LeftEyeDepth = CustomLeftEyeDepth
        MinimumCandlestickLength = CustomMinimumNoseLength

def OnCalculate(rates_total, prev_calculated, time, Open, High, Low, Close, tickvolume, volume, spread):
    global LastBars
    NeedBarsCounted = 0
    NoseLength = 0.0
    NoseBody = 0.0
    LeftEyeBody = 0.0
    LeftEyeLength = 0.0
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    if LastBars == rates_total:
        return rates_total
    NeedBarsCounted = rates_total - LastBars
    if CountBars > 0 and NeedBarsCounted > CountBars:
        NeedBarsCounted = CountBars
    LastBars = rates_total
    if NeedBarsCounted == rates_total:
        NeedBarsCounted -= 1
    UpDown[0] = EMPTY_VALUE
    for i in range(NeedBarsCounted, 1 - 1, -1):
        UpDown[i] = EMPTY_VALUE
        if i == (rates_total - 1):
            continue
        NoseLength = High[i] - Low[i]
        if NoseLength < (MinimumCandlestickLength * Point()):
            continue
        if NoseLength == 0:
            NoseLength = Point()
        LeftEyeLength = High[i + 1] - Low[i + 1]
        if LeftEyeLength == 0:
            LeftEyeLength = Point()
        NoseBody = MathAbs(Open[i] - Close[i])
        if NoseBody == 0:
            NoseBody = Point()
        LeftEyeBody = MathAbs(Open[i + 1] - Close[i + 1])
        if LeftEyeBody == 0:
            LeftEyeBody = Point()
        if (High[i] - High[i + 1]) >= (NoseLength * NoseProtruding):
            if _fdiv(NoseBody, NoseLength) <= MaxNoseBodySize:
                if (1 - _fdiv(High[i] - MathMax(Open[i], Close[i]), NoseLength)) < NoseBodyPosition:
                    if (not LeftEyeOppositeDirection) or Close[i + 1] > Open[i + 1]:
                        if (not NoseSameDirection) or Close[i] < Open[i]:
                            if _fdiv(LeftEyeBody, LeftEyeLength) >= LeftEyeMinBodySize:
                                if MathMax(Open[i], Close[i]) <= High[i + 1] and MathMin(Open[i], Close[i]) >= Low[i + 1]:
                                    if _fdiv(NoseBody, LeftEyeBody) <= NoseBodyToLeftEyeBody:
                                        if _fdiv(NoseLength, LeftEyeLength) >= NoseLengthToLeftEyeLength:
                                            if (Low[i] - Low[i + 1]) >= (LeftEyeLength * LeftEyeDepth):
                                                if (not NoseBodyInsideLeftEyeBody) or (MathMax(Open[i], Close[i]) <= MathMax(Open[i + 1], Close[i + 1]) and MathMin(Open[i], Close[i]) >= MathMin(Open[i + 1], Close[i + 1])):
                                                    UpDown[i] = High[i] + (DisplayDistance * Point()) + (NoseLength / 5)
                                                    Color[i] = 1.0
                                                    if i == 1:
                                                        SendAlert('Bearish')
        if (Low[i + 1] - Low[i]) >= (NoseLength * NoseProtruding):
            if _fdiv(NoseBody, NoseLength) <= MaxNoseBodySize:
                if (1 - _fdiv(MathMin(Open[i], Close[i]) - Low[i], NoseLength)) < NoseBodyPosition:
                    if (not LeftEyeOppositeDirection) or Close[i + 1] < Open[i + 1]:
                        if (not NoseSameDirection) or Close[i] > Open[i]:
                            if _fdiv(LeftEyeBody, LeftEyeLength) >= LeftEyeMinBodySize:
                                if MathMax(Open[i], Close[i]) <= High[i + 1] and MathMin(Open[i], Close[i]) >= Low[i + 1]:
                                    if _fdiv(NoseBody, LeftEyeBody) <= NoseBodyToLeftEyeBody:
                                        if _fdiv(NoseLength, LeftEyeLength) >= NoseLengthToLeftEyeLength:
                                            if (High[i + 1] - High[i]) >= (LeftEyeLength * LeftEyeDepth):
                                                if (not NoseBodyInsideLeftEyeBody) or (MathMax(Open[i], Close[i]) <= MathMax(Open[i + 1], Close[i + 1]) and MathMin(Open[i], Close[i]) >= MathMin(Open[i + 1], Close[i + 1])):
                                                    UpDown[i] = Low[i] - (DisplayDistance * Point()) - (NoseLength / 5)
                                                    Color[i] = 0.0
                                                    if i == 1:
                                                        SendAlert('Bullish')
    return rates_total

def TimeframeToString(P):
    return StringSubstr(EnumToString(P, 'ENUM_TIMEFRAMES'), 7)

def SendAlert(dir):
    per = TimeframeToString(Period())
    if UseAlerts:
        Alert(dir + ' Pinbar on ', Symbol(), ' @ ', per)
        PlaySound('alert.wav')
    if UseEmailAlerts:
        SendMail(Symbol() + ' @ ' + per + ' - ' + dir + ' Pinbar', dir + ' Pinbar on ' + Symbol() + ' @ ' + per + ' as of ' + TimeToString(TimeCurrent()))
    if UseNotificationAlerts:
        SendNotification(dir + ' Pinbar on ' + Symbol() + ' @ ' + per + ' as of ' + TimeToString(TimeCurrent()))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PinbarDetector(_MQL5Indicator):
    name = 'PinbarDetector'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CountBars': 0,  # CountBars - number of bars to count on, 0 = all.
        'DisplayDistance': 5,  # DisplayDistance - the higher it is the the distance from faces to candles.
        'UseAlerts': True,  # Use Alerts
        'UseEmailAlerts': False,  # Use Email Alerts (configure SMTP parameters in Tools->Options->Emails)
        'UseNotificationAlerts': False,  # Use Notification Alerts (configure push-notifications in Tools->Options->Notifications)
        'UseCustomSettings': False,  # Use Custom Settings - if true = use below parameters:
        'CustomMaxNoseBodySize': 0.33,  # Max. Body / Candle length ratio of the Nose Bar
        'CustomNoseBodyPosition': 0.4,  # Body position in Nose Bar (e.g. top/bottom 40%)
        'CustomLeftEyeOppositeDirection': True,  # true = Direction of Left Eye Bar should be opposite to pattern (bearish bar for bullish Pinbar pattern and vice versa)
        'CustomNoseSameDirection': False,  # true = Direction of Nose Bar should be the same as of pattern (bullish bar for bullish Pinbar pattern and vice versa)
        'CustomNoseBodyInsideLeftEyeBody': False,  # true = Nose Body should be contained inside Left Eye Body
        'CustomLeftEyeMinBodySize': 0.1,  # Min. Body / Candle length ratio of the Left Eye Bar
        'CustomNoseProtruding': 0.5,  # Minimum protrusion of Nose Bar compared to Nose Bar length
        'CustomNoseBodyToLeftEyeBody': 1.0,  # Maximum relative size of the Nose Bar Body to Left Eye Bar Body
        'CustomNoseLengthToLeftEyeLength': 0.0,  # Minimum relative size of the Nose Bar Length to Left Eye Bar Length
        'CustomLeftEyeDepth': 0.1,  # Minimum relative depth of the Left Eye to its length; depth is difference with Nose's back
        'CustomMinimumNoseLength': 1,  # Minimum nose candlestick length in points
    }

