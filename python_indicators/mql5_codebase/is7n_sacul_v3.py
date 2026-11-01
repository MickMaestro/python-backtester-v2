"""is7n_sacul_v3 — converted from MQL5: MQL5 Indicators/iS7N_SacuL.mq5/is7n_sacul_v3.mq5

Arrows & curves type indicator
The 'iS7N_SacuL.mq5' indicator is based on the
original indicator 'Lucas1.mq4', written in MT4
Copyright © 2007, lukas1
http://www.alpari-idc.ru/
Copyright: Copyright 2010, SHOOTER777; Link: s7n@mail.ru; Version: 3.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, SHOOTER777', 'link': 's7n@mail.ru', 'version': '3.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 1, 4: 1}, 'colors': {1: [255], 2: [32768], 3: [8421504], 4: [8421504]}, 'widths': {1: 3, 2: 3, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'iSacuL_UP_Arrow', 2: 'iSacuL_DN_Arrow', 3: 'iSacuL_UP_Line', 4: 'iSacuL_DN_Line', 5: 'iSacuL_Trend'}, 'levels': [], 'description': ['Arrows & curves type indicator', "The 'iS7N_SacuL.mq5' indicator is based on the", "original indicator 'Lucas1.mq4', written in MT4", 'Copyright © 2007, lukas1', 'http://www.alpari-idc.ru/'], 'name': 'is7n_sacul_v3', 'source': 'MQL5 Indicators/iS7N_SacuL.mq5/is7n_sacul_v3.mq5', 'folder': 'iS7N_SacuL.mq5', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Pro', 'py': 'Pro', 'param': 'Pro', 'type': 'int', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'bExp', 'py': 'bExp', 'param': 'bExp', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name

# ---- inputs and global variables
Per = _input('Per', 7)
Pro = _input('Pro', 25)
bExp = _input('bExp', False)
iMx = 500  # number of bars to calculate
dBuf_1 = Arr(0, 0.0)  # "up" arrows buffer
dBuf_2 = Arr(0, 0.0)  # "down" arrows buffer
dBuf_3 = Arr(0, 0.0)  # upper channel buffer
dBuf_4 = Arr(0, 0.0)  # lower channel buffer
dBuf_5 = Arr(0, 0.0)  # trend direction buffer
dBuf_Hi = Arr(0, 0.0)  # buffer for Hi
dBuf_Lo = Arr(0, 0.0)  # buffer for Lo
ihHiA = 0
ihLoA = 0
ihHiL = 0
ihLoL = 0
bUp = False
bOld = False
sSmbl = ""
sShNm = ""

def OnInit():
    global sSmbl
    sSmbl = Symbol()
    SetIndexBuffer(0, dBuf_1)
    SetIndexBuffer(1, dBuf_2)
    SetIndexBuffer(2, dBuf_3)
    SetIndexBuffer(3, dBuf_4)
    SetIndexBuffer(4, dBuf_5)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, sShNm)
    PlotIndexSetString(0, PLOT_LABEL, 'UP_Arrow')
    PlotIndexSetString(1, PLOT_LABEL, 'DN_Arrow')
    PlotIndexSetString(2, PLOT_LABEL, 'UP_Line')
    PlotIndexSetString(3, PLOT_LABEL, 'DN_Line')
    PlotIndexSetString(4, PLOT_LABEL, 'Trend_Arrow')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(5, PLOT_SHOW_DATA, False)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global bOld, bUp, iMx, ihHiA, ihLoA
    if prev_calculated > 0:
        if rates_total <= prev_calculated:
            return rates_total
    dHiA = 0.0
    dLoA = 0.0
    dMax = 0.0
    dMin = 0.0
    if Pro <= 0:
        PlotIndexSetInteger(2, PLOT_LINE_COLOR, Blue)
        PlotIndexSetInteger(3, PLOT_LINE_COLOR, Blue)
    else:
        PlotIndexSetInteger(2, PLOT_LINE_COLOR, Gray)
        PlotIndexSetInteger(3, PLOT_LINE_COLOR, Gray)
    if prev_calculated <= 0:
        for i in range(0, rates_total - 1 + 1):
            dBuf_1[i] = EMPTY_VALUE
            dBuf_2[i] = EMPTY_VALUE
            dBuf_3[i] = EMPTY_VALUE
            dBuf_4[i] = EMPTY_VALUE
            dBuf_5[i] = EMPTY_VALUE
        Print('!!!All buffer arrays has been filled with empty values!!!')
    iMn = 10 * Per
    if iMn > rates_total:
        return 0
    if iMn > iMx:
        iMx = iMn
    if iMx > rates_total:
        iMx = rates_total
    limit = 0
    preMx = 1
    if bExp:
        preMx = iMn
    if prev_calculated <= 0:
        limit = rates_total - iMx
    else:
        limit = prev_calculated - preMx
    for i in range(limit, 0, -1):
        if dBuf_2[i] > 0:
            bOld = False
            break
        if dBuf_1[i] > 0:
            bOld = True
            break
    for iii in range(limit, rates_total + 1):
        ihHiA = CopyHigh(sSmbl, Period(), rates_total - iii - 1, Per, dBuf_Hi)
        if ihHiA <= 0:
            break
        else:
            dHiA = dBuf_Hi[ArrayMaximum(dBuf_Hi, 0, WHOLE_ARRAY)]
        ihLoA = CopyLow(sSmbl, Period(), rates_total - iii - 1, Per, dBuf_Lo)
        if ihLoA <= 0:
            break
        else:
            dLoA = dBuf_Lo[ArrayMinimum(dBuf_Lo, 0, WHOLE_ARRAY)]
        dMax = dHiA - (((dHiA - dLoA) * Pro) / 100)
        dMin = dLoA + (((dHiA - dLoA) * Pro) / 100)
        if price[iii] < dMin:
            bUp = False
        if price[iii] > dMax:
            bUp = True
        dBuf_5[iii] = bUp
        if (bUp != bOld and bUp == False) and iii != (rates_total - 1):
            dBuf_2[iii] = dHiA
        if (bUp != bOld and bUp == True) and iii != (rates_total - 1):
            dBuf_1[iii] = dLoA
        bOld = bUp
        dBuf_3[iii] = dMax
        dBuf_4[iii] = dMin
        dBuf_1[limit + 1] = EMPTY_VALUE
        dBuf_2[limit + 1] = EMPTY_VALUE
        dBuf_1[limit] = EMPTY_VALUE
        dBuf_2[limit] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Is7nSaculV3(_MQL5Indicator):
    name = 'is7n_sacul_v3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Per': 7,
        'Pro': 25,
        'bExp': False,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

