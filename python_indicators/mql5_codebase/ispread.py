"""ispread — converted from MQL5: MQL5 Indicators/iSpread is a spread indicator for pair trading/ispread.mq5

Copyright: A.V. Oreshkin; Link: vk.com/mtforex; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'A.V. Oreshkin', 'link': 'vk.com/mtforex', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [16776960], 2: [255], 3: [65535], 4: [32768], 5: [255], 6: [65535], 7: [32768]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'SNT', 2: 'L1 UP', 3: 'L2 UP', 4: 'L3 UP', 5: 'L1 DN', 6: 'L2 DN', 7: 'L3 DN'}, 'levels': [0.0, 1.0, -1.0], 'description': [], 'name': 'ispread', 'source': 'MQL5 Indicators/iSpread is a spread indicator for pair trading/ispread.mq5', 'folder': 'iSpread is a spread indicator for pair trading', 'inputs': [{'mql': 'BeginTime', 'py': 'BeginTime', 'param': None, 'type': 'datetime', 'default': 1356998400, 'label': 'Date to start', 'sinput': False}, {'mql': 'Symbol1', 'py': 'Symbol1', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Symbol 1', 'sinput': False}, {'mql': 'Symbol2', 'py': 'Symbol2', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Symbol 2', 'sinput': False}, {'mql': 'Action', 'py': 'Action', 'param': 'Action', 'type': 'int', 'default': 4, 'label': 'Action', 'sinput': False}, {'mql': 'Invert1', 'py': 'Invert1', 'param': 'Invert1', 'type': 'bool', 'default': False, 'label': 'Reverse of symbol 1', 'sinput': False}, {'mql': 'Invert2', 'py': 'Invert2', 'param': 'Invert2', 'type': 'bool', 'default': False, 'label': 'Reverse of symbol 2', 'sinput': False}, {'mql': 'Pow1', 'py': 'Pow1', 'param': 'Pow1', 'type': 'double', 'default': 1.0, 'label': 'Power of symbol 1', 'sinput': False}, {'mql': 'Pow2', 'py': 'Pow2', 'param': 'Pow2', 'type': 'double', 'default': 1.0, 'label': 'Power of symbol 2', 'sinput': False}, {'mql': 'Multi1', 'py': 'Multi1', 'param': 'Multi1', 'type': 'double', 'default': 1.0, 'label': 'Multiplier of symbol 1', 'sinput': False}, {'mql': 'Multi2', 'py': 'Multi2', 'param': 'Multi2', 'type': 'double', 'default': 1.0, 'label': 'Multiplier of symbol 2', 'sinput': False}, {'mql': 'Ln', 'py': 'Ln', 'param': 'Ln', 'type': 'bool', 'default': False, 'label': 'The logarithm', 'sinput': False}, {'mql': 'Average', 'py': 'Average', 'param': 'Average', 'type': 'uint', 'default': 3, 'label': 'Smoothing.Period', 'sinput': False}, {'mql': 'Algo', 'py': 'Algo', 'param': 'Algo', 'type': 'int', 'default': 2, 'label': 'Selecting an algorithm', 'sinput': False}, {'mql': 'Window', 'py': 'Window', 'param': 'Window', 'type': 'uint', 'default': 288, 'label': 'Period for the algorithm', 'sinput': False}, {'mql': 'Screen_Levels', 'py': 'Screen_Levels', 'param': 'Screen_Levels', 'type': 'bool', 'default': True, 'label': 'Show levels', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 1, 'label': 'Levels calculation method', 'sinput': False}, {'mql': 'Levels', 'py': 'Levels', 'param': 'Levels', 'type': 'double', 'default': 1.0, 'label': 'Ratio of levels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MOVE
Subtract = 1
Add = 2
Multiply = 3
Divizion = 4
_enum('MOVE', {1: 'Subtract', 2: 'Add', 3: 'Multiply', 4: 'Divizion'})

# enum DET
Returns = 1
DeTrend = 2
_enum('DET', {1: 'Returns', 2: 'DeTrend'})

# enum LVL
Norm = 1
MaxMin = 2
_enum('LVL', {1: 'Norm', 2: 'MaxMin'})

# ---- inputs and global variables
BeginTime = _input('BeginTime', 1356998400)  # Date to start
Symbol1 = _input('Symbol1', 'GBPUSD')  # Symbol 1
Symbol2 = _input('Symbol2', 'EURUSD')  # Symbol 2
Action = _input('Action', Divizion)  # Action
Invert1 = _input('Invert1', False)  # Reverse of symbol 1
Invert2 = _input('Invert2', False)  # Reverse of symbol 2
Pow1 = _input('Pow1', 1.0)  # Power of symbol 1
Pow2 = _input('Pow2', 1.0)  # Power of symbol 2
Multi1 = _input('Multi1', 1.0)  # Multiplier of symbol 1
Multi2 = _input('Multi2', 1.0)  # Multiplier of symbol 2
Ln = _input('Ln', False)  # The logarithm
Average = _input('Average', 3)  # Smoothing.Period
Algo = _input('Algo', DeTrend)  # Selecting an algorithm
Window = _input('Window', 288)  # Period for the algorithm
Screen_Levels = _input('Screen_Levels', True)  # Show levels
Method = _input('Method', Norm)  # Levels calculation method
Levels = _input('Levels', 1.0)  # Ratio of levels
Error_Init = True
BeginDate = 0
BF = Arr(0, 0.0)  # The final array for the output
PR1 = Arr(0, 0.0)  # Arrays of initial data after mathematical processing
PR2 = Arr(0, 0.0)  # Arrays of initial data after mathematical processing
PRA1 = Arr(0, 0.0)  # Arrays PR1 and PR2 smoothed by a MA
PRA2 = Arr(0, 0.0)  # Arrays PR1 and PR2 smoothed by a MA
CALC = Arr(0, 0.0)  # Output here either after a detrend or after the first difference
DTR = Arr(0, 0.0)  # An array after detrend
LG1 = Arr(0, 0.0)  # An array for first differences
LG2 = Arr(0, 0.0)  # An array for first differences
max_ = 0.0  # Extreme for normalization
min_ = 0.0  # Extreme for normalization
L1up = Arr(0, 0.0)  # arrays for the levels
L2up = Arr(0, 0.0)  # arrays for the levels
L3up = Arr(0, 0.0)  # arrays for the levels
L1dn = Arr(0, 0.0)  # arrays for the levels
L2dn = Arr(0, 0.0)  # arrays for the levels
L3dn = Arr(0, 0.0)  # arrays for the levels

def OnInit():
    global Error_Init, max_, min_
    Error_Init = True
    LOAD_DATA()
    max_ = -10000.0
    min_ = 10000.0
    IndicatorSetString(INDICATOR_SHORTNAME, NAME())
    SetIndexBuffer(0, BF, INDICATOR_DATA)
    SetIndexBuffer(1, L1up, INDICATOR_DATA)
    SetIndexBuffer(2, L2up, INDICATOR_DATA)
    SetIndexBuffer(3, L3up, INDICATOR_DATA)
    SetIndexBuffer(4, L1dn, INDICATOR_DATA)
    SetIndexBuffer(5, L2dn, INDICATOR_DATA)
    SetIndexBuffer(6, L3dn, INDICATOR_DATA)
    SetIndexBuffer(7, PR1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, PR2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, PRA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, PRA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, CALC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, DTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, LG1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, LG2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BF, False)
    ArraySetAsSeries(PR1, False)
    ArraySetAsSeries(PR2, False)
    ArraySetAsSeries(PRA1, False)
    ArraySetAsSeries(PRA2, False)
    ArraySetAsSeries(CALC, False)
    ArraySetAsSeries(DTR, False)
    ArraySetAsSeries(LG1, False)
    ArraySetAsSeries(LG2, False)
    ArraySetAsSeries(L1up, False)
    ArraySetAsSeries(L2up, False)
    ArraySetAsSeries(L3up, False)
    ArraySetAsSeries(L1dn, False)
    ArraySetAsSeries(L2dn, False)
    ArraySetAsSeries(L3dn, False)
    ZeroMemory(L1up)
    ZeroMemory(L2up)
    ZeroMemory(L3up)
    ZeroMemory(L1dn)
    ZeroMemory(L2dn)
    ZeroMemory(L3dn)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global max_, min_
    if Error_Init:
        LOAD_DATA()
    if Error_Init:
        return INIT_FAILED
    pr1 = Arr(1, 0.0, dyn=False)
    pr2 = Arr(1, 0.0, dyn=False)
    x1 = 0
    x2 = 0
    limit = prev_calculated
    if limit > 1:
        limit = limit - 2
    for pos in range(1 + limit, rates_total):
        if time[pos] < BeginDate:
            EMTF(pos)
            continue
        x1 = CopyClose(Symbol1, PERIOD_CURRENT, _DT(time[pos]), 1, pr1)
        x2 = CopyClose(Symbol2, PERIOD_CURRENT, _DT(time[pos]), 1, pr2)
        if x1 <= 0 or x2 <= 0:
            EMTF(pos)
            Print('Data omission: ' + _str(time[pos]))
            continue
        if pr1[0] == 0 or pr2[0] == 0:
            EMTF(pos)
            Print('Zero data received: ' + _str(time[pos]))
            continue
        PR1[pos] = MODIFY(pr1[0], Invert1, Pow1, Multi1)
        PR2[pos] = MODIFY(pr2[0], Invert2, Pow2, Multi2)
    if Average > 1:
        for pos in range(1 + limit, rates_total):
            MA(pos)
    else:
        ArrayCopy(PRA1, PR1, 0, 0, WHOLE_ARRAY)
        ArrayCopy(PRA2, PR2, 0, 0, WHOLE_ARRAY)
    for pos in range(1 + limit, rates_total):
        CALC[pos] = ACTION(PRA1[pos], PRA2[pos])
    if Algo == DeTrend and Window > 1:
        for pos in range(1 + limit, rates_total):
            DT(pos)
            if DTR[pos] == EMPTY_VALUE:
                BF[pos] = EMPTY_VALUE
            else:
                BF[pos] = DTR[pos]
    elif Algo == Returns and Window > 0:
        for pos in range(1 + limit, rates_total):
            LAG(pos)
            if LG1[pos] == EMPTY_VALUE or LG2[pos] == EMPTY_VALUE:
                BF[pos] = EMPTY_VALUE
            else:
                BF[pos] = _fdiv(LG1[pos], LG2[pos]) - 1
    else:
        ArrayCopy(BF, CALC, 0, 0, WHOLE_ARRAY)
    if Screen_Levels and Window != 0:
        for pos in range(1 + limit, rates_total):
            if BF[pos] == EMPTY_VALUE:
                LCLEAR(pos)
                continue
            if Method <= 2:
                if BF[pos] > max_:
                    max_ = BF[pos]
                if BF[pos] < min_:
                    min_ = BF[pos]
                if Method == Norm:
                    if ((max_ - min_) != 0 and max_ != -10000) and min_ != 10000:
                        BF[pos] = _fdiv(BF[pos] - min_, max_ - min_) - 0.5
                        L1up[pos] = 0.125 * Levels
                        L2up[pos] = 2 * L1up[pos]
                        L3up[pos] = 3 * L1up[pos]
                        L1dn[pos] = -L1up[pos]
                        L2dn[pos] = -L2up[pos]
                        L3dn[pos] = -L3up[pos]
                    else:
                        LCLEAR(pos)
                if Method == MaxMin:
                    if max_ != -10000 and min_ != 10000:
                        L1up[pos] = (MathMax(MathAbs(max_), MathAbs(min_)) / 4) * Levels
                        L2up[pos] = 2 * L1up[pos]
                        L3up[pos] = 3 * L1up[pos]
                        L1dn[pos] = -L1up[pos]
                        L2dn[pos] = -L2up[pos]
                        L3dn[pos] = -L3up[pos]
                    else:
                        LCLEAR(pos)
    else:
        for pos in range(1 + limit, rates_total):
            LCLEAR(pos)
    return rates_total

def MODIFY(in_, inv, pw, ml):
    if inv:
        in_ = _fdiv(1, in_)
    in_ = MathPow(in_, pw) * ml
    if Ln:
        in_ = MathLog(in_)
    return in_

def ACTION(in1, in2):
    if in1 == EMPTY_VALUE or in2 == EMPTY_VALUE:
        return EMPTY_VALUE
    _sw1 = Action
    if _sw1 == 1:
        return in1 - in2
    elif _sw1 == 2:
        return in1 + in2
    elif _sw1 == 3:
        return in1 * in2
    elif _sw1 == 4:
        return _fdiv(in1, in2)
    return _fdiv(in1, in2)

def LOAD_DATA():
    global BeginDate, Error_Init
    txt = TimeToString(TimeLocal(), TIME_SECONDS)
    if not SymbolSelect(Symbol1, True):
        txt = txt + '\nUnavailable ' + Symbol1
        Comment(txt)
        return True
    if not SymbolSelect(Symbol2, True):
        txt = txt + '\nUnavailable ' + Symbol2
        Comment(txt)
        return True
    smb = _int(Window) * 2
    if Bars(Symbol1, PERIOD_CURRENT) <= smb:
        txt = txt + '\nNot enough data of the first symbol'
        Comment(txt)
        return True
    if Bars(Symbol2, PERIOD_CURRENT) <= smb:
        txt = txt + '\nNot enough data of the second symbol'
        Comment(txt)
        return True
    temp = Arr(1, 0, dyn=False)
    if CopyTime(Symbol1, PERIOD_CURRENT, Bars(Symbol1, PERIOD_CURRENT) - 1, 1, temp) <= 0:
        txt = txt + '\nGetting the date of the first symbol'
        Comment(txt)
        return True
    BeginDate = MathMax(BeginTime, temp[0])
    if CopyTime(Symbol2, PERIOD_CURRENT, Bars(Symbol2, PERIOD_CURRENT) - 1, 1, temp) <= 0:
        txt = txt + '\nGetting the date of the second symbol'
        Comment(txt)
        return True
    BeginDate = MathMax(BeginDate, temp[0])
    Comment('')
    Error_Init = False
    return False

def EMTF(i):
    BF[i] = EMPTY_VALUE
    CALC[i] = EMPTY_VALUE
    PR1[i] = EMPTY_VALUE
    PR2[i] = EMPTY_VALUE
    PRA1[i] = EMPTY_VALUE
    PRA2[i] = EMPTY_VALUE
    DTR[i] = EMPTY_VALUE
    LG1[i] = EMPTY_VALUE
    LG2[i] = EMPTY_VALUE
    LCLEAR(i)

def LCLEAR(i):
    L1up[i] = EMPTY_VALUE
    L2up[i] = EMPTY_VALUE
    L3up[i] = EMPTY_VALUE
    L1dn[i] = EMPTY_VALUE
    L2dn[i] = EMPTY_VALUE
    L3dn[i] = EMPTY_VALUE

def MA(pos):
    if (pos <= _int(Average) or PR1[pos] == EMPTY_VALUE) or PR1[pos] == EMPTY_VALUE:
        PRA1[pos] = EMPTY_VALUE
        PRA2[pos] = EMPTY_VALUE
        return
    x1 = 1
    temp = PR1[pos]
    for j in range(1, _int(Average)):
        if PR1[pos - j] != EMPTY_VALUE:
            temp += PR1[pos - j]
            x1 += 1
    temp = _fdiv(temp, float(x1))
    PRA1[pos] = temp
    x1 = 1
    temp = PR2[pos]
    for j in range(1, _int(Average)):
        if PR2[pos - j] != EMPTY_VALUE:
            temp += PR2[pos - j]
            x1 += 1
    temp = _fdiv(temp, float(x1))
    PRA2[pos] = temp

def DT(pos):
    if pos <= _int(Average + Window) or CALC[pos] == EMPTY_VALUE:
        DTR[pos] = EMPTY_VALUE
        return
    x1 = 1
    temp = CALC[pos]
    for j in range(1, _int(Window)):
        if CALC[pos - j] != EMPTY_VALUE:
            temp += CALC[pos - j]
            x1 += 1
    temp = _fdiv(temp, float(x1))
    DTR[pos] = CALC[pos] - temp

def LAG(pos):
    if (((pos <= _int(Average + Window) or PRA1[pos] == EMPTY_VALUE) or PRA2[pos] == EMPTY_VALUE) or PRA1[pos - Window] == EMPTY_VALUE) or PRA2[pos - Window] == EMPTY_VALUE:
        LG1[pos] = EMPTY_VALUE
        LG2[pos] = EMPTY_VALUE
        return
    if PRA1[pos - Window] != 0:
        LG1[pos] = _fdiv(PRA1[pos], PRA1[pos - Window])
    else:
        LG1[pos] = PRA1[pos]
    if PRA2[pos - Window] != 0:
        LG2[pos] = _fdiv(PRA2[pos], PRA2[pos - Window])
    else:
        LG2[pos] = PRA2[pos]

def NAME():
    name = ''
    if Invert1:
        name = '(inv)' + Symbol1
    else:
        name = Symbol1
    _sw2 = Action
    if _sw2 == 1:
        name = name + '-'
    elif _sw2 == 2:
        name = name + '+'
    elif _sw2 == 3:
        name = name + '*'
    elif _sw2 == 4:
        name = name + '/'
    if Invert2:
        name = name + '(inv)' + Symbol2
    else:
        name = name + Symbol2
    return name


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ispread(_MQL5Indicator):
    name = 'ispread'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Action': _Choice({1: 'Difference', 2: 'Sum', 3: 'Product', 4: 'Ratio'}, default=4),  # Action
        'Invert1': False,  # Reverse of symbol 1
        'Invert2': False,  # Reverse of symbol 2
        'Pow1': 1.0,  # Power of symbol 1
        'Pow2': 1.0,  # Power of symbol 2
        'Multi1': 1.0,  # Multiplier of symbol 1
        'Multi2': 1.0,  # Multiplier of symbol 2
        'Ln': False,  # The logarithm
        'Average': 3,  # Smoothing.Period
        'Algo': _Choice({1: 'The first difference', 2: 'Detrend using a simple MA'}, default=2),  # Selecting an algorithm
        'Window': 288,  # Period for the algorithm
        'Screen_Levels': True,  # Show levels
        'Method': _Choice({1: 'Normalization to 0..1 with an offset', 2: 'Levels of extrema'}, default=1),  # Levels calculation method
        'Levels': 1.0,  # Ratio of levels
    }

