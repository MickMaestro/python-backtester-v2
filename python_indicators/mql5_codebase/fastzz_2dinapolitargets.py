"""fastzz_2dinapolitargets — converted from MQL5: MQL5 Indicators/Quick ZigZag plus DiNapoli/fastzz_2dinapolitargets.mq5

FastZZ plus DiNapoli Target Levels.
The modified indicator FastZZ.mq5.
Copyright: Copyright 2012, Yurich; Link: https://login.mql5.com/ru/users/Yurich; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Yurich', 'link': 'https://login.mql5.com/ru/users/Yurich', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [8421376]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Fast ZZ'}, 'levels': [], 'description': ['FastZZ plus DiNapoli Target Levels.', 'The modified indicator FastZZ.mq5.'], 'name': 'fastzz_2dinapolitargets', 'source': 'MQL5 Indicators/Quick ZigZag plus DiNapoli/fastzz_2dinapolitargets.mq5', 'folder': 'Quick ZigZag plus DiNapoli', 'inputs': [{'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 500, 'label': 'Minimum points in a ray', 'sinput': False}, {'mql': 'VLine', 'py': 'VLine', 'param': 'VLine', 'type': 'bool', 'default': True, 'label': 'Show the vertical lines', 'sinput': False}, {'mql': 'Sound', 'py': 'Sound', 'param': 'Sound', 'type': 'bool', 'default': True, 'label': 'Play sound', 'sinput': False}, {'mql': 'SoundFile', 'py': 'SoundFile', 'param': None, 'type': 'string', 'default': 'expert.wav', 'label': 'Sound file', 'sinput': False}, {'mql': 'cStar', 'py': 'cStar', 'param': None, 'type': 'color', 'default': 15794160, 'label': 'Start Line color', 'sinput': False}, {'mql': 'cStop', 'py': 'cStop', 'param': None, 'type': 'color', 'default': 255, 'label': 'Stop Line color', 'sinput': False}, {'mql': 'cTar1', 'py': 'cTar1', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Target1 Line color', 'sinput': False}, {'mql': 'cTar2', 'py': 'cTar2', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Target2 Line color', 'sinput': False}, {'mql': 'cTar3', 'py': 'cTar3', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Target3 Line color', 'sinput': False}, {'mql': 'cTar4', 'py': 'cTar4', 'param': None, 'type': 'color', 'default': 9125192, 'label': 'Target4 Line color', 'sinput': False}, {'mql': 'cTarT1', 'py': 'cTarT1', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Time Target1 color', 'sinput': False}, {'mql': 'cTarT2', 'py': 'cTarT2', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Time Target2 color', 'sinput': False}, {'mql': 'cTarT3', 'py': 'cTarT3', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Time Target3 color', 'sinput': False}, {'mql': 'cTarT4', 'py': 'cTarT4', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Time Target4 color', 'sinput': False}, {'mql': 'cTarT5', 'py': 'cTarT5', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Time Target4 color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Depth = _input('Depth', 500)  # Minimum points in a ray
VLine = _input('VLine', True)  # Show the vertical lines
Sound = _input('Sound', True)  # Play sound
SoundFile = _input('SoundFile', 'expert.wav')  # Sound file
cStar = _input('cStar', clrHoneydew)  # Start Line color
cStop = _input('cStop', clrRed)  # Stop Line color
cTar1 = _input('cTar1', clrGreen)  # Target1 Line color
cTar2 = _input('cTar2', clrDarkOrange)  # Target2 Line color
cTar3 = _input('cTar3', clrDarkOrchid)  # Target3 Line color
cTar4 = _input('cTar4', clrDarkSlateBlue)  # Target4 Line color
cTarT1 = _input('cTarT1', clrDarkSlateGray)  # Time Target1 color
cTarT2 = _input('cTarT2', clrDarkSlateGray)  # Time Target2 color
cTarT3 = _input('cTarT3', clrDarkSlateGray)  # Time Target3 color
cTarT4 = _input('cTarT4', clrDarkSlateGray)  # Time Target4 color
cTarT5 = _input('cTarT5', clrDarkSlateGray)  # Time Target4 color
zzH = Arr(0, 0.0)
zzL = Arr(0, 0.0)
depth = 0.0
A = 0.0
B = 0.0
C = 0.0
Price = Arr(6, 0.0, dyn=False)
last = 0
direction = 0
Refresh = 0
AT = 0
BT = 0
CT = 0
Time = Arr(5, 0, dyn=False)
Color = Arr(11, 0, dyn=False)
Name = Arr.of(['Start Line', 'Stop Line', 'Target1 Line', 'Target2 Line', 'Target3 Line', 'Target4 Line', 'Time Target1', 'Time Target2', 'Time Target3', 'Time Target4', 'Time Target5'], fill="", dyn=False, size=11)

def OnInit():
    global Refresh, depth, direction, last
    i = 0
    SetIndexBuffer(0, zzH, INDICATOR_DATA)
    SetIndexBuffer(1, zzL, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    Color[0] = cStar
    Color[1] = cStop
    Color[2] = cTar1
    Color[3] = cTar2
    Color[4] = cTar3
    Color[5] = cTar4
    Color[6] = cTarT1
    Color[7] = cTarT2
    Color[8] = cTarT3
    Color[9] = cTarT4
    Color[10] = cTarT5
    depth = Depth * Point()
    direction = 1
    last = 0
    Refresh = 1
    i = 0
    for i in range(i, 6):
        if ObjectFind(0, Name[i]) != 0:
            ObjectCreate(0, Name[i], OBJ_HLINE, 0, 0, 0)
            ObjectSetInteger(0, Name[i], OBJPROP_COLOR, Color[i])
            ObjectSetInteger(0, Name[i], OBJPROP_WIDTH, 1)
            ObjectSetInteger(0, Name[i], OBJPROP_STYLE, STYLE_DOT)
    else:
        i = _range_end(i, 6, 1)
    if VLine == True:
        i = 6
        for i in range(i, 11):
            if ObjectFind(0, Name[i]) != 0:
                ObjectCreate(0, Name[i], OBJ_VLINE, 0, 0, 0)
                ObjectSetInteger(0, Name[i], OBJPROP_COLOR, Color[i])
                ObjectSetInteger(0, Name[i], OBJPROP_WIDTH, 1)
                ObjectSetInteger(0, Name[i], OBJPROP_STYLE, STYLE_DOT)
        else:
            i = _range_end(i, 11, 1)

def OnDeinit(reason):
    i = 0
    i = 0
    for i in range(i, 11):
        ObjectDelete(0, Name[i])
    else:
        i = _range_end(i, 11, 1)
    ChartRedraw()
    return

def OnCalculate(total, calculated, time, open, high, low, close, tick, real, spread):
    global A, AT, B, BT, C, CT, Refresh, direction, last
    i = 0
    set_ = False
    a = 0.0
    if calculated == 0:
        last = 0
    i = ((calculated - 1) if (calculated > 0) else 0)
    for i in range(i, total - 1):
        set_ = False
        zzL[i] = 0.0
        zzH[i] = 0.0
        if direction > 0:
            if high[i] > zzH[last]:
                zzH[last] = 0.0
                zzH[i] = high[i]
                if low[i] < (high[last] - depth):
                    if open[i] < close[i]:
                        zzH[last] = high[last]
                        A = C
                        B = high[last]
                        C = low[i]
                        AT = CT
                        BT = time[last]
                        CT = time[i]
                        Refresh = 1
                    else:
                        direction = -1
                        A = B
                        B = C
                        C = high[i]
                        AT = BT
                        BT = CT
                        CT = time[i]
                        Refresh = 1
                    zzL[i] = low[i]
                last = i
                set_ = True
            if low[i] < (zzH[last] - depth) and ((not set_) or open[i] > close[i]):
                zzL[i] = low[i]
                if high[i] > (zzL[i] + depth) and open[i] < close[i]:
                    zzH[i] = high[i]
                    A = C
                    B = high[last]
                    C = low[i]
                    AT = CT
                    BT = time[last]
                    CT = time[i]
                    Refresh = 1
                else:
                    if direction > 0:
                        A = B
                        B = C
                        C = high[last]
                        AT = BT
                        BT = CT
                        CT = time[last]
                        Refresh = 1
                    direction = -1
                last = i
        else:
            if low[i] < zzL[last]:
                zzL[last] = 0.0
                zzL[i] = low[i]
                if high[i] > (low[last] + depth):
                    if open[i] > close[i]:
                        zzL[last] = low[last]
                        A = C
                        B = low[last]
                        C = high[i]
                        AT = CT
                        BT = time[last]
                        CT = time[i]
                        Refresh = 1
                    else:
                        direction = 1
                        A = B
                        B = C
                        C = low[i]
                        AT = BT
                        BT = CT
                        CT = time[i]
                        Refresh = 1
                    zzH[i] = high[i]
                last = i
                set_ = True
            if high[i] > (zzL[last] + depth) and ((not set_) or open[i] < close[i]):
                zzH[i] = high[i]
                if low[i] < (zzH[i] - depth) and open[i] > close[i]:
                    zzL[i] = low[i]
                    A = C
                    B = low[last]
                    C = high[i]
                    AT = CT
                    BT = time[last]
                    CT = time[i]
                    Refresh = 1
                else:
                    if direction < 0:
                        A = B
                        B = C
                        C = low[last]
                        AT = BT
                        BT = CT
                        CT = time[last]
                        Refresh = 1
                    direction = 1
                last = i
        zzH[total - 1] = 0.0
        zzL[total - 1] = 0.0
    else:
        i = _range_end(i, total - 1, 1)
    if Refresh == 1:
        Refresh = 0
        a = B - A
        Price[0] = NormalizeDouble((a * 0.318) + C, Digits())
        Price[1] = C
        Price[2] = NormalizeDouble((a * 0.618) + C, Digits())
        Price[3] = a + C
        Price[4] = NormalizeDouble((a * 1.618) + C, Digits())
        Price[5] = NormalizeDouble((a * 2.618) + C, Digits())
        i = 0
        for i in range(i, 6):
            ObjectMove(0, Name[i], 0, time[total - 1], Price[i])
        else:
            i = _range_end(i, 6, 1)
        if VLine == True:
            a = float(BT - AT)
            Time[0] = _long(MathRound(a * 0.318)) + CT
            Time[1] = _long(MathRound(a * 0.618)) + CT
            Time[2] = _long(MathRound(a)) + CT
            Time[3] = _long(MathRound(a * 1.618)) + CT
            Time[4] = _long(MathRound(a * 2.618)) + CT
            i = 6
            for i in range(i, 11):
                ObjectMove(0, Name[i], 0, Time[i - 6], open[total - 1])
            else:
                i = _range_end(i, 11, 1)
        ChartRedraw()
        if Sound == True:
            PlaySound(SoundFile)
    return total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fastzz2dinapolitargets(_MQL5Indicator):
    name = 'fastzz_2dinapolitargets'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Depth': 500,  # Minimum points in a ray
        'VLine': True,  # Show the vertical lines
        'Sound': True,  # Play sound
    }

