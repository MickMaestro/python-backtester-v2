"""pinbardetector — converted from MQL5: MQL5 Indicators/Pinbar Detector/pinbardetector.mq5

Pinbar Detector - detects Pinbars on charts.
Has two sets of predefined settings: common and strict.
Fully modifiable parameters of Pinbar pattern.
Usage instructions:
http://www.earnforex.com/forex-strategy/pinbar-trading-system
http://nysetrader.net/pin-bar/
Copyright: Copyright © 2011, EarnForex; Link: http://www.earnforex.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [65280, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Pinbar Detector - detects Pinbars on charts.', 'Has two sets of predefined settings: common and strict.', 'Fully modifiable parameters of Pinbar pattern.', 'Usage instructions:', 'http://www.earnforex.com/forex-strategy/pinbar-trading-system', 'http://nysetrader.net/pin-bar/'], 'name': 'pinbardetector', 'source': 'MQL5 Indicators/Pinbar Detector/pinbardetector.mq5', 'folder': 'Pinbar Detector', 'inputs': [{'mql': 'UseAlerts', 'py': 'UseAlerts', 'param': 'UseAlerts', 'type': 'bool', 'default': True, 'label': 'Permission to alerts', 'sinput': False}, {'mql': 'UseEmailAlerts', 'py': 'UseEmailAlerts', 'param': 'UseEmailAlerts', 'type': 'bool', 'default': False, 'label': 'Permission to email alerts', 'sinput': False}, {'mql': 'MaxNoseBodySize', 'py': 'MaxNoseBodySize', 'param': 'MaxNoseBodySize', 'type': 'double', 'default': 0.33, 'label': 'maximum allowable ratio of Nose body to the bar length', 'sinput': False}, {'mql': 'NoseBodyPosition', 'py': 'NoseBodyPosition', 'param': 'NoseBodyPosition', 'type': 'double', 'default': 0.4, 'label': 'extreme position of the Nose body inside the bar. Upper part for the bullish pattern, lower part to the bearish pattern', 'sinput': False}, {'mql': 'LeftEyeOppositeDirection', 'py': 'LeftEyeOppositeDirection', 'param': 'LeftEyeOppositeDirection', 'type': 'bool', 'default': True, 'label': 'Left eye should be bearish for the bullish Pin Bar and should be bullish for the bearish Pin Bar', 'sinput': False}, {'mql': 'NoseSameDirection', 'py': 'NoseSameDirection', 'param': 'NoseSameDirection', 'type': 'bool', 'default': False, 'label': 'the Nose should be in the same direction as the pattern itself', 'sinput': False}, {'mql': 'NoseBodyInsideLeftEyeBody', 'py': 'NoseBodyInsideLeftEyeBody', 'param': 'NoseBodyInsideLeftEyeBody', 'type': 'bool', 'default': False, 'label': 'the Nose body should be fit in the Left Eye body', 'sinput': False}, {'mql': 'LeftEyeMinBodySize', 'py': 'LeftEyeMinBodySize', 'param': 'LeftEyeMinBodySize', 'type': 'double', 'default': 0.1, 'label': 'minimum size of the Left Eye body relatively to the bar length', 'sinput': False}, {'mql': 'NoseProtruding', 'py': 'NoseProtruding', 'param': 'NoseProtruding', 'type': 'double', 'default': 0.5, 'label': 'minimum Nose protrusion relatively to the bar length', 'sinput': False}, {'mql': 'NoseBodyToLeftEyeBody', 'py': 'NoseBodyToLeftEyeBody', 'param': 'NoseBodyToLeftEyeBody', 'type': 'double', 'default': 1.0, 'label': 'maximum size of the Nose body relatively to the Left Eye body', 'sinput': False}, {'mql': 'NoseLengthToLeftEyeLength', 'py': 'NoseLengthToLeftEyeLength', 'param': 'NoseLengthToLeftEyeLength', 'type': 'double', 'default': 0.0, 'label': 'minimum Nose size relatively to the Left Eye', 'sinput': False}, {'mql': 'LeftEyeDepth', 'py': 'LeftEyeDepth', 'param': 'LeftEyeDepth', 'type': 'double', 'default': 0.1, 'label': 'minimum depth of the Left Eye relatively to its length. Depth is the length of the bar part behind the Nose', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UseAlerts = _input('UseAlerts', True)  # Permission to alerts
UseEmailAlerts = _input('UseEmailAlerts', False)  # Permission to email alerts
MaxNoseBodySize = _input('MaxNoseBodySize', 0.33)  # maximum allowable ratio of Nose body to the bar length
NoseBodyPosition = _input('NoseBodyPosition', 0.4)  # extreme position of the Nose body inside the bar. Upper part for the bullish pattern, lower part to the bearish pattern
LeftEyeOppositeDirection = _input('LeftEyeOppositeDirection', True)  # Left eye should be bearish for the bullish Pin Bar and should be bullish for the bearish Pin Bar
NoseSameDirection = _input('NoseSameDirection', False)  # the Nose should be in the same direction as the pattern itself
NoseBodyInsideLeftEyeBody = _input('NoseBodyInsideLeftEyeBody', False)  # the Nose body should be fit in the Left Eye body
LeftEyeMinBodySize = _input('LeftEyeMinBodySize', 0.1)  # minimum size of the Left Eye body relatively to the bar length
NoseProtruding = _input('NoseProtruding', 0.5)  # minimum Nose protrusion relatively to the bar length
NoseBodyToLeftEyeBody = _input('NoseBodyToLeftEyeBody', 1.0)  # maximum size of the Nose body relatively to the Left Eye body
NoseLengthToLeftEyeLength = _input('NoseLengthToLeftEyeLength', 0.0)  # minimum Nose size relatively to the Left Eye
LeftEyeDepth = _input('LeftEyeDepth', 0.1)  # minimum depth of the Left Eye relatively to its length. Depth is the length of the bar part behind the Nose
UpDown = Arr(0, 0.0)
Color = Arr(0, 0.0)
LastBars = 0

def OnInit():
    SetIndexBuffer(0, UpDown, INDICATOR_DATA)
    SetIndexBuffer(1, Color, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(UpDown, True)
    ArraySetAsSeries(Color, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 74)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, 'Pinbar')

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
    LastBars = rates_total
    if NeedBarsCounted == rates_total:
        NeedBarsCounted -= 1
    UpDown[0] = EMPTY_VALUE
    for bar in range(NeedBarsCounted, 1 - 1, -1):
        UpDown[bar] = EMPTY_VALUE
        if bar == (rates_total - 1):
            continue
        NoseLength = High[bar] - Low[bar]
        if not NoseLength:
            NoseLength = Point()
        LeftEyeLength = High[bar + 1] - Low[bar + 1]
        if not LeftEyeLength:
            LeftEyeLength = Point()
        NoseBody = MathAbs(Open[bar] - Close[bar])
        if not NoseBody:
            NoseBody = Point()
        LeftEyeBody = MathAbs(Open[bar + 1] - Close[bar + 1])
        if not LeftEyeBody:
            LeftEyeBody = Point()
        if (High[bar] - High[bar + 1]) >= (NoseLength * NoseProtruding):
            if _fdiv(NoseBody, NoseLength) <= MaxNoseBodySize:
                if (1 - _fdiv(High[bar] - MathMax(Open[bar], Close[bar]), NoseLength)) < NoseBodyPosition:
                    if (not LeftEyeOppositeDirection) or Close[bar + 1] > Open[bar + 1]:
                        if (not NoseSameDirection) or Close[bar] < Open[bar]:
                            if _fdiv(LeftEyeBody, LeftEyeLength) >= LeftEyeMinBodySize:
                                if MathMax(Open[bar], Close[bar] <= High[bar + 1]) and MathMin(Open[bar], Close[bar]) >= Low[bar + 1]:
                                    if _fdiv(NoseBody, LeftEyeBody) <= NoseBodyToLeftEyeBody:
                                        if _fdiv(NoseLength, LeftEyeLength) >= NoseLengthToLeftEyeLength:
                                            if (Low[bar] - Low[bar + 1]) >= (LeftEyeLength * LeftEyeDepth):
                                                if (not NoseBodyInsideLeftEyeBody) or (MathMax(Open[bar], Close[bar]) <= MathMax(Open[bar + 1], Close[bar + 1]) and MathMin(Open[bar], Close[bar]) >= MathMin(Open[bar + 1], Close[bar + 1])):
                                                    UpDown[bar] = High[bar] + (5 * Point()) + (NoseLength / 5)
                                                    Color[bar] = 1.0
                                                    if bar == 1:
                                                        SendAlert('Bearish')
        if (Low[bar + 1] - Low[bar]) >= (NoseLength * NoseProtruding):
            if _fdiv(NoseBody, NoseLength) <= MaxNoseBodySize:
                if (1 - _fdiv(MathMin(Open[bar], Close[bar]) - Low[bar], NoseLength)) < NoseBodyPosition:
                    if (not LeftEyeOppositeDirection) or Close[bar + 1] < Open[bar + 1]:
                        if (not NoseSameDirection) or Close[bar] > Open[bar]:
                            if _fdiv(LeftEyeBody, LeftEyeLength) >= LeftEyeMinBodySize:
                                if MathMax(Open[bar], Close[bar] <= High[bar + 1]) and MathMin(Open[bar], Close[bar]) >= Low[bar + 1]:
                                    if _fdiv(NoseBody, LeftEyeBody) <= NoseBodyToLeftEyeBody:
                                        if _fdiv(NoseLength, LeftEyeLength) >= NoseLengthToLeftEyeLength:
                                            if (High[bar + 1] - High[bar]) >= (LeftEyeLength * LeftEyeDepth):
                                                if (not NoseBodyInsideLeftEyeBody) or (MathMax(Open[bar], Close[bar]) <= MathMax(Open[bar + 1], Close[bar + 1]) and MathMin(Open[bar], Close[bar]) >= MathMin(Open[bar + 1], Close[bar + 1])):
                                                    UpDown[bar] = Low[bar] - (5 * Point()) - (NoseLength / 5)
                                                    Color[bar] = 0.0
                                                    if bar == 1:
                                                        SendAlert('Bullish')
    return rates_total

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def SendAlert(dir):
    per = TimeframeToString(Period())
    if UseAlerts:
        Alert(dir + ' Pinbar on ', Symbol(), ' @ ', per)
        PlaySound('alert.wav')
    if UseEmailAlerts:
        SendMail(Symbol() + ' @ ' + per + ' - ' + dir + ' Pinbar', dir + ' Pinbar on ' + Symbol() + ' @ ' + per + ' as of ' + TimeToString(TimeCurrent()))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pinbardetector(_MQL5Indicator):
    name = 'pinbardetector'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UseAlerts': True,  # Permission to alerts
        'UseEmailAlerts': False,  # Permission to email alerts
        'MaxNoseBodySize': 0.33,  # maximum allowable ratio of Nose body to the bar length
        'NoseBodyPosition': 0.4,  # extreme position of the Nose body inside the bar. Upper part for the bullish pattern, lower part to the bearish pattern
        'LeftEyeOppositeDirection': True,  # Left eye should be bearish for the bullish Pin Bar and should be bullish for the bearish Pin Bar
        'NoseSameDirection': False,  # the Nose should be in the same direction as the pattern itself
        'NoseBodyInsideLeftEyeBody': False,  # the Nose body should be fit in the Left Eye body
        'LeftEyeMinBodySize': 0.1,  # minimum size of the Left Eye body relatively to the bar length
        'NoseProtruding': 0.5,  # minimum Nose protrusion relatively to the bar length
        'NoseBodyToLeftEyeBody': 1.0,  # maximum size of the Nose body relatively to the Left Eye body
        'NoseLengthToLeftEyeLength': 0.0,  # minimum Nose size relatively to the Left Eye
        'LeftEyeDepth': 0.1,  # minimum depth of the Left Eye relatively to its length. Depth is the length of the bar part behind the Nose
    }

