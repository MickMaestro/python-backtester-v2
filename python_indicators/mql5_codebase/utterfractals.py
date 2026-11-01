"""utterfractals — converted from MQL5: MQL5 Indicators/UtterFractals/utterfractals.mq5

Utter Fractals
Copyright: Copyright © 2011, RMM; Link: rmm@nm.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, RMM', 'link': 'rmm@nm.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': ['Utter Fractals'], 'name': 'utterfractals', 'source': 'MQL5 Indicators/UtterFractals/utterfractals.mq5', 'folder': 'UtterFractals', 'inputs': [{'mql': 'QuantityOfBars_', 'py': 'QuantityOfBars_', 'param': 'QuantityOfBars_', 'type': 'uint', 'default': 1000, 'label': 'History observation depth in bars', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 217, 'label': 'Upper fractal symbol code', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 218, 'label': 'Lower fractal symbol code', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
QuantityOfBars_ = _input('QuantityOfBars_', 1000)  # History observation depth in bars
UpLable = _input('UpLable', 217)  # Upper fractal symbol code
DnLable = _input('DnLable', 218)  # Lower fractal symbol code
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Up_tmp = 0.0
Dn_tmp = 0.0
review = 20
StartBars = 0
QuantityOfBars = 0

def OnInit():
    global QuantityOfBars, StartBars
    StartBars = 6
    QuantityOfBars = QuantityOfBars_
    SetIndexBuffer(0, Up, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(Up, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, Dn, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(Dn, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'UtterFractals'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def ExistUp(index, High):
    if High[index + 1] < High[index] and High[index] >= High[index - 1]:
        return True
    return False

def ExistDn(index, Low):
    if Low[index + 1] >= Low[index] and Low[index] <= Low[index - 1]:
        return True
    return False

def IdentDualExtr(index, Open, Low, High, Close):
    j = 0
    type_ = 0
    up_back = False
    dn_back = False
    up_forward = False
    dn_forward = False
    upres = False
    dnres = False
    direction = ""
    j = index
    if Open[index] < Close[index]:
        direction = 'up'
    if Open[index] > Close[index]:
        direction = 'dn'
    upres = ExistUp(j, High)
    dnres = ExistDn(j, Low)
    while j < (index + review):
        j += 1
        if (upres and (not dnres)) and High[j] > Low[index]:
            if High[j] > High[index] and Open[index] > Close[index]:
                up_back = True
                dn_back = False
                direction = 'dn'
                break
            if High[j] < High[index] and Open[index] > Close[index]:
                up_back = False
                dn_back = False
                direction = 'dn'
                break
            if High[j] > High[index] and Open[index] < Close[index]:
                up_back = True
                dn_back = False
                direction = 'up'
                break
            if High[j] < High[index] and Open[index] < Close[index]:
                up_back = True
                dn_back = False
                direction = 'up'
                break
            if High[j] > High[index] and Open[index] == Close[index]:
                up_back = True
                dn_back = False
                direction = 'up'
                break
            if High[j] < High[index] and Open[index] == Close[index]:
                up_back = False
                dn_back = False
                direction = 'up'
                break
        if dnres and (not upres):
            if (Low[j] < Low[index] and Low[j] < High[index]) and Open[index] > Close[index]:
                up_back = False
                dn_back = True
                direction = 'dn'
                break
            if (Low[j] > Low[index] and Low[j] < High[index]) and Open[index] > Close[index]:
                up_back = False
                dn_back = True
                direction = 'dn'
                break
            if (Low[j] < Low[index] and Low[j] < High[index]) and Open[index] < Close[index]:
                up_back = False
                dn_back = True
                direction = 'up'
                break
            if (Low[j] > Low[index] and Low[j] < High[index]) and Open[index] < Close[index]:
                up_back = False
                dn_back = False
                direction = 'up'
                break
            if (Low[j] < High[index] and Low[j] < Low[index]) and Open[index] == Close[index]:
                up_back = False
                dn_back = True
                direction = 'up'
                break
            if (Low[j] < High[index] and Low[j] > Low[index]) and Open[index] == Close[index]:
                up_back = False
                dn_back = True
                direction = 'up'
                break
    j = index
    while j > (index - review):
        j -= 1
        if (upres and (not dnres)) and High[j] > Low[index]:
            if High[j] > High[index] and Open[index] > Close[index]:
                up_forward = True
                dn_forward = False
                direction = 'dn'
                break
            if High[j] < High[index] and Open[index] > Close[index]:
                up_forward = True
                dn_forward = False
                direction = 'dn'
                break
            if High[j] > High[index] and Open[index] < Close[index]:
                up_forward = True
                dn_forward = False
                direction = 'up'
                break
            if High[j] < High[index] and Open[index] < Close[index]:
                up_forward = False
                dn_forward = False
                direction = 'up'
                break
            if High[j] > High[index] and Open[index] == Close[index]:
                up_forward = True
                dn_forward = False
                direction = 'up'
                break
            if High[j] < High[index] and Open[index] == Close[index]:
                up_forward = True
                dn_forward = False
                direction = 'up'
                break
        if (dnres and (not upres)) and Low[j] < High[index]:
            if Low[j] < Low[index] and Open[index] > Close[index]:
                up_forward = False
                dn_forward = True
                direction = 'dn'
                break
            if Low[j] > Low[index] and Open[index] > Close[index]:
                up_forward = False
                dn_forward = False
                direction = 'dn'
                break
            if Low[j] < Low[index] and Open[index] < Close[index]:
                up_forward = False
                dn_forward = True
                direction = 'up'
                break
            if Low[j] > Low[index] and Open[index] < Close[index]:
                up_forward = False
                dn_forward = True
                direction = 'up'
                break
            if Low[j] < Low[index] and Open[index] == Close[index]:
                up_forward = False
                dn_forward = True
                direction = 'up'
                break
            if Low[j] > Low[index] and Open[index] == Close[index]:
                up_forward = False
                dn_forward = True
                direction = 'up'
                break
    if (up_back and up_forward) and direction == 'dn':
        type_ = 1
    if ((not up_back) and up_forward) and direction == 'dn':
        type_ = 2
    if ((not up_back) and up_forward) and direction == 'dn':
        type_ = 3
    if (up_back and up_forward) and direction == 'dn':
        type_ = 4
    if (up_back and up_forward) and direction == 'up':
        type_ = 5
    if (up_back and up_forward) and direction == 'up':
        type_ = 6
    if (up_back and up_forward) and direction == 'up':
        type_ = 7
    if (up_back and up_forward) and direction == 'up':
        type_ = 8
    if (dn_back and dn_forward) and direction == 'dn':
        type_ = 9
    if (dn_back and dn_forward) and direction == 'dn':
        type_ = 10
    if (dn_back and dn_forward) and direction == 'dn':
        type_ = 11
    if (dn_back and dn_forward) and direction == 'dn':
        type_ = 12
    if (dn_back and dn_forward) and direction == 'up':
        type_ = 13
    if ((not dn_back) and dn_forward) and direction == 'up':
        type_ = 14
    if (dn_back and dn_forward) and direction == 'up':
        type_ = 15
    if ((not dn_back) and dn_forward) and direction == 'up':
        type_ = 16
    if (dn_back and up_forward) and direction == 'dn':
        type_ = 17
    if (dn_back and up_forward) and direction == 'dn':
        type_ = 18
    if (dn_back and up_forward) and direction == 'dn':
        type_ = 19
    if (dn_back and up_forward) and direction == 'dn':
        type_ = 20
    if (dn_back and up_forward) and direction == 'up':
        type_ = 21
    if ((not dn_back) and up_forward) and direction == 'up':
        type_ = 22
    if (dn_back and (not up_forward)) and direction == 'up':
        type_ = 23
    if ((not dn_back) and (not up_forward)) and direction == 'up':
        type_ = 24
    if (up_back and dn_forward) and direction == 'dn':
        type_ = 25
    if (up_back and (not dn_forward)) and direction == 'dn':
        type_ = 26
    if ((not up_back) and dn_forward) and direction == 'dn':
        type_ = 27
    if ((not up_back) and (not dn_forward)) and direction == 'dn':
        type_ = 28
    if (up_back and dn_forward) and direction == 'up':
        type_ = 29
    if (up_back and dn_forward) and direction == 'up':
        type_ = 30
    if (up_back and dn_forward) and direction == 'up':
        type_ = 31
    if (up_back and dn_forward) and direction == 'up':
        type_ = 32
    return type_

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Dn_tmp, QuantityOfBars, Up_tmp
    if rates_total < StartBars:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    actual_back = False
    actual_forward = False
    i = 0
    j = 0
    TypeDuo = 0
    Up[0] = 0.0
    Up[1] = 0.0
    Dn[0] = 0.0
    Dn[1] = 0.0
    if _int(QuantityOfBars) > (rates_total - 21):
        QuantityOfBars = rates_total - 21
    i = _int(QuantityOfBars)
    for i in range(i, 1, -1):
        Up[i] = 0.0
        Dn[i] = 0.0
        if ExistUp(i, high) and (not ExistDn(i, high)):
            actual_back = False
            j = i
            while j < (i + review):
                j += 1
                if (ExistUp(j, high) and (not ExistDn(j, high))) and high[j] >= high[i]:
                    actual_back = False
                    break
                if (ExistDn(j, high) and (not ExistUp(j, high))) and low[j] < high[i]:
                    actual_back = True
                    break
                if ExistDn(j, high) and ExistUp(j, high):
                    TypeDuo = IdentDualExtr(j, open, low, high, close)
                    _sw1 = TypeDuo
                    if _sw1 == 1:
                        actual_back = True
                    elif _sw1 == 2:
                        actual_back = True
                    elif _sw1 == 3:
                        actual_back = True
                    elif _sw1 == 4:
                        actual_back = True
                    elif _sw1 == 5:
                        actual_back = True
                    elif _sw1 == 6:
                        actual_back = True
                    elif _sw1 == 7:
                        actual_back = True
                    elif _sw1 == 8:
                        actual_back = True
                    elif _sw1 == 9:
                        actual_back = True
                    elif _sw1 == 10:
                        actual_back = True
                    elif _sw1 == 11:
                        actual_back = True
                    elif _sw1 == 12:
                        actual_back = True
                    elif _sw1 == 13:
                        actual_back = True
                    elif _sw1 == 14:
                        actual_back = True
                    elif _sw1 == 15:
                        actual_back = True
                    elif _sw1 == 16:
                        actual_back = True
                    elif _sw1 == 17:
                        actual_back = True
                    elif _sw1 == 18:
                        actual_back = True
                    elif _sw1 == 19:
                        actual_back = True
                    elif _sw1 == 20:
                        actual_back = True
                    elif _sw1 == 21:
                        actual_back = True
                    elif _sw1 == 22:
                        actual_back = True
                    elif _sw1 == 23:
                        actual_back = False
                    elif _sw1 == 24:
                        actual_back = False
                    elif _sw1 == 25:
                        actual_back = True
                    elif _sw1 == 26:
                        actual_back = True
                    elif _sw1 == 27:
                        actual_back = True
                    elif _sw1 == 28:
                        actual_back = True
                    elif _sw1 == 29:
                        actual_back = True
                    elif _sw1 == 30:
                        actual_back = True
                    elif _sw1 == 31:
                        actual_back = True
                    elif _sw1 == 32:
                        actual_back = True
                    break
            actual_forward = False
            j = i
            while j > (i - review):
                if j < 2:
                    break
                j -= 1
                if (ExistUp(j, high) and (not ExistDn(j, high))) and high[j] > high[i]:
                    actual_forward = False
                    break
                if (ExistDn(j, high) and (not ExistUp(j, high))) and low[j] < high[i]:
                    actual_forward = True
                    break
                if ExistDn(j, high) and ExistUp(j, high):
                    TypeDuo = IdentDualExtr(j, open, low, high, close)
                    _sw2 = TypeDuo
                    if _sw2 == 1:
                        actual_forward = True
                    elif _sw2 == 2:
                        actual_forward = False
                    elif _sw2 == 3:
                        actual_forward = False
                    elif _sw2 == 4:
                        actual_forward = True
                    elif _sw2 == 5:
                        actual_forward = True
                    elif _sw2 == 6:
                        actual_forward = True
                    elif _sw2 == 7:
                        actual_forward = True
                    elif _sw2 == 8:
                        actual_forward = True
                    elif _sw2 == 9:
                        actual_forward = True
                    elif _sw2 == 10:
                        actual_forward = True
                    elif _sw2 == 11:
                        actual_forward = True
                    elif _sw2 == 12:
                        actual_forward = True
                    elif _sw2 == 13:
                        actual_forward = True
                    elif _sw2 == 14:
                        actual_forward = True
                    elif _sw2 == 15:
                        actual_forward = True
                    elif _sw2 == 16:
                        actual_forward = True
                    elif _sw2 == 17:
                        actual_forward = True
                    elif _sw2 == 18:
                        actual_forward = True
                    elif _sw2 == 19:
                        actual_forward = True
                    elif _sw2 == 20:
                        actual_forward = True
                    elif _sw2 == 21:
                        actual_forward = True
                    elif _sw2 == 22:
                        actual_forward = True
                    elif _sw2 == 23:
                        actual_forward = True
                    elif _sw2 == 24:
                        actual_forward = True
                    elif _sw2 == 25:
                        actual_forward = True
                    elif _sw2 == 26:
                        actual_forward = True
                    elif _sw2 == 27:
                        actual_forward = False
                    elif _sw2 == 28:
                        actual_forward = False
                    elif _sw2 == 29:
                        actual_forward = True
                    elif _sw2 == 30:
                        actual_forward = True
                    elif _sw2 == 31:
                        actual_forward = True
                    elif _sw2 == 32:
                        actual_forward = True
                    break
            if actual_back and actual_forward:
                Up_tmp = high[i]
            else:
                Up_tmp = 0.0
        else:
            Up_tmp = 0.0
        if ExistDn(i, high) and (not ExistUp(i, high)):
            actual_back = False
            j = i
            while j < (i + review):
                j += 1
                if (ExistDn(j, high) and (not ExistUp(j, high))) and low[j] <= low[i]:
                    actual_back = False
                    break
                if (ExistUp(j, high) and (not ExistDn(j, high))) and high[j] > low[i]:
                    actual_back = True
                    break
                if ExistDn(j, high) and ExistUp(j, high):
                    TypeDuo = IdentDualExtr(j, open, low, high, close)
                    _sw3 = TypeDuo
                    if _sw3 == 1:
                        actual_back = True
                    elif _sw3 == 2:
                        actual_back = True
                    elif _sw3 == 3:
                        actual_back = True
                    elif _sw3 == 4:
                        actual_back = True
                    elif _sw3 == 5:
                        actual_back = True
                    elif _sw3 == 6:
                        actual_back = True
                    elif _sw3 == 7:
                        actual_back = True
                    elif _sw3 == 8:
                        actual_back = True
                    elif _sw3 == 9:
                        actual_back = True
                    elif _sw3 == 10:
                        actual_back = True
                    elif _sw3 == 11:
                        actual_back = True
                    elif _sw3 == 12:
                        actual_back = True
                    elif _sw3 == 13:
                        actual_back = True
                    elif _sw3 == 14:
                        actual_back = True
                    elif _sw3 == 15:
                        actual_back = True
                    elif _sw3 == 16:
                        actual_back = True
                    elif _sw3 == 17:
                        actual_back = True
                    elif _sw3 == 18:
                        actual_back = True
                    elif _sw3 == 19:
                        actual_back = True
                    elif _sw3 == 20:
                        actual_back = True
                    elif _sw3 == 21:
                        actual_back = True
                    elif _sw3 == 22:
                        actual_back = True
                    elif _sw3 == 23:
                        actual_back = True
                    elif _sw3 == 24:
                        actual_back = True
                    elif _sw3 == 25:
                        actual_back = True
                    elif _sw3 == 26:
                        actual_back = False
                    elif _sw3 == 27:
                        actual_back = True
                    elif _sw3 == 28:
                        actual_back = False
                    elif _sw3 == 29:
                        actual_back = True
                    elif _sw3 == 30:
                        actual_back = True
                    elif _sw3 == 31:
                        actual_back = True
                    elif _sw3 == 32:
                        actual_back = True
                    break
            actual_forward = False
            j = i
            while j > (i - review):
                if j < 2:
                    break
                j -= 1
                if (ExistDn(j, high) and (not ExistUp(j, high))) and low[j] < low[i]:
                    actual_forward = False
                    break
                if (ExistUp(j, high) and (not ExistDn(j, high))) and high[j] > low[i]:
                    actual_forward = True
                    break
                if ExistDn(j, high) and ExistUp(j, high):
                    TypeDuo = IdentDualExtr(j, open, low, high, close)
                    _sw4 = TypeDuo
                    if _sw4 == 1:
                        actual_forward = True
                    elif _sw4 == 2:
                        actual_forward = True
                    elif _sw4 == 3:
                        actual_forward = True
                    elif _sw4 == 4:
                        actual_forward = True
                    elif _sw4 == 5:
                        actual_forward = True
                    elif _sw4 == 6:
                        actual_forward = True
                    elif _sw4 == 7:
                        actual_forward = True
                    elif _sw4 == 8:
                        actual_forward = True
                    elif _sw4 == 9:
                        actual_forward = True
                    elif _sw4 == 10:
                        actual_forward = True
                    elif _sw4 == 11:
                        actual_forward = True
                    elif _sw4 == 12:
                        actual_forward = True
                    elif _sw4 == 13:
                        actual_forward = True
                    elif _sw4 == 14:
                        actual_forward = False
                    elif _sw4 == 15:
                        actual_forward = True
                    elif _sw4 == 16:
                        actual_forward = False
                    elif _sw4 == 17:
                        actual_forward = True
                    elif _sw4 == 18:
                        actual_forward = True
                    elif _sw4 == 19:
                        actual_forward = True
                    elif _sw4 == 20:
                        actual_forward = True
                    elif _sw4 == 21:
                        actual_forward = True
                    elif _sw4 == 22:
                        actual_forward = False
                    elif _sw4 == 23:
                        actual_forward = True
                    elif _sw4 == 24:
                        actual_forward = False
                    elif _sw4 == 25:
                        actual_forward = True
                    elif _sw4 == 26:
                        actual_forward = True
                    elif _sw4 == 27:
                        actual_forward = True
                    elif _sw4 == 28:
                        actual_forward = True
                    elif _sw4 == 29:
                        actual_forward = True
                    elif _sw4 == 30:
                        actual_forward = True
                    elif _sw4 == 31:
                        actual_forward = True
                    elif _sw4 == 32:
                        actual_forward = True
                    break
            if actual_back and actual_forward:
                Dn_tmp = low[i]
            else:
                Dn_tmp = 0.0
        else:
            Dn_tmp = 0.0
        if ExistDn(i, high) and ExistUp(i, high):
            TypeDuo = IdentDualExtr(i, open, low, high, close)
            _sw5 = TypeDuo
            if _sw5 == 1:
                Up_tmp = 0.0
                Dn_tmp = low[i]
            elif _sw5 == 2:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 3:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 4:
                Up_tmp = 0.0
                Dn_tmp = low[i]
            elif _sw5 == 5:
                Up_tmp = 0.0
                Dn_tmp = low[i]
            elif _sw5 == 6:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 7:
                Up_tmp = 0.0
                Dn_tmp = low[i]
            elif _sw5 == 8:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 9:
                Up_tmp = high[i]
                Dn_tmp = 0.0
            elif _sw5 == 10:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 11:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 12:
                Up_tmp = low[i]
                Dn_tmp = 0.0
            elif _sw5 == 13:
                Up_tmp = high[i]
                Dn_tmp = 0.0
            elif _sw5 == 14:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 15:
                Up_tmp = high[i]
                Dn_tmp = 0.0
            elif _sw5 == 16:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 17:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 18:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 19:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 20:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 21:
                Up_tmp = 0.0
                Dn_tmp = 0.0
            elif _sw5 == 22:
                Up_tmp = 0.0
                Dn_tmp = low[i]
            elif _sw5 == 23:
                Up_tmp = high[i]
                Dn_tmp = 0.0
            elif _sw5 == 24:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 25:
                Up_tmp = 0.0
                Dn_tmp = 0.0
            elif _sw5 == 26:
                Up_tmp = 0.0
                Dn_tmp = low[i]
            elif _sw5 == 27:
                Up_tmp = high[i]
                Dn_tmp = 0.0
            elif _sw5 == 28:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 29:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 30:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 31:
                Up_tmp = high[i]
                Dn_tmp = low[i]
            elif _sw5 == 32:
                Up_tmp = high[i]
                Dn_tmp = low[i]
        if (not ExistDn(i, high)) and (not ExistUp(i, high)):
            Up_tmp = 0.0
            Dn_tmp = 0.0
        Up[i] = Up_tmp + (2 * Point())
        Dn[i] = Dn_tmp - (2 * Point())
    else:
        i = _range_end(i, 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Utterfractals(_MQL5Indicator):
    name = 'utterfractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'QuantityOfBars_': 1000,  # History observation depth in bars
        'UpLable': 217,  # Upper fractal symbol code
        'DnLable': 218,  # Lower fractal symbol code
    }

