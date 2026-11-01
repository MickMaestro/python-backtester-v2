"""FiboZigZag — converted from MQL5: MQL5 Indicators/ZigZag auto Fibo/FiboZigZag.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'FiboZigZag', 'source': 'MQL5 Indicators/ZigZag auto Fibo/FiboZigZag.mq5', 'folder': 'ZigZag auto Fibo', 'inputs': [{'mql': 'inpName', 'py': 'inpName', 'param': None, 'type': 'string', 'default': 'Fibo_01', 'label': 'Fibo Name', 'sinput': False}, {'mql': 'inpDepth', 'py': 'inpDepth', 'param': 'inpDepth', 'type': 'int', 'default': 34, 'label': 'ZigZag Depth', 'sinput': False}, {'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'int', 'default': 15, 'label': 'ZigZag Deviation', 'sinput': False}, {'mql': 'inpBackStep', 'py': 'inpBackStep', 'param': 'inpBackStep', 'type': 'int', 'default': 8, 'label': 'ZigZag BackStep', 'sinput': False}, {'mql': 'inpLeg', 'py': 'inpLeg', 'param': 'inpLeg', 'type': 'int', 'default': 1, 'label': 'ZigZag Leg', 'sinput': False}, {'mql': 'inpLineColor', 'py': 'inpLineColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Line Color', 'sinput': False}, {'mql': 'inpLevelsColor', 'py': 'inpLevelsColor', 'param': None, 'type': 'color', 'default': 11829830, 'label': 'Levels Color', 'sinput': False}, {'mql': 'inpRay', 'py': 'inpRay', 'param': 'inpRay', 'type': 'bool', 'default': False, 'label': 'Ray', 'sinput': False}, {'mql': 'inpLevel1', 'py': 'inpLevel1', 'param': 'inpLevel1', 'type': 'double', 'default': 0.0, 'label': 'Level 1', 'sinput': False}, {'mql': 'inpLevel2', 'py': 'inpLevel2', 'param': 'inpLevel2', 'type': 'double', 'default': 23.6, 'label': 'Level 2', 'sinput': False}, {'mql': 'inpLevel3', 'py': 'inpLevel3', 'param': 'inpLevel3', 'type': 'double', 'default': 38.2, 'label': 'Level 3', 'sinput': False}, {'mql': 'inpLevel4', 'py': 'inpLevel4', 'param': 'inpLevel4', 'type': 'double', 'default': 50.0, 'label': 'Level 4', 'sinput': False}, {'mql': 'inpLevel5', 'py': 'inpLevel5', 'param': 'inpLevel5', 'type': 'double', 'default': 61.8, 'label': 'Level 5', 'sinput': False}, {'mql': 'inpLevel6', 'py': 'inpLevel6', 'param': 'inpLevel6', 'type': 'double', 'default': 100.0, 'label': 'Level 6', 'sinput': False}, {'mql': 'inpLevel7', 'py': 'inpLevel7', 'param': 'inpLevel7', 'type': 'double', 'default': 161.8, 'label': 'Level 7', 'sinput': False}, {'mql': 'inpLevel8', 'py': 'inpLevel8', 'param': 'inpLevel8', 'type': 'double', 'default': 261.8, 'label': 'Level 8', 'sinput': False}, {'mql': 'inpLevel9', 'py': 'inpLevel9', 'param': 'inpLevel9', 'type': 'double', 'default': 423.6, 'label': 'Level 9', 'sinput': False}, {'mql': 'inpMaxBars', 'py': 'inpMaxBars', 'param': 'inpMaxBars', 'type': 'int', 'default': 1000, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpName = _input('inpName', 'Fibo_01')  # Fibo Name
inpDepth = _input('inpDepth', 34)  # ZigZag Depth
inpDeviation = _input('inpDeviation', 15)  # ZigZag Deviation
inpBackStep = _input('inpBackStep', 8)  # ZigZag BackStep
inpLeg = _input('inpLeg', 1)  # ZigZag Leg
inpLineColor = _input('inpLineColor', clrRed)  # Line Color
inpLevelsColor = _input('inpLevelsColor', clrSteelBlue)  # Levels Color
inpRay = _input('inpRay', False)  # Ray
inpLevel1 = _input('inpLevel1', 0.0)  # Level 1
inpLevel2 = _input('inpLevel2', 23.6)  # Level 2
inpLevel3 = _input('inpLevel3', 38.2)  # Level 3
inpLevel4 = _input('inpLevel4', 50.0)  # Level 4
inpLevel5 = _input('inpLevel5', 61.8)  # Level 5
inpLevel6 = _input('inpLevel6', 100.0)  # Level 6
inpLevel7 = _input('inpLevel7', 161.8)  # Level 7
inpLevel8 = _input('inpLevel8', 261.8)  # Level 8
inpLevel9 = _input('inpLevel9', 423.6)  # Level 9
inpMaxBars = _input('inpMaxBars', 1000)
levels = Arr(9, 0.0, dyn=False)  # Levels Array
handle = 0

def OnInit():
    global handle
    levels[0] = inpLevel1
    levels[1] = inpLevel2
    levels[2] = inpLevel3
    levels[3] = inpLevel4
    levels[4] = inpLevel5
    levels[5] = inpLevel6
    levels[6] = inpLevel7
    levels[7] = inpLevel8
    levels[8] = inpLevel9
    handle = iCustom(Symbol(), PERIOD_CURRENT, 'examples\\ZigZag', inpDepth, inpDeviation, inpBackStep)
    if handle == INVALID_HANDLE:
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, inpName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    times = Arr(2, 0, dyn=False)
    price = Arr(2, 0.0, dyn=False)
    if not GetZZ(times, price):
        return 0
    if ObjectFind(0, inpName) < 0:
        FiboDraw(inpName, times, price, inpLineColor, inpLevelsColor)
    else:
        FiboMove(inpName, times, price, inpLevelsColor)
    ChartRedraw()
    return rates_total
    return rates_total

def FiboMove(name, time, price, clrLevels):
    ObjectMove(0, name, 0, time[1], price[1])
    ObjectMove(0, name, 1, time[0], price[0])
    FiboSetLevels(name, price, clrLevels)
    ChartRedraw()

def FiboDraw(name, time, price, clrFibo=clrRed, clrLevels=clrYellow):
    chart_ID = 0
    sub_window = 0
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_FIBO, sub_window, time[1], price[1], time[0], price[0]):
        Print('FiboDraw', ': failed to create "Fibonacci Retracement"! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clrFibo)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, 1)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, inpRay)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)
    FiboSetLevels(name, price, clrLevels)
    return True

def FiboSetLevels(name, price, clrLevels=clrYellow):
    chart_ID = 0
    sub_window = 0
    N = ArraySize(levels)
    str_ = ''
    ResetLastError()
    ObjectSetInteger(chart_ID, name, OBJPROP_LEVELS, N)
    for i in range(0, N):
        ObjectSetDouble(chart_ID, name, OBJPROP_LEVELVALUE, i, levels[i] / 100.0)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, i, clrLevels)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELSTYLE, i, STYLE_DOT)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELWIDTH, i, 1)
    for i in range(0, N):
        str_ = DoubleToString(levels[i], 1) + '% = '
        str_ += DoubleToString(price[0] + ((levels[i] / 100.0) * (price[1] - price[0])), Digits()) + '  '
        ObjectSetString(chart_ID, name, OBJPROP_LEVELTEXT, i, str_)
    return True

def GetZZ(time, price):
    ret = False
    leg = MathMax(1, inpLeg)
    cnt = 0
    idx = 0
    zz = Arr(0, 0.0)
    ArraySetAsSeries(zz, True)
    if CopyBuffer(handle, 0, 0, inpMaxBars, zz) != inpMaxBars:
        return ret
    for i in range(1, inpMaxBars - 1):
        if zz[i] <= 0.0 or zz[i] == EMPTY_VALUE:
            continue
        cnt += 1
        if cnt < leg:
            continue
        Time = Arr(0, 0)
        if CopyTime(Symbol(), PERIOD_CURRENT, i, 1, Time) != 1:
            return False
        time[idx] = Time[0]
        price[idx] = zz[i]
        idx += 1
        if idx > 1:
            if CopyTime(Symbol(), PERIOD_CURRENT, 0, 1, Time) != 1:
                return False
            time[0] = Time[0]
            ret = True
            break
    return ret


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboZigZag(_MQL5Indicator):
    name = 'FiboZigZag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDepth': 34,  # ZigZag Depth
        'inpDeviation': 15,  # ZigZag Deviation
        'inpBackStep': 8,  # ZigZag BackStep
        'inpLeg': 1,  # ZigZag Leg
        'inpRay': False,  # Ray
        'inpLevel1': 0.0,  # Level 1
        'inpLevel2': 23.6,  # Level 2
        'inpLevel3': 38.2,  # Level 3
        'inpLevel4': 50.0,  # Level 4
        'inpLevel5': 61.8,  # Level 5
        'inpLevel6': 100.0,  # Level 6
        'inpLevel7': 161.8,  # Level 7
        'inpLevel8': 261.8,  # Level 8
        'inpLevel9': 423.6,  # Level 9
        'inpMaxBars': 1000,
    }

