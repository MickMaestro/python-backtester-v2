"""mmlevls_vg — converted from MQL5: MQL5 Indicators/Murrey Math Lines for the Current Bar/mmlevls_vg.mq5

Copyright: Copyright © 2006, Vladislav Goshkov (VG).; Link: 4vg@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Vladislav Goshkov (VG).', 'link': '4vg@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'mmlevls_vg', 'source': 'MQL5 Indicators/Murrey Math Lines for the Current Bar/mmlevls_vg.mq5', 'folder': 'Murrey Math Lines for the Current Bar', 'inputs': [{'mql': 'P', 'py': 'P', 'param': 'P', 'type': 'int', 'default': 90, 'label': '', 'sinput': False}, {'mql': 'MMPeriod', 'py': 'MMPeriod', 'param': 'MMPeriod', 'type': 'int', 'default': 16408, 'label': '', 'sinput': False}, {'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'int', 'default': 0, 'label': 'Bar index for levels calculation', 'sinput': False}, {'mql': 'mml_clr_m_2_8', 'py': 'mml_clr_m_2_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[-2]/8 level color', 'sinput': False}, {'mql': 'mml_clr_m_1_8', 'py': 'mml_clr_m_1_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[-1]/8 level color', 'sinput': False}, {'mql': 'mml_clr_0_8', 'py': 'mml_clr_0_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[0]/8 level color', 'sinput': False}, {'mql': 'mml_clr_1_8', 'py': 'mml_clr_1_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[1]/8 level color', 'sinput': False}, {'mql': 'mml_clr_2_8', 'py': 'mml_clr_2_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[2]/8 level color', 'sinput': False}, {'mql': 'mml_clr_3_8', 'py': 'mml_clr_3_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[3]/8 level color', 'sinput': False}, {'mql': 'mml_clr_4_8', 'py': 'mml_clr_4_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[4]/8 level color', 'sinput': False}, {'mql': 'mml_clr_5_8', 'py': 'mml_clr_5_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[5]/8 level color', 'sinput': False}, {'mql': 'mml_clr_6_8', 'py': 'mml_clr_6_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[6]/8 level color', 'sinput': False}, {'mql': 'mml_clr_7_8', 'py': 'mml_clr_7_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[7]/8 level color', 'sinput': False}, {'mql': 'mml_clr_8_8', 'py': 'mml_clr_8_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[8]/8 level color', 'sinput': False}, {'mql': 'mml_clr_p_1_8', 'py': 'mml_clr_p_1_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[+1]/8 level color', 'sinput': False}, {'mql': 'mml_clr_p_2_8', 'py': 'mml_clr_p_2_8', 'param': None, 'type': 'color', 'default': 0, 'label': '[+2]/8 level color', 'sinput': False}, {'mql': 'mml_style_m_2_8', 'py': 'mml_style_m_2_8', 'param': 'mml_style_m_2_8', 'type': 'int', 'default': 0, 'label': '[-2]/8 level line style', 'sinput': False}, {'mql': 'mml_style_m_1_8', 'py': 'mml_style_m_1_8', 'param': 'mml_style_m_1_8', 'type': 'int', 'default': 4, 'label': '[-1]/8 level line style', 'sinput': False}, {'mql': 'mml_style_0_8', 'py': 'mml_style_0_8', 'param': 'mml_style_0_8', 'type': 'int', 'default': 4, 'label': '[0]/8 level line style', 'sinput': False}, {'mql': 'mml_style_1_8', 'py': 'mml_style_1_8', 'param': 'mml_style_1_8', 'type': 'int', 'default': 4, 'label': '[1]/8 level line style', 'sinput': False}, {'mql': 'mml_style_2_8', 'py': 'mml_style_2_8', 'param': 'mml_style_2_8', 'type': 'int', 'default': 4, 'label': '[2]/8 level line style', 'sinput': False}, {'mql': 'mml_style_3_8', 'py': 'mml_style_3_8', 'param': 'mml_style_3_8', 'type': 'int', 'default': 4, 'label': '[3]/8 level line style', 'sinput': False}, {'mql': 'mml_style_4_8', 'py': 'mml_style_4_8', 'param': 'mml_style_4_8', 'type': 'int', 'default': 4, 'label': '[4]/8 level line style', 'sinput': False}, {'mql': 'mml_style_5_8', 'py': 'mml_style_5_8', 'param': 'mml_style_5_8', 'type': 'int', 'default': 4, 'label': '[5]/8 level line style', 'sinput': False}, {'mql': 'mml_style_6_8', 'py': 'mml_style_6_8', 'param': 'mml_style_6_8', 'type': 'int', 'default': 4, 'label': '[6]/8 level line style', 'sinput': False}, {'mql': 'mml_style_7_8', 'py': 'mml_style_7_8', 'param': 'mml_style_7_8', 'type': 'int', 'default': 4, 'label': '[7]/8 level line style', 'sinput': False}, {'mql': 'mml_style_8_8', 'py': 'mml_style_8_8', 'param': 'mml_style_8_8', 'type': 'int', 'default': 4, 'label': '[8]/8 level line style', 'sinput': False}, {'mql': 'mml_style_p_1_8', 'py': 'mml_style_p_1_8', 'param': 'mml_style_p_1_8', 'type': 'int', 'default': 4, 'label': '[+1]/8 level line style', 'sinput': False}, {'mql': 'mml_style_p_2_8', 'py': 'mml_style_p_2_8', 'param': 'mml_style_p_2_8', 'type': 'int', 'default': 0, 'label': '[+2]/8 level line style', 'sinput': False}, {'mql': 'mml_wdth_m_2_8', 'py': 'mml_wdth_m_2_8', 'param': 'mml_wdth_m_2_8', 'type': 'int', 'default': 1, 'label': '[-2]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_m_1_8', 'py': 'mml_wdth_m_1_8', 'param': 'mml_wdth_m_1_8', 'type': 'int', 'default': 1, 'label': '[-1]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_0_8', 'py': 'mml_wdth_0_8', 'param': 'mml_wdth_0_8', 'type': 'int', 'default': 1, 'label': '[0]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_1_8', 'py': 'mml_wdth_1_8', 'param': 'mml_wdth_1_8', 'type': 'int', 'default': 1, 'label': '[1]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_2_8', 'py': 'mml_wdth_2_8', 'param': 'mml_wdth_2_8', 'type': 'int', 'default': 1, 'label': '[2]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_3_8', 'py': 'mml_wdth_3_8', 'param': 'mml_wdth_3_8', 'type': 'int', 'default': 1, 'label': '[3]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_4_8', 'py': 'mml_wdth_4_8', 'param': 'mml_wdth_4_8', 'type': 'int', 'default': 1, 'label': '[4]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_5_8', 'py': 'mml_wdth_5_8', 'param': 'mml_wdth_5_8', 'type': 'int', 'default': 1, 'label': '[5]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_6_8', 'py': 'mml_wdth_6_8', 'param': 'mml_wdth_6_8', 'type': 'int', 'default': 1, 'label': '[6]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_7_8', 'py': 'mml_wdth_7_8', 'param': 'mml_wdth_7_8', 'type': 'int', 'default': 1, 'label': '[7]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_8_8', 'py': 'mml_wdth_8_8', 'param': 'mml_wdth_8_8', 'type': 'int', 'default': 1, 'label': '[8]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_p_1_8', 'py': 'mml_wdth_p_1_8', 'param': 'mml_wdth_p_1_8', 'type': 'int', 'default': 1, 'label': '[+1]/8 level width', 'sinput': False}, {'mql': 'mml_wdth_p_2_8', 'py': 'mml_wdth_p_2_8', 'param': 'mml_wdth_p_2_8', 'type': 'int', 'default': 1, 'label': '[+2]/8 level width', 'sinput': False}, {'mql': 'MarkColor', 'py': 'MarkColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Label color', 'sinput': False}, {'mql': 'MarkNumber', 'py': 'MarkNumber', 'param': 'MarkNumber', 'type': 'int', 'default': 217, 'label': 'Label index', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Levels font', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'Font size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# enum STYLE
STYLE_SOLID_ = 0
STYLE_DASH_ = 1
STYLE_DOT_ = 2
STYLE_DASHDOT_ = 3
STYLE_DASHDOTDOT_ = 4
_enum('STYLE', {0: 'STYLE_SOLID_', 1: 'STYLE_DASH_', 2: 'STYLE_DOT_', 3: 'STYLE_DASHDOT_', 4: 'STYLE_DASHDOTDOT_'})

# ---- inputs and global variables
P = _input('P', 90)
MMPeriod = _input('MMPeriod', PERIOD_D1)
StepBack = _input('StepBack', 0)  # Bar index for levels calculation
mml_style_m_2_8 = _input('mml_style_m_2_8', STYLE_SOLID)  # [-2]/8 level line style
mml_style_m_1_8 = _input('mml_style_m_1_8', STYLE_DASHDOTDOT)  # [-1]/8 level line style
mml_style_0_8 = _input('mml_style_0_8', STYLE_DASHDOTDOT)  # [0]/8 level line style
mml_style_1_8 = _input('mml_style_1_8', STYLE_DASHDOTDOT)  # [1]/8 level line style
mml_style_2_8 = _input('mml_style_2_8', STYLE_DASHDOTDOT)  # [2]/8 level line style
mml_style_3_8 = _input('mml_style_3_8', STYLE_DASHDOTDOT)  # [3]/8 level line style
mml_style_4_8 = _input('mml_style_4_8', STYLE_DASHDOTDOT)  # [4]/8 level line style
mml_style_5_8 = _input('mml_style_5_8', STYLE_DASHDOTDOT)  # [5]/8 level line style
mml_style_6_8 = _input('mml_style_6_8', STYLE_DASHDOTDOT)  # [6]/8 level line style
mml_style_7_8 = _input('mml_style_7_8', STYLE_DASHDOTDOT)  # [7]/8 level line style
mml_style_8_8 = _input('mml_style_8_8', STYLE_DASHDOTDOT)  # [8]/8 level line style
mml_style_p_1_8 = _input('mml_style_p_1_8', STYLE_DASHDOTDOT)  # [+1]/8 level line style
mml_style_p_2_8 = _input('mml_style_p_2_8', STYLE_SOLID)  # [+2]/8 level line style
mml_wdth_m_2_8 = _input('mml_wdth_m_2_8', 1)  # [-2]/8 level width
mml_wdth_m_1_8 = _input('mml_wdth_m_1_8', 1)  # [-1]/8 level width
mml_wdth_0_8 = _input('mml_wdth_0_8', 1)  # [0]/8 level width
mml_wdth_1_8 = _input('mml_wdth_1_8', 1)  # [1]/8 level width
mml_wdth_2_8 = _input('mml_wdth_2_8', 1)  # [2]/8 level width
mml_wdth_3_8 = _input('mml_wdth_3_8', 1)  # [3]/8 level width
mml_wdth_4_8 = _input('mml_wdth_4_8', 1)  # [4]/8 level width
mml_wdth_5_8 = _input('mml_wdth_5_8', 1)  # [5]/8 level width
mml_wdth_6_8 = _input('mml_wdth_6_8', 1)  # [6]/8 level width
mml_wdth_7_8 = _input('mml_wdth_7_8', 1)  # [7]/8 level width
mml_wdth_8_8 = _input('mml_wdth_8_8', 1)  # [8]/8 level width
mml_wdth_p_1_8 = _input('mml_wdth_p_1_8', 1)  # [+1]/8 level width
mml_wdth_p_2_8 = _input('mml_wdth_p_2_8', 1)  # [+2]/8 level width
MarkNumber = _input('MarkNumber', 217)  # Label index
Font = _input('Font', 'Arial')  # Levels font
FontSize = _input('FontSize', 11)  # Font size
dmml = 0.0
dvtl = 0.0
sum_ = 0.0
v1 = 0.0
v2 = 0.0
mn = 0.0
mx = 0.0
x1 = 0.0
x2 = 0.0
x3 = 0.0
x4 = 0.0
x5 = 0.0
x6 = 0.0
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0
y5 = 0.0
y6 = 0.0
octave = 0.0
fractal = 0.0
range_ = 0.0
finalH = 0.0
finalL = 0.0
mml = Arr(13, 0.0, dyn=False)
ln_txt = Arr(13, "", dyn=False)
buff_str = ''
bn_v1 = 0
bn_v2 = 0
OctLinesCnt = 13
mml_thk = 8
mml_clr = Arr(13, 0, dyn=False)
mml_wdth = Arr(13, 0, dyn=False)
mml_style = Arr(13, 0, dyn=False)
mml_shft = 35
ntime = 0
CurPeriod = 0
nDigits = 0
NewPeriod = 0
CurPeriod_ = 0

def OnInit():
    global CurPeriod_, NewPeriod, mml_thk
    CurPeriod_ = _idiv(PeriodSeconds(PERIOD_CURRENT), 60)
    if MMPeriod > 0:
        NewPeriod = P * _int(MathCeil(_idiv(PeriodSeconds(MMPeriod), PeriodSeconds(PERIOD_CURRENT))))
    else:
        NewPeriod = P
    ln_txt[0] = '[-2/8]P'
    ln_txt[1] = '[-1/8]P'
    ln_txt[2] = '[0/8]P'
    ln_txt[3] = '[1/8]P'
    ln_txt[4] = '[2/8]P'
    ln_txt[5] = '[3/8]P'
    ln_txt[6] = '[4/8]P'
    ln_txt[7] = '[5/8]P'
    ln_txt[8] = '[6/8]P'
    ln_txt[9] = '[7/8]P'
    ln_txt[10] = '[8/8]P'
    ln_txt[11] = '[+1/8]P'
    ln_txt[12] = '[+2/8]P'
    mml_thk = 3
    mml_clr[0] = mml_clr_m_2_8
    mml_style[0] = mml_style_m_2_8
    mml_wdth[0] = mml_wdth_m_2_8
    mml_clr[1] = mml_clr_m_1_8
    mml_style[1] = mml_style_m_1_8
    mml_wdth[1] = mml_wdth_m_1_8
    mml_clr[2] = mml_clr_0_8
    mml_style[2] = mml_style_0_8
    mml_wdth[2] = mml_wdth_0_8
    mml_clr[3] = mml_clr_1_8
    mml_style[3] = mml_style_1_8
    mml_wdth[3] = mml_wdth_1_8
    mml_clr[4] = mml_clr_2_8
    mml_style[4] = mml_style_2_8
    mml_wdth[4] = mml_wdth_2_8
    mml_clr[5] = mml_clr_3_8
    mml_style[5] = mml_style_3_8
    mml_wdth[5] = mml_wdth_3_8
    mml_clr[6] = mml_clr_4_8
    mml_style[6] = mml_style_3_8
    mml_wdth[6] = mml_wdth_3_8
    mml_clr[7] = mml_clr_5_8
    mml_style[7] = mml_style_5_8
    mml_wdth[7] = mml_wdth_5_8
    mml_clr[8] = mml_clr_6_8
    mml_style[8] = mml_style_6_8
    mml_wdth[8] = mml_wdth_6_8
    mml_clr[9] = mml_clr_7_8
    mml_style[9] = mml_style_7_8
    mml_wdth[9] = mml_wdth_7_8
    mml_clr[10] = mml_clr_8_8
    mml_style[10] = mml_style_8_8
    mml_wdth[10] = mml_wdth_8_8
    mml_clr[11] = mml_clr_p_1_8
    mml_style[11] = mml_style_p_1_8
    mml_wdth[11] = mml_wdth_p_1_8
    mml_clr[12] = mml_clr_p_2_8
    mml_style[12] = mml_style_p_2_8
    mml_wdth[12] = mml_wdth_p_2_8

def OnDeinit(reason):
    for i in range(0, OctLinesCnt):
        ObjectDelete(0, 'mml' + IntegerToString(i))
        ObjectDelete(0, 'mml_txt' + IntegerToString(i))
    ObjectDelete(0, 'LR_LatestCulcBar')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global CurPeriod, NewPeriod, bn_v1, bn_v2, buff_str, dmml, finalH, finalL, fractal, mn, mx, ntime, octave, range_, sum_, v1, v2, x1, x2, x3, x4, x5, x6, y1, y2, y3, y4, y5, y6
    if rates_total < P:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    i = 0
    if ntime != time[0] or CurPeriod != CurPeriod_:
        Print('MMLevls : NewPeriod = ', NewPeriod)
        if NewPeriod > rates_total:
            NewPeriod = rates_total
        bn_v1 = ArrayMinimum(low, StepBack, NewPeriod)
        bn_v2 = ArrayMaximum(high, StepBack, NewPeriod)
        v1 = low[bn_v1]
        v2 = high[bn_v2]
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
        sum_ = MathFloor(_fdiv(MathLog(_fdiv(fractal, range_)), MathLog(2.0)))
        octave = fractal * MathPow(0.5, sum_)
        mn = MathFloor(_fdiv(v1, octave)) * octave
        if (mn + octave) > v2:
            mx = mn + octave
        else:
            mx = mn + (2 * octave)
        if v1 >= (((3 * (mx - mn)) / 16.0) + mn) and v2 <= (((9 * (mx - mn)) / 16) + mn):
            x2 = mn + ((mx - mn) / 2.0)
        else:
            x2 = 0.0
        if (v1 >= (mn - ((mx - mn) / 8.0)) and v2 <= (((5 * (mx - mn)) / 8) + mn)) and x2 == 0:
            x1 = mn + ((mx - mn) / 2.0)
        else:
            x1 = 0.0
        if v1 >= (mn + ((7 * (mx - mn)) / 16.0)) and v2 <= (((13 * (mx - mn)) / 16) + mn):
            x4 = mn + ((3 * (mx - mn)) / 4.0)
        else:
            x4 = 0.0
        if (v1 >= (mn + ((3 * (mx - mn)) / 8.0)) and v2 <= (((9 * (mx - mn)) / 8) + mn)) and x4 == 0:
            x5 = mx
        else:
            x5 = 0.0
        if ((((v1 >= (mn + ((mx - mn) / 8)) and v2 <= (((7 * (mx - mn)) / 8) + mn)) and x1 == 0) and x2 == 0) and x4 == 0) and x5 == 0:
            x3 = mn + ((3 * (mx - mn)) / 4.0)
        else:
            x3 = 0.0
        if (x1 + x2 + x3 + x4 + x5) == 0:
            x6 = mx
        else:
            x6 = 0.0
        finalH = x1 + x2 + x3 + x4 + x5 + x6
        if x1 > 0:
            y1 = mn
        else:
            y1 = 0.0
        if x2 > 0:
            y2 = mn + ((mx - mn) / 4.0)
        else:
            y2 = 0.0
        if x3 > 0:
            y3 = mn + ((mx - mn) / 4.0)
        else:
            y3 = 0.0
        if x4 > 0:
            y4 = mn + ((mx - mn) / 2.0)
        else:
            y4 = 0.0
        if x5 > 0:
            y5 = mn + ((mx - mn) / 2.0)
        else:
            y5 = 0.0
        if finalH > 0 and (y1 + y2 + y3 + y4 + y5) == 0:
            y6 = mn
        else:
            y6 = 0.0
        finalL = y1 + y2 + y3 + y4 + y5 + y6
        i = 0
        for i in range(i, OctLinesCnt):
            mml[i] = 0.0
        else:
            i = _range_end(i, OctLinesCnt, 1)
        dmml = (finalH - finalL) / 8.0
        Print('MMLevls : NewPeriod = ', NewPeriod, ' dmml = ', dmml, ' finalL = ', finalL)
        mml[0] = finalL - (dmml * 2.0)
        i = 1
        for i in range(i, OctLinesCnt):
            mml[i] = mml[i - 1] + dmml
        else:
            i = _range_end(i, OctLinesCnt, 1)
        i = 0
        for i in range(i, OctLinesCnt):
            buff_str = 'mml' + IntegerToString(i)
            if ObjectFind(0, buff_str) == -1:
                ObjectCreate(0, buff_str, OBJ_HLINE, 0, time[0], mml[i])
                ObjectSetInteger(0, buff_str, OBJPROP_COLOR, mml_clr[i])
                ObjectSetInteger(0, buff_str, OBJPROP_WIDTH, mml_wdth[i])
                ObjectSetInteger(0, buff_str, OBJPROP_STYLE, mml_style[i])
                ObjectSetInteger(0, buff_str, OBJPROP_BACK, True)
            else:
                ObjectMove(0, buff_str, 0, time[0], mml[i])
            buff_str = 'mml_txt' + IntegerToString(i)
            if ObjectFind(0, buff_str) == -1:
                ObjectCreate(0, buff_str, OBJ_TEXT, 0, time[mml_shft], mml_shft)
                ObjectSetString(0, buff_str, OBJPROP_TEXT, ln_txt[i])
                ObjectSetString(0, buff_str, OBJPROP_FONT, Font)
                ObjectSetInteger(0, buff_str, OBJPROP_FONTSIZE, FontSize)
                ObjectSetInteger(0, buff_str, OBJPROP_COLOR, mml_clr[i])
                ObjectMove(0, buff_str, 0, time[mml_shft], mml[i])
            else:
                ObjectMove(0, buff_str, 0, time[mml_shft], mml[i])
        else:
            i = _range_end(i, OctLinesCnt, 1)
        ntime = _int(time[0])
        CurPeriod = CurPeriod_
        buff_str_ = 'LR_LatestCulcBar'
        if ObjectFind(0, buff_str_) == -1:
            ObjectCreate(0, buff_str_, OBJ_ARROW, 0, time[StepBack], low[StepBack] - (2 * Point()))
            ObjectSetInteger(0, buff_str_, OBJPROP_ARROWCODE, MarkNumber)
            ObjectSetInteger(0, buff_str_, OBJPROP_COLOR, MarkColor)
        else:
            ObjectMove(0, buff_str_, 0, time[StepBack], low[StepBack] - (2 * Point()))
    return rates_total

# ---- global variables initialised from expressions
mml_clr_m_2_8 = _input('mml_clr_m_2_8', _uint(Gray))  # [-2]/8 level color
mml_clr_m_1_8 = _input('mml_clr_m_1_8', _uint(Gray))  # [-1]/8 level color
mml_clr_0_8 = _input('mml_clr_0_8', _uint(Aqua))  # [0]/8 level color
mml_clr_1_8 = _input('mml_clr_1_8', _uint(Yellow))  # [1]/8 level color
mml_clr_2_8 = _input('mml_clr_2_8', _uint(Red))  # [2]/8 level color
mml_clr_3_8 = _input('mml_clr_3_8', _uint(Green))  # [3]/8 level color
mml_clr_4_8 = _input('mml_clr_4_8', _uint(Blue))  # [4]/8 level color
mml_clr_5_8 = _input('mml_clr_5_8', _uint(Green))  # [5]/8 level color
mml_clr_6_8 = _input('mml_clr_6_8', _uint(Red))  # [6]/8 level color
mml_clr_7_8 = _input('mml_clr_7_8', _uint(Yellow))  # [7]/8 level color
mml_clr_8_8 = _input('mml_clr_8_8', _uint(Aqua))  # [8]/8 level color
mml_clr_p_1_8 = _input('mml_clr_p_1_8', _uint(Gray))  # [+1]/8 level color
mml_clr_p_2_8 = _input('mml_clr_p_2_8', _uint(Gray))  # [+2]/8 level color
MarkColor = _input('MarkColor', _uint(Red))  # Label color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MmlevlsVg(_MQL5Indicator):
    name = 'mmlevls_vg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'P': 90,
        'MMPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),
        'StepBack': 0,  # Bar index for levels calculation
        'mml_style_m_2_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # [-2]/8 level line style
        'mml_style_m_1_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [-1]/8 level line style
        'mml_style_0_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [0]/8 level line style
        'mml_style_1_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [1]/8 level line style
        'mml_style_2_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [2]/8 level line style
        'mml_style_3_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [3]/8 level line style
        'mml_style_4_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [4]/8 level line style
        'mml_style_5_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [5]/8 level line style
        'mml_style_6_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [6]/8 level line style
        'mml_style_7_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [7]/8 level line style
        'mml_style_8_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [8]/8 level line style
        'mml_style_p_1_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # [+1]/8 level line style
        'mml_style_p_2_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # [+2]/8 level line style
        'mml_wdth_m_2_8': 1,  # [-2]/8 level width
        'mml_wdth_m_1_8': 1,  # [-1]/8 level width
        'mml_wdth_0_8': 1,  # [0]/8 level width
        'mml_wdth_1_8': 1,  # [1]/8 level width
        'mml_wdth_2_8': 1,  # [2]/8 level width
        'mml_wdth_3_8': 1,  # [3]/8 level width
        'mml_wdth_4_8': 1,  # [4]/8 level width
        'mml_wdth_5_8': 1,  # [5]/8 level width
        'mml_wdth_6_8': 1,  # [6]/8 level width
        'mml_wdth_7_8': 1,  # [7]/8 level width
        'mml_wdth_8_8': 1,  # [8]/8 level width
        'mml_wdth_p_1_8': 1,  # [+1]/8 level width
        'mml_wdth_p_2_8': 1,  # [+2]/8 level width
        'MarkNumber': 217,  # Label index
        'FontSize': 11,  # Font size
    }

