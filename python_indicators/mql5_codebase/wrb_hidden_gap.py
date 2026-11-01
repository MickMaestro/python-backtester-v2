"""wrb-hidden-gap — converted from MQL5: MQL5 Indicators/WRB/wrb-hidden-gap.mq5

by Andriy Moraru.
Copyright: EarnForex.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'EarnForex.com', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_plots': 1, 'indicator_buffers': 1}, 'types': {1: 5}, 'colors': {1: [16776960]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['', '', '', 'by Andriy Moraru.'], 'name': 'wrb-hidden-gap', 'source': 'MQL5 Indicators/WRB/wrb-hidden-gap.mq5', 'folder': 'WRB', 'inputs': [{'mql': 'UseWholeBars', 'py': 'UseWholeBars', 'param': 'UseWholeBars', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'WRB_LookBackBarCount', 'py': 'WRB_LookBackBarCount', 'param': 'WRB_LookBackBarCount', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'WRB_WingDingsSymbol', 'py': 'WRB_WingDingsSymbol', 'param': 'WRB_WingDingsSymbol', 'type': 'int', 'default': 115, 'label': '', 'sinput': False}, {'mql': 'HGcolor1', 'py': 'HGcolor1', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'HGcolor2', 'py': 'HGcolor2', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'HGstyle', 'py': 'HGstyle', 'param': 'HGstyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StartCalculationFromBar', 'py': 'StartCalculationFromBar', 'param': 'StartCalculationFromBar', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'HollowBoxes', 'py': 'HollowBoxes', 'param': 'HollowBoxes', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'DoAlerts', 'py': 'DoAlerts', 'param': 'DoAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UseWholeBars = _input('UseWholeBars', False)
WRB_LookBackBarCount = _input('WRB_LookBackBarCount', 3)
WRB_WingDingsSymbol = _input('WRB_WingDingsSymbol', 115)
HGcolor1 = _input('HGcolor1', clrDodgerBlue)
HGcolor2 = _input('HGcolor2', clrBlue)
HGstyle = _input('HGstyle', STYLE_SOLID)
StartCalculationFromBar = _input('StartCalculationFromBar', 100)
HollowBoxes = _input('HollowBoxes', False)
DoAlerts = _input('DoAlerts', False)
WRB = Arr(0, 0.0)
totalBarCount = -1

def ObDeleteObjectsByPrefix(Prefix):
    L = StringLen(Prefix)
    i = 0
    while i < ObjectsTotal(0, -1, OBJ_RECTANGLE):
        ObjName = ObjectName(0, i, -1, OBJ_RECTANGLE)
        if StringSubstr(ObjName, 0, L) != Prefix:
            i += 1
            continue
        ObjectDelete(0, ObjName)

def intersect(H1, L1, H2, L2):
    if L1 > H2 or H1 < L2:
        return 0
    if H1 >= H2 and L1 >= L2:
        return 1
    if H1 <= H2 and L1 <= L2:
        return 2
    if H1 >= H2 and L1 <= L2:
        return 3
    if H1 <= H2 and L1 >= L2:
        return 4
    return 0

def checkHGFilled(barNumber, High, Low, Time, rates_total):
    j = 0
    i = 0
    ObjectText = ""
    Prefix = 'HG_UNFILLED_'
    box_H = 0.0
    box_L = 0.0
    HGFillPA_H = 0.0
    HGFillPA_L = 0.0
    startTime = 0
    objectColor = 0
    L = StringLen(Prefix)
    i = 0
    while i < ObjectsTotal(0, -1, OBJ_RECTANGLE):
        ObjName = ObjectName(0, i, -1, OBJ_RECTANGLE)
        if StringSubstr(ObjName, 0, L) != Prefix:
            i += 1
            continue
        box_H = ObjectGetDouble(0, ObjName, OBJPROP_PRICE, 0)
        box_L = ObjectGetDouble(0, ObjName, OBJPROP_PRICE, 1)
        objectColor = _uint(ObjectGetInteger(0, ObjName, OBJPROP_COLOR))
        startTime = _uint(ObjectGetInteger(0, ObjName, OBJPROP_TIME, 0))
        HGFillPA_H = High[barNumber]
        HGFillPA_L = Low[barNumber]
        j = 0
        while (intersect(High[barNumber - j], Low[barNumber - j], box_H, box_L) != 0 and (barNumber - j) >= 0) and startTime < Time[barNumber - j]:
            if High[barNumber - j] > HGFillPA_H:
                HGFillPA_H = High[barNumber - j]
            if Low[barNumber - j] < HGFillPA_L:
                HGFillPA_L = Low[barNumber - j]
            if HGFillPA_H > box_H and HGFillPA_L < box_L:
                ObjectDelete(0, ObjName)
                ObjectText = 'HG_FILLED_' + TimeToString(startTime, TIME_DATE | TIME_MINUTES)
                ObjectCreate(0, ObjectText, OBJ_RECTANGLE, 0, startTime, box_H, Time[barNumber], box_L)
                ObjectSetInteger(0, ObjectText, OBJPROP_STYLE, HGstyle)
                ObjectSetInteger(0, ObjectText, OBJPROP_COLOR, objectColor)
                ObjectSetInteger(0, ObjectText, OBJPROP_FILL, not HollowBoxes)
                break
            j += 1
        i += 1

def checkWRB(i, Open, Close):
    j = 0
    WRB_test = False
    body = 0.0
    bodyPrior = 0.0
    WRB_test = True
    body = MathAbs(Open[i] - Close[i])
    j = 1
    for j in range(j, WRB_LookBackBarCount + 1):
        bodyPrior = MathAbs(Open[i - j] - Close[i - j])
        if bodyPrior > body:
            WRB_test = False
            break
    else:
        j = _range_end(j, WRB_LookBackBarCount + 1, 1)
    if WRB_test:
        WRB[i] = (Open[i] + Close[i]) / 2
    else:
        WRB[i] = EMPTY_VALUE
    return WRB_test

def checkHG(i, High, Low, Open, Close, Time):
    ObjectText = ""
    H = 0.0
    L = 0.0
    H2 = 0.0
    L2 = 0.0
    H1 = 0.0
    L1 = 0.0
    A = 0.0
    B = 0.0
    j = 0
    HGcolor = HGcolor1
    if WRB[i - 1] != EMPTY_VALUE:
        H2 = High[i - 2]
        L2 = Low[i - 2]
        H1 = High[i]
        L1 = Low[i]
        if UseWholeBars:
            H = High[i - 1]
            L = Low[i - 1]
        elif Open[i - 1] > Close[i - 1]:
            H = Open[i - 1]
            L = Close[i - 1]
        else:
            H = Close[i - 1]
            L = Open[i - 1]
        if L2 > H1:
            A = MathMin(L2, H)
            B = MathMax(H1, L)
        elif L1 > H2:
            A = MathMin(L1, H)
            B = MathMax(H2, L)
        else:
            return
        if A > B:
            Length = StringLen('HG_UNFILLED_')
            j = 0
            while j < ObjectsTotal(0, -1, OBJ_RECTANGLE):
                ObjectText = ObjectName(0, j, -1, OBJ_RECTANGLE)
                if StringSubstr(ObjectText, 0, Length) != 'HG_UNFILLED_':
                    j += 1
                    continue
                if intersect(ObjectGetDouble(0, ObjectText, OBJPROP_PRICE), ObjectGetDouble(0, ObjectText, OBJPROP_PRICE, 1), A, B) != 0:
                    HGcolor = _uint(ObjectGetInteger(0, ObjectText, OBJPROP_COLOR))
                    if HGcolor == HGcolor1:
                        HGcolor = HGcolor2
                    else:
                        HGcolor = HGcolor1
                    break
                j += 1
            ObjectText = 'HG_UNFILLED_' + TimeToString(Time[i - 1], TIME_DATE | TIME_MINUTES)
            ObjectCreate(0, ObjectText, OBJ_RECTANGLE, 0, Time[i - 1], A, TimeCurrent() + (10 * 365 * 24 * 60 * 60), B)
            ObjectSetInteger(0, ObjectText, OBJPROP_STYLE, HGstyle)
            ObjectSetInteger(0, ObjectText, OBJPROP_COLOR, HGcolor)
            ObjectSetInteger(0, ObjectText, OBJPROP_FILL, not HollowBoxes)

def CheckAlert():
    total = ObjectsTotal(0, -1, OBJ_RECTANGLE)
    for j in range(0, total):
        ObjectText = ObjectName(0, j, -1, OBJ_RECTANGLE)
        if StringSubstr(ObjectText, StringLen(ObjectText) - 1, 1) == 'A':
            ObjectNameWithoutA = StringSubstr(ObjectText, 0, StringLen(ObjectText) - 1)
            if ObjectFind(0, ObjectNameWithoutA) >= 0:
                ObjectDelete(0, ObjectNameWithoutA)
            continue
        Length = StringLen('HG_UNFILLED_')
        if StringSubstr(ObjectText, 0, Length) != 'HG_UNFILLED_':
            continue
        Ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
        Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        Price1 = ObjectGetDouble(0, ObjectText, OBJPROP_PRICE)
        Price2 = ObjectGetDouble(0, ObjectText, OBJPROP_PRICE, 1)
        High = MathMax(Price1, Price2)
        Low = MathMin(Price1, Price2)
        if Ask > Low and Bid < High:
            Alert(Symbol() + ': ' + 'WRB rectangle breached.')
            PlaySound('alert.wav')
            ObjectSetString(0, ObjectText, OBJPROP_NAME, ObjectText + 'A')
            return

def OnInit():
    SetIndexBuffer(0, WRB, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, WRB_WingDingsSymbol)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, 'WRB')
    IndicatorSetString(INDICATOR_SHORTNAME, 'WRB+HG')
    ArrayInitialize(WRB, EMPTY_VALUE)

def OnDeinit(reason):
    ObDeleteObjectsByPrefix('HG_')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global totalBarCount
    if DoAlerts:
        CheckAlert()
    if totalBarCount != rates_total:
        start = prev_calculated
        start -= 1
        if start < WRB_LookBackBarCount:
            start = WRB_LookBackBarCount
        if start < (rates_total - 1 - StartCalculationFromBar):
            start = rates_total - 1 - StartCalculationFromBar
        for i in range(start, rates_total - 1):
            if UseWholeBars:
                checkWRB(i, High, Low)
            else:
                checkWRB(i, Open, Close)
            checkHG(i, High, Low, Open, Close, Time)
            checkHGFilled(i, High, Low, Time, rates_total)
        totalBarCount = rates_total
    checkHGFilled(rates_total - 1, High, Low, Time, rates_total)
    WRB[rates_total - 1] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WrbHiddenGap(_MQL5Indicator):
    name = 'wrb-hidden-gap'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'UseWholeBars': False,
        'WRB_LookBackBarCount': 3,
        'WRB_WingDingsSymbol': 115,
        'HGstyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'StartCalculationFromBar': 100,
        'HollowBoxes': False,
        'DoAlerts': False,
    }

