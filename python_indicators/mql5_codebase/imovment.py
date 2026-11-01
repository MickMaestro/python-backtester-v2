"""imovment — converted from MQL5: MQL5 Indicators/iMovment/imovment.mq5

Copyright: dmffx.com; Link: http://dmffx.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'dmffx.com', 'link': 'http://dmffx.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [4294967295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'imovment', 'source': 'MQL5 Indicators/iMovment/imovment.mq5', 'folder': 'iMovment', 'inputs': [{'mql': 'Movment', 'py': 'Movment', 'param': 'Movment', 'type': 'int', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpBackColor', 'py': 'UpBackColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DnBackColor', 'py': 'DnBackColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Auto5Digits', 'py': 'Auto5Digits', 'param': 'Auto5Digits', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
Movment = _input('Movment', 70)
Auto5Digits = _input('Auto5Digits', True)
BOpen = Arr(0, 0.0)
BHigh = Arr(0, 0.0)
BLow = Arr(0, 0.0)
BClose = Arr(0, 0.0)
BColor = Arr(0, 0.0)
BTrend = Arr(0, 0.0)
BMin = Arr(0, 0.0)
BMax = Arr(0, 0.0)
Grad = 10
Colors = Arr(0, 0)
Movment2 = 0.0

def OnInit():
    global Movment2
    Movment2 = Movment
    if Auto5Digits:
        if Digits() == 5 or Digits() == 3:
            Movment2 *= 10
    SetIndexBuffer(0, BOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BLow, INDICATOR_DATA)
    SetIndexBuffer(3, BClose, INDICATOR_DATA)
    SetIndexBuffer(4, BColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BTrend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BMin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BMax, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    ArrayResize(Colors, Grad * 2)
    Col1 = _uint(PlotIndexGetInteger(0, PLOT_LINE_COLOR, 0))
    Col2 = _uint(PlotIndexGetInteger(0, PLOT_LINE_COLOR, 1))
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, Grad * 2)
    i = 0
    while i < Grad:
        Colors[i] = GetColor(_fdiv(1.0 * i, Grad - 1), DnColor, DnBackColor)
        Colors[i + Grad] = GetColor(_fdiv(1.0 * i, Grad - 1), UpColor, UpBackColor)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, Colors[i])
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i + Grad, Colors[i + Grad])
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    if prev_calculated > 0:
        limit = prev_calculated - 1
    else:
        limit = 1
    for i in range(limit, rates_total):
        BOpen[i] = open[i]
        BHigh[i] = high[i]
        BLow[i] = low[i]
        BClose[i] = close[i]
        BTrend[i] = BTrend[i - 1]
        BMax[i] = BMax[i - 1]
        BMin[i] = BMin[i - 1]
        ColInd = 0
        _sw1 = _int(BTrend[i])
        if _sw1 == 1:
            if close[i] > BMax[i]:
                BMax[i] = close[i]
            ColInd = _int(MathCeil(_fdiv(10.0 * (BMax[i] - close[i]), Point() * Movment2)))
            if ColInd >= Grad:
                BTrend[i] = -1.0
                BMin[i] = close[i]
                ColInd = 0
            else:
                ColInd += Grad
        elif _sw1 == 0:
            BOpen[i] = 0.0
            BHigh[i] = 0.0
            BLow[i] = 0.0
            BClose[i] = 0.0
            if close[i] > BMax[i]:
                BMax[i] = close[i]
            if close[i] < BMin[i]:
                BMin[i] = close[i]
            if close[i] <= (BMax[i] - (Point() * Movment2)):
                BTrend[i] = -1.0
                BMin[i] = close[i]
            if close[i] >= (BMin[i] + (Point() * Movment2)):
                BTrend[i] = 1.0
                BMax[i] = close[i]
        elif _sw1 == -1:
            if close[i] < BMin[i]:
                BMin[i] = close[i]
            ColInd = _int(MathCeil(_fdiv(10.0 * (close[i] - BMin[i]), Point() * Movment2)))
            if ColInd >= Grad:
                BTrend[i] = 1.0
                BMax[i] = close[i]
                ColInd = Grad
        BColor[i] = ColInd
    return rates_total

def GetColor(aK, Col1, Col2):
    R1 = Box(0)
    G1 = Box(0)
    B1 = Box(0)
    R2 = Box(0)
    G2 = Box(0)
    B2 = Box(0)
    fGetRGB(R1, G1, B1, Col1)
    fGetRGB(R2, G2, B2, _int(Col2))
    return fRGB(_int(R1.v + (aK * (R2.v - R1.v))), _int(G1.v + (aK * (G2.v - G1.v))), _int(B1.v + (aK * (B2.v - B1.v))))

def fGetRGB(aR, aG, aB, aCol):
    aB.v = _idiv(aCol, 65536)
    aCol -= aB.v * 65536
    aG.v = _idiv(aCol, 256)
    aCol -= aG.v * 256
    aR.v = aCol

def fRGB(aR, aG, aB):
    return _uint(aR + (256 * aG) + (65536 * aB))

# ---- global variables initialised from expressions
UpColor = _input('UpColor', _uint(Blue))
UpBackColor = _input('UpBackColor', _uint(White))
DnColor = _input('DnColor', _uint(Red))
DnBackColor = _input('DnBackColor', _uint(White))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Imovment(_MQL5Indicator):
    name = 'imovment'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Movment': 70,
        'Auto5Digits': True,
    }

