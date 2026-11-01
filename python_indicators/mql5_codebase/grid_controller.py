"""Grid_Controller — converted from MQL5: MQL5 Indicators/Horizontal Grid Controller/Grid_Controller.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Grid_Controller', 'source': 'MQL5 Indicators/Horizontal Grid Controller/Grid_Controller.mq5', 'folder': 'Horizontal Grid Controller', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'int', 'default': 50, 'label': 'vertical grid step in points', 'sinput': False}, {'mql': 'Figure', 'py': 'Figure', 'param': 'Figure', 'type': 'int', 'default': 1000, 'label': 'figure step', 'sinput': False}, {'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 0, 'label': 'bars in history (0 - all history)', 'sinput': False}, {'mql': 'new_Hfigure', 'py': 'new_Hfigure', 'param': None, 'type': 'color', 'default': 6908265, 'label': 'new figure', 'sinput': False}, {'mql': 'new_Hline', 'py': 'new_Hline', 'param': None, 'type': 'color', 'default': 6908265, 'label': 'new line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
Step = _input('Step', 50)  # vertical grid step in points
Figure = _input('Figure', 1000)  # figure step
MaxBars = _input('MaxBars', 0)  # bars in history (0 - all history)
new_Hfigure = _input('new_Hfigure', clrDimGray)  # new figure
new_Hline = _input('new_Hline', clrDimGray)  # new line
step = 0
prefix = 'grid_'
old_Times = Arr.of([0], fill=0, dyn=False, size=21)  # array for old times
line_name = ""  # line name
line_counter = 0  # line counter
start_pos = 0  # starting position
start_time = 0

def OnInit():
    global step
    CheckOtherTimeFrames(Symbol())
    step = Step
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global start_pos
    if rates_total < 0:
        return 0
    if not CheckOtherTimeFrames(Symbol()):
        return prev_calculated
    if prev_calculated == 0:
        Play()
        if MaxBars != 0:
            if MaxBars < rates_total:
                start_pos = rates_total - MaxBars
    else:
        start_pos = prev_calculated - 1
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global step
    if id_ == CHARTEVENT_KEYDOWN:
        _sw1 = _int(lparam)
        if _sw1 == 76:
            if step >= 1:
                step = step + 1
                Play()
        elif _sw1 == 75:
            if step >= 1:
                step = step - 1
                Play()
        elif _sw1 == 74:
            if step >= 1:
                step = Step
                Play()

def Play():
    global line_counter, line_name, start_pos, start_time
    line_name = ''
    line_counter = 0
    start_pos = 0
    start_time = GetTickCount()
    ObjectsDeleteAll(0, prefix)
    Ris_H_Line()
    ArrayInitialize(old_Times, 0)
    Comment('Steps ', step)

def SetHLine(nm, p1, cl=_uint(Red)):
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_HLINE, 0, 0, p1)
    ObjectSetInteger(0, nm, OBJPROP_COLOR, cl)
    ObjectSetInteger(0, nm, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, nm, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)

def Ris_H_Line():
    global line_counter
    Uroven = 0.0
    rez = 0
    i = 0
    line_counter = 0
    mass = Arr(0, 0.0)
    max_ = 10.0
    min_ = 0.0
    index = 0
    ArraySetAsSeries(mass, True)
    if CopyHigh(Symbol(), PERIOD_MN1, 0, Bars(Symbol(), PERIOD_MN1), mass) > 2:
        index = ArrayMaximum(mass, 0, WHOLE_ARRAY)
        CopyHigh(Symbol(), PERIOD_MN1, index, 1, mass)
        max_ = mass[0]
    if CopyLow(Symbol(), PERIOD_MN1, 0, Bars(Symbol(), PERIOD_MN1), mass) > 2:
        index = ArrayMinimum(mass, 0, WHOLE_ARRAY)
        CopyLow(Symbol(), PERIOD_MN1, index, 1, mass)
        min_ = mass[0]
    while Uroven <= max_:
        i += 1
        Uroven = i * step * Point()
        if Uroven >= min_:
            line_counter += 1
            rez = _int(MathMod(Uroven * MathPow(10, Digits()), Figure))
            if rez == 0:
                if Period() < PERIOD_W1:
                    SetHLine(prefix + 'HLine_' + _str(line_counter), Uroven, new_Hfigure)
            elif Period() < PERIOD_M30:
                SetHLine(prefix + 'HLine_' + _str(line_counter), Uroven, new_Hline)
    ChartRedraw()

def CheckOtherTimeFrames(symbol):
    ctm = Arr(1, 0, dyn=False)
    checktime = TimeGMT() - (86400 * 60)
    res = True
    if CopyTime(symbol, PERIOD_H1, _DT(checktime), 1, ctm) != 1:
        res = False
    if CopyTime(symbol, PERIOD_D1, _DT(checktime), 1, ctm) != 1:
        res = False
    if CopyTime(symbol, PERIOD_W1, _DT(checktime), 1, ctm) != 1:
        res = False
    if CopyTime(symbol, PERIOD_MN1, _DT(checktime), 1, ctm) != 1:
        res = False
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GridController(_MQL5Indicator):
    name = 'Grid_Controller'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 50,  # vertical grid step in points
        'Figure': 1000,  # figure step
        'MaxBars': 0,  # bars in history (0 - all history)
    }

