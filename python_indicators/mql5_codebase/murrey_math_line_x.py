"""Murrey_Math_Line_X — converted from MQL5: MQL5 Indicators/Murrey Math Line X MT5/Murrey_Math_Line_X.mq5

Murrey Math Line X - support and resistance lines according to Murrey Math rules.
Link: https://t.me/ForexEaPremium; Version: 1.05

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '1.05', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Murrey Math Line X - support and resistance lines according to Murrey Math rules.'], 'name': 'Murrey_Math_Line_X', 'source': 'MQL5 Indicators/Murrey Math Line X MT5/Murrey_Math_Line_X.mq5', 'folder': 'Murrey Math Line X MT5', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 64, 'label': 'Period', 'sinput': False}, {'mql': 'UpperTimeframe', 'py': 'UpperTimeframe', 'param': 'UpperTimeframe', 'type': 'int', 'default': 16408, 'label': '', 'sinput': False}, {'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LabelSide', 'py': 'LabelSide', 'param': 'LabelSide', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'mml_clr_m_2_8', 'py': 'mml_clr_m_2_8', 'param': None, 'type': 'color', 'default': 16777215, 'label': '[-2]/8 Color', 'sinput': False}, {'mql': 'mml_clr_m_1_8', 'py': 'mml_clr_m_1_8', 'param': None, 'type': 'color', 'default': 16777215, 'label': '[-1]/8 Color', 'sinput': False}, {'mql': 'mml_clr_0_8', 'py': 'mml_clr_0_8', 'param': None, 'type': 'color', 'default': 16776960, 'label': '[0]/8 Color', 'sinput': False}, {'mql': 'mml_clr_1_8', 'py': 'mml_clr_1_8', 'param': None, 'type': 'color', 'default': 65535, 'label': '[1]/8 Color', 'sinput': False}, {'mql': 'mml_clr_2_8', 'py': 'mml_clr_2_8', 'param': None, 'type': 'color', 'default': 255, 'label': '[2]/8 Color', 'sinput': False}, {'mql': 'mml_clr_3_8', 'py': 'mml_clr_3_8', 'param': None, 'type': 'color', 'default': 32768, 'label': '[3]/8 Color', 'sinput': False}, {'mql': 'mml_clr_4_8', 'py': 'mml_clr_4_8', 'param': None, 'type': 'color', 'default': 16711680, 'label': '[4]/8 Color', 'sinput': False}, {'mql': 'mml_clr_5_8', 'py': 'mml_clr_5_8', 'param': None, 'type': 'color', 'default': 32768, 'label': '[5]/8 Color', 'sinput': False}, {'mql': 'mml_clr_6_8', 'py': 'mml_clr_6_8', 'param': None, 'type': 'color', 'default': 255, 'label': '[6]/8 Color', 'sinput': False}, {'mql': 'mml_clr_7_8', 'py': 'mml_clr_7_8', 'param': None, 'type': 'color', 'default': 65535, 'label': '[7]/8 Color', 'sinput': False}, {'mql': 'mml_clr_8_8', 'py': 'mml_clr_8_8', 'param': None, 'type': 'color', 'default': 16776960, 'label': '[8]/8 Color', 'sinput': False}, {'mql': 'mml_clr_p_1_8', 'py': 'mml_clr_p_1_8', 'param': None, 'type': 'color', 'default': 16777215, 'label': '[+1]/8 Color', 'sinput': False}, {'mql': 'mml_clr_p_2_8', 'py': 'mml_clr_p_2_8', 'param': None, 'type': 'color', 'default': 16777215, 'label': '[+2]/8 Color', 'sinput': False}, {'mql': 'mml_wdth_m_2_8', 'py': 'mml_wdth_m_2_8', 'param': 'mml_wdth_m_2_8', 'type': 'int', 'default': 2, 'label': '[-2]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_m_1_8', 'py': 'mml_wdth_m_1_8', 'param': 'mml_wdth_m_1_8', 'type': 'int', 'default': 1, 'label': '[-1]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_0_8', 'py': 'mml_wdth_0_8', 'param': 'mml_wdth_0_8', 'type': 'int', 'default': 1, 'label': '[0]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_1_8', 'py': 'mml_wdth_1_8', 'param': 'mml_wdth_1_8', 'type': 'int', 'default': 1, 'label': '[1]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_2_8', 'py': 'mml_wdth_2_8', 'param': 'mml_wdth_2_8', 'type': 'int', 'default': 1, 'label': '[2]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_3_8', 'py': 'mml_wdth_3_8', 'param': 'mml_wdth_3_8', 'type': 'int', 'default': 1, 'label': '[3]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_4_8', 'py': 'mml_wdth_4_8', 'param': 'mml_wdth_4_8', 'type': 'int', 'default': 1, 'label': '[4]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_5_8', 'py': 'mml_wdth_5_8', 'param': 'mml_wdth_5_8', 'type': 'int', 'default': 1, 'label': '[5]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_6_8', 'py': 'mml_wdth_6_8', 'param': 'mml_wdth_6_8', 'type': 'int', 'default': 1, 'label': '[6]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_7_8', 'py': 'mml_wdth_7_8', 'param': 'mml_wdth_7_8', 'type': 'int', 'default': 1, 'label': '[7]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_8_8', 'py': 'mml_wdth_8_8', 'param': 'mml_wdth_8_8', 'type': 'int', 'default': 1, 'label': '[8]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_p_1_8', 'py': 'mml_wdth_p_1_8', 'param': 'mml_wdth_p_1_8', 'type': 'int', 'default': 1, 'label': '[+1]/8 Width', 'sinput': False}, {'mql': 'mml_wdth_p_2_8', 'py': 'mml_wdth_p_2_8', 'param': 'mml_wdth_p_2_8', 'type': 'int', 'default': 2, 'label': '[+2]/8 Width', 'sinput': False}, {'mql': 'MarkColor', 'py': 'MarkColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'MarkNumber', 'py': 'MarkNumber', 'param': 'MarkNumber', 'type': 'int', 'default': 217, 'label': '', 'sinput': False}, {'mql': 'FontFace', 'py': 'FontFace', 'param': None, 'type': 'string', 'default': 'Verdana', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'MML-', 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'NativeAlerts', 'py': 'NativeAlerts', 'param': 'NativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlerts', 'py': 'EmailAlerts', 'param': 'EmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'NotificationAlerts', 'py': 'NotificationAlerts', 'param': 'NotificationAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_side
Left = 0
Right = 1
_enum('enum_side', {0: 'Left', 1: 'Right'})

# enum ENUM_CANDLE_TO_CHECK
Current = 0
Previous = 1
_enum('ENUM_CANDLE_TO_CHECK', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
period = _input('period', 64)  # Period
UpperTimeframe = _input('UpperTimeframe', PERIOD_D1)
StepBack = _input('StepBack', 0)
LabelSide = _input('LabelSide', Left)
mml_clr_m_2_8 = _input('mml_clr_m_2_8', clrWhite)  # [-2]/8 Color
mml_clr_m_1_8 = _input('mml_clr_m_1_8', clrWhite)  # [-1]/8 Color
mml_clr_0_8 = _input('mml_clr_0_8', clrAqua)  # [0]/8 Color
mml_clr_1_8 = _input('mml_clr_1_8', clrYellow)  # [1]/8 Color
mml_clr_2_8 = _input('mml_clr_2_8', clrRed)  # [2]/8 Color
mml_clr_3_8 = _input('mml_clr_3_8', clrGreen)  # [3]/8 Color
mml_clr_4_8 = _input('mml_clr_4_8', clrBlue)  # [4]/8 Color
mml_clr_5_8 = _input('mml_clr_5_8', clrGreen)  # [5]/8 Color
mml_clr_6_8 = _input('mml_clr_6_8', clrRed)  # [6]/8 Color
mml_clr_7_8 = _input('mml_clr_7_8', clrYellow)  # [7]/8 Color
mml_clr_8_8 = _input('mml_clr_8_8', clrAqua)  # [8]/8 Color
mml_clr_p_1_8 = _input('mml_clr_p_1_8', clrWhite)  # [+1]/8 Color
mml_clr_p_2_8 = _input('mml_clr_p_2_8', clrWhite)  # [+2]/8 Color
mml_wdth_m_2_8 = _input('mml_wdth_m_2_8', 2)  # [-2]/8 Width
mml_wdth_m_1_8 = _input('mml_wdth_m_1_8', 1)  # [-1]/8 Width
mml_wdth_0_8 = _input('mml_wdth_0_8', 1)  # [0]/8 Width
mml_wdth_1_8 = _input('mml_wdth_1_8', 1)  # [1]/8 Width
mml_wdth_2_8 = _input('mml_wdth_2_8', 1)  # [2]/8 Width
mml_wdth_3_8 = _input('mml_wdth_3_8', 1)  # [3]/8 Width
mml_wdth_4_8 = _input('mml_wdth_4_8', 1)  # [4]/8 Width
mml_wdth_5_8 = _input('mml_wdth_5_8', 1)  # [5]/8 Width
mml_wdth_6_8 = _input('mml_wdth_6_8', 1)  # [6]/8 Width
mml_wdth_7_8 = _input('mml_wdth_7_8', 1)  # [7]/8 Width
mml_wdth_8_8 = _input('mml_wdth_8_8', 1)  # [8]/8 Width
mml_wdth_p_1_8 = _input('mml_wdth_p_1_8', 1)  # [+1]/8 Width
mml_wdth_p_2_8 = _input('mml_wdth_p_2_8', 2)  # [+2]/8 Width
MarkColor = _input('MarkColor', clrBlue)
MarkNumber = _input('MarkNumber', 217)
FontFace = _input('FontFace', 'Verdana')
FontSize = _input('FontSize', 10)
ObjectPrefix = _input('ObjectPrefix', 'MML-')
TriggerCandle = _input('TriggerCandle', Previous)
NativeAlerts = _input('NativeAlerts', False)
EmailAlerts = _input('EmailAlerts', False)
NotificationAlerts = _input('NotificationAlerts', False)
ln_txt = Arr(13, "", dyn=False)
OctLinesCnt = 13
mml_clr = Arr(13, 0, dyn=False)
mml_wdth = Arr(13, 0, dyn=False)
mml = Arr(13, 0.0, dyn=False)
nTime = 0
NewPeriod = 0
LastAlertTime = Arr(13, 0, dyn=False)
prevSignal = Arr(13, 0, dyn=False)

def OnInit():
    global NewPeriod
    if UpperTimeframe != PERIOD_CURRENT and UpperTimeframe != Period():
        NewPeriod = period * _int(MathCeil(_idiv(PeriodSeconds(UpperTimeframe), PeriodSeconds(Period()))))
    else:
        NewPeriod = period
    ln_txt[0] = '[-2/8]P Extreme Overshoot [-2/8]'
    ln_txt[1] = '[-1/8]P Overshoot [-1/8]'
    ln_txt[2] = '[0/8]P Ultimate Support - extremely oversold [0/8]'
    ln_txt[3] = '[1/8]P Weak, Place to Stop and Reverse [1/8]'
    ln_txt[4] = '[2/8]P Pivot, Reverse - major [2/8]'
    ln_txt[5] = '[3/8]P Bottom of Trading Range [3/8] - BUY Premium Zone'
    ln_txt[6] = '[4/8]P Major S/R Pivot Point [4/8] - Best New BUY or SELL level'
    ln_txt[7] = '[5/8]P Top of Trading Range [5/8] - SELL Premium Zone'
    ln_txt[8] = '[6/8]P Pivot, Reverse - major [6/8]'
    ln_txt[9] = '[7/8]P Weak, Place to Stop and Reverse [7/8]'
    ln_txt[10] = '[8/8]P Ultimate Resistance - extremely overbought [8/8]'
    ln_txt[11] = '[+1/8]P Overshoot [+1/8]'
    ln_txt[12] = '[+2/8]P Extreme Overshoot [+2/8]'
    mml_clr[0] = mml_clr_m_2_8
    mml_wdth[0] = mml_wdth_m_2_8
    mml_clr[1] = mml_clr_m_1_8
    mml_wdth[1] = mml_wdth_m_1_8
    mml_clr[2] = mml_clr_0_8
    mml_wdth[2] = mml_wdth_0_8
    mml_clr[3] = mml_clr_1_8
    mml_wdth[3] = mml_wdth_1_8
    mml_clr[4] = mml_clr_2_8
    mml_wdth[4] = mml_wdth_2_8
    mml_clr[5] = mml_clr_3_8
    mml_wdth[5] = mml_wdth_3_8
    mml_clr[6] = mml_clr_4_8
    mml_wdth[6] = mml_wdth_4_8
    mml_clr[7] = mml_clr_5_8
    mml_wdth[7] = mml_wdth_5_8
    mml_clr[8] = mml_clr_6_8
    mml_wdth[8] = mml_wdth_6_8
    mml_clr[9] = mml_clr_7_8
    mml_wdth[9] = mml_wdth_7_8
    mml_clr[10] = mml_clr_8_8
    mml_wdth[10] = mml_wdth_8_8
    mml_clr[11] = mml_clr_p_1_8
    mml_wdth[11] = mml_wdth_p_1_8
    mml_clr[12] = mml_clr_p_2_8
    mml_wdth[12] = mml_wdth_p_2_8

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), ObjectPrefix)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global nTime
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Time, True)
    if nTime < Time[0]:
        bn_v1 = ArrayMinimum(Low, StepBack, NewPeriod + StepBack)
        bn_v2 = ArrayMaximum(High, StepBack, NewPeriod + StepBack)
        v1 = Low[bn_v1]
        v2 = High[bn_v2]
        fractal = 0.0
        if v2 <= 250000 and v2 > 25000:
            fractal = 100000.0
        elif v2 <= 25000 and v2 > 2500:
            fractal = 10000.0
        elif v2 <= 2500 and v2 > 250:
            fractal = 1000.0
        elif v2 <= 250 and v2 > 25:
            fractal = 100.0
        elif v2 <= 25 and v2 > 12.5:
            fractal = 12.5
        elif v2 <= 12.5 and v2 > 6.25:
            fractal = 12.5
        elif v2 <= 6.25 and v2 > 3.125:
            fractal = 6.25
        elif v2 <= 3.125 and v2 > 1.5625:
            fractal = 3.125
        elif v2 <= 1.5625 and v2 > 0.390625:
            fractal = 1.5625
        elif v2 <= 0.390625 and v2 > 0:
            fractal = 0.1953125
        range_ = v2 - v1
        sum_ = MathFloor(_fdiv(MathLog(_fdiv(fractal, range_)), MathLog(2)))
        octave = fractal * MathPow(0.5, sum_)
        mn = MathFloor(_fdiv(v1, octave)) * octave
        mx = 0.0
        if (mn + octave) > v2:
            mx = mn + octave
        else:
            mx = mn + (2 * octave)
        x1 = 0.0
        x2 = 0.0
        x3 = 0.0
        x4 = 0.0
        x5 = 0.0
        x6 = 0.0
        if v1 >= (((3 * (mx - mn)) / 16) + mn) and v2 <= (((9 * (mx - mn)) / 16) + mn):
            x2 = mn + ((mx - mn) / 2)
        else:
            x2 = 0.0
        if (v1 >= (mn - ((mx - mn) / 8)) and v2 <= (((5 * (mx - mn)) / 8) + mn)) and x2 == 0:
            x1 = mn + ((mx - mn) / 2)
        else:
            x1 = 0.0
        if v1 >= (mn + ((7 * (mx - mn)) / 16)) and v2 <= (((13 * (mx - mn)) / 16) + mn):
            x4 = mn + ((3 * (mx - mn)) / 4)
        else:
            x4 = 0.0
        if (v1 >= (mn + ((3 * (mx - mn)) / 8)) and v2 <= (((9 * (mx - mn)) / 8) + mn)) and x4 == 0:
            x5 = mx
        else:
            x5 = 0.0
        if ((((v1 >= (mn + ((mx - mn) / 8)) and v2 <= (((7 * (mx - mn)) / 8) + mn)) and x1 == 0) and x2 == 0) and x4 == 0) and x5 == 0:
            x3 = mn + ((3 * (mx - mn)) / 4)
        else:
            x3 = 0.0
        if (x1 + x2 + x3 + x4 + x5) == 0:
            x6 = mx
        else:
            x6 = 0.0
        finalH = x1 + x2 + x3 + x4 + x5 + x6
        y1 = 0.0
        y2 = 0.0
        y3 = 0.0
        y4 = 0.0
        y5 = 0.0
        y6 = 0.0
        if x1 > 0:
            y1 = mn
        else:
            y1 = 0.0
        if x2 > 0:
            y2 = mn + ((mx - mn) / 4)
        else:
            y2 = 0.0
        if x3 > 0:
            y3 = mn + ((mx - mn) / 4)
        else:
            y3 = 0.0
        if x4 > 0:
            y4 = mn + ((mx - mn) / 2)
        else:
            y4 = 0.0
        if x5 > 0:
            y5 = mn + ((mx - mn) / 2)
        else:
            y5 = 0.0
        if finalH > 0 and (y1 + y2 + y3 + y4 + y5) == 0:
            y6 = mn
        else:
            y6 = 0.0
        finalL = y1 + y2 + y3 + y4 + y5 + y6
        dmml = (finalH - finalL) / 8
        mml[0] = finalL - (dmml * 2)
        for i in range(1, OctLinesCnt):
            mml[i] = mml[i - 1] + dmml
        first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
        if first_bar == 0:
            return 0
        if LabelSide == Right:
            first_bar = 1
        for i in range(0, OctLinesCnt):
            name = ObjectPrefix + IntegerToString(i)
            if ObjectFind(0, name) == -1:
                ObjectCreate(0, name, OBJ_HLINE, 0, Time[0], mml[i])
                ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
                ObjectSetInteger(0, name, OBJPROP_COLOR, mml_clr[i])
                ObjectSetInteger(0, name, OBJPROP_WIDTH, mml_wdth[i])
            else:
                ObjectMove(0, name, 0, Time[0], mml[i])
            name = ObjectPrefix + 'txt' + IntegerToString(i)
            if ObjectFind(0, name) == -1:
                ObjectCreate(0, name, OBJ_TEXT, 0, Time[first_bar - 1], mml[i])
                ObjectSetString(0, name, OBJPROP_TEXT, ln_txt[i])
                ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
                ObjectSetString(0, name, OBJPROP_FONT, FontFace)
                ObjectSetInteger(0, name, OBJPROP_COLOR, mml_clr[i])
                ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
            else:
                ObjectMove(0, name, 0, Time[first_bar - 1], mml[i])
        name = ObjectPrefix + 'LatestCalcBar'
        if ObjectFind(0, name) == -1:
            ObjectCreate(0, name, OBJ_ARROW, 0, Time[StepBack], Low[StepBack] - (2 * Point()))
            ObjectSetInteger(0, name, OBJPROP_ARROWCODE, MarkNumber)
            ObjectSetInteger(0, name, OBJPROP_COLOR, MarkColor)
        else:
            ObjectMove(0, name, 0, Time[StepBack], Low[StepBack] - (2 * Point()))
        nTime = Time[0]
    if ((not NativeAlerts) and (not EmailAlerts)) and (not NotificationAlerts):
        return rates_total
    for i in range(0, 13):
        Signal = 0
        if Close[TriggerCandle] > mml[i]:
            if Open[TriggerCandle] <= mml[i] or Close[TriggerCandle + 1] <= mml[i]:
                Signal = 1
        elif Close[TriggerCandle] < mml[i]:
            if Open[TriggerCandle] >= mml[i] or Close[TriggerCandle + 1] >= mml[i]:
                Signal = -1
        if prevSignal[i] == 42:
            prevSignal[i] = Signal
            continue
        if (TriggerCandle > 0 and Time[TriggerCandle] > LastAlertTime[i]) or TriggerCandle == 0:
            Text = ""
            TextNative = ""
            if Signal == 1 and prevSignal[i] != 1:
                Text = 'MMLX: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Breach Up: ' + ln_txt[i] + ' at ' + DoubleToString(mml[i], Digits()) + '.'
                TextNative = 'Breach Up: ' + ln_txt[i] + ' at ' + DoubleToString(mml[i], Digits()) + '.'
                DoAlerts(Text, TextNative)
                LastAlertTime[i] = Time[TriggerCandle]
            elif Signal == -1 and prevSignal[i] != -1:
                Text = 'MMLX: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Breach Down: ' + ln_txt[i] + ' at ' + DoubleToString(mml[i], Digits()) + '.'
                TextNative = 'Breach Down: ' + ln_txt[i] + ' at ' + DoubleToString(mml[i], Digits()) + '.'
                DoAlerts(Text, TextNative)
                LastAlertTime[i] = Time[TriggerCandle]
        prevSignal[i] = Signal
    return rates_total

def DoAlerts(Text, TextNative):
    if NativeAlerts:
        Alert(TextNative)
    if EmailAlerts:
        SendMail(Text, Text)
    if NotificationAlerts:
        SendNotification(Text)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MurreyMathLineX(_MQL5Indicator):
    name = 'Murrey_Math_Line_X'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 64,  # Period
        'UpperTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),
        'StepBack': 0,
        'LabelSide': _Choice({0: 'Left', 1: 'Right'}, default=0),
        'mml_wdth_m_2_8': 2,  # [-2]/8 Width
        'mml_wdth_m_1_8': 1,  # [-1]/8 Width
        'mml_wdth_0_8': 1,  # [0]/8 Width
        'mml_wdth_1_8': 1,  # [1]/8 Width
        'mml_wdth_2_8': 1,  # [2]/8 Width
        'mml_wdth_3_8': 1,  # [3]/8 Width
        'mml_wdth_4_8': 1,  # [4]/8 Width
        'mml_wdth_5_8': 1,  # [5]/8 Width
        'mml_wdth_6_8': 1,  # [6]/8 Width
        'mml_wdth_7_8': 1,  # [7]/8 Width
        'mml_wdth_8_8': 1,  # [8]/8 Width
        'mml_wdth_p_1_8': 1,  # [+1]/8 Width
        'mml_wdth_p_2_8': 2,  # [+2]/8 Width
        'MarkNumber': 217,
        'FontSize': 10,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
        'NativeAlerts': False,
        'EmailAlerts': False,
        'NotificationAlerts': False,
    }

