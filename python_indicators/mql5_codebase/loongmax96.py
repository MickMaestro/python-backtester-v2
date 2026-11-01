"""loongmax96 — converted from MQL5: MQL5 Indicators/LoongMAx96/loongmax96.mq5

Copyright: 2010, Loong@forum.mql4.com; Link: Loong@forum.mql4.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.cmybuffer import *  # #include cmybuffer.mqh

MQL5_META = {'props': {'copyright': '2010, Loong@forum.mql4.com', 'link': 'Loong@forum.mql4.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'loongmax96', 'source': 'MQL5 Indicators/LoongMAx96/loongmax96.mq5', 'folder': 'LoongMAx96', 'inputs': [{'mql': 'smootMode', 'py': 'smootMode', 'param': 'smootMode', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cmybuffer.mqh']}

Aqua = 0xFFFF00  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Orange = 0x00A5FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
smootMode = _input('smootMode', MODE_EMA)
price = _input('price', PRICE_CLOSE)
shift = _input('shift', 0)
iParam = Arr(96, 0, dyn=False)

def ColorInc16(i):
    iColor = 0
    MA_Rinc = 0
    MA_Ginc = 0
    MA_Binc = 0
    if i <= 0:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 4:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 96
        MA_Binc = 0
    elif i < 8:
        iColor = 0x00FFFF
        MA_Rinc = -96
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 12:
        iColor = 0x00FF00
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 96
    elif i < 16:
        iColor = 0xFFFF00
        MA_Rinc = 0
        MA_Ginc = -96
        MA_Binc = 0
    elif i < 20:
        iColor = 0xFF0000
        MA_Rinc = 96
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 24:
        iColor = 0xFF00FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = -96
    elif i < 28:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 96
        MA_Binc = 0
    elif i < 32:
        iColor = 0x00FFFF
        MA_Rinc = -96
        MA_Ginc = 0
        MA_Binc = 0
    else:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 0
    iColorInc = MA_Rinc + (256 * MA_Ginc) + (65536 * MA_Binc)
    return iColor + (iColorInc * _imod(i, 2))

def ColorInc32(i):
    iColor = 0
    MA_Rinc = 0
    MA_Ginc = 0
    MA_Binc = 0
    if i <= 0:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 4:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 48
        MA_Binc = 0
    elif i < 8:
        iColor = 0x00FFFF
        MA_Rinc = -48
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 12:
        iColor = 0x00FF00
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 48
    elif i < 16:
        iColor = 0xFFFF00
        MA_Rinc = 0
        MA_Ginc = -48
        MA_Binc = 0
    elif i < 20:
        iColor = 0xFF0000
        MA_Rinc = 48
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 24:
        iColor = 0xFF00FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = -48
    elif i < 28:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 48
        MA_Binc = 0
    elif i < 32:
        iColor = 0x00FFFF
        MA_Rinc = -48
        MA_Ginc = 0
        MA_Binc = 0
    else:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 0
    iColorInc = MA_Rinc + (256 * MA_Ginc) + (65536 * MA_Binc)
    return iColor + (iColorInc * _imod(i, 4))

def ColorInc96(i):
    iColor = 0
    MA_Rinc = 0
    MA_Ginc = 0
    MA_Binc = 0
    if i <= 0:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 16:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 16
        MA_Binc = 0
    elif i < 32:
        iColor = 0x00FFFF
        MA_Rinc = -16
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 48:
        iColor = 0x00FF00
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 16
    elif i < 64:
        iColor = 0xFFFF00
        MA_Rinc = 0
        MA_Ginc = -16
        MA_Binc = 0
    elif i < 80:
        iColor = 0xFF0000
        MA_Rinc = 16
        MA_Ginc = 0
        MA_Binc = 0
    elif i < 96:
        iColor = 0xFF00FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = -16
    else:
        iColor = 0x0000FF
        MA_Rinc = 0
        MA_Ginc = 0
        MA_Binc = 0
    iColorInc = MA_Rinc + (256 * MA_Ginc) + (65536 * MA_Binc)
    return iColor + (iColorInc * _imod(i, 16))

def SequenceQuadratic(iReturnValue, iSize, i0, im):
    if ArraySize(iReturnValue) < 2:
        return False
    if iSize < 2:
        return False
    iReturnValue[0] = 2
    for i in range(1, iSize):
        iReturnValue[i] = (i + 1) * (i + 1)
    return True

def OnInit():
    MaxBarsinChart = TerminalInfoInteger(TERMINAL_MAXBARS)
    if MaxBarsinChart > 50000:
        Print('Max bars in chart is too large:', MaxBarsinChart)
        Print('Please reduce the number of max bars in chart in the Options to 50000 and restart client terminal')
        return -1
    IndicatorSetString(INDICATOR_SHORTNAME, 'LoongMAx96')
    iColor = _uint(Red)
    bReturn = SequenceQuadratic(iParam, 96, 2, 2)
    iTmp = 0
    for i in range(0, 96):
        MAA[i].Init()
        iTmp = iParam[i]
        MAA[i].mParam = iTmp
        iColor = _uint(ColorInc96(i))
        MAA[i].mSetIndexBuffer(i, INDICATOR_DATA)
        MAA[i].mPlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        MAA[i].mPlotIndexSetInteger(i, PLOT_LINE_STYLE, STYLE_SOLID)
        MAA[i].mPlotIndexSetInteger(i, PLOT_COLOR_INDEXES, 1)
        MAA[i].mPlotIndexSetInteger(i, PLOT_LINE_COLOR, iColor)
        MAA[i].mPlotIndexSetString(i, PLOT_LABEL, 'MA' + IntegerToString(i, 2, 48) + '(color:' + IntegerToString(iColor) + ')')
        MAA[i].mhandle = iMA(None, 0, MAA[i].mParam, shift, smootMode, price)
    return 0

def OnDeinit(reason):
    for i in range(0, 96):
        MAA[i].Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    copied = 0
    for i in range(0, 96):
        copied = MAA[i].mCopyBuffer(prev_calculated, rates_total)
    return rates_total

# ---- global variables initialised from expressions
iColor8Cycle = Arr.of([_uint(Red), _uint(Orange), _uint(Yellow), _uint(Lime), _uint(Aqua), _uint(Blue), _uint(Magenta), _uint(White)], fill=0, dyn=False, size=8)
MAA = Arr(96, 0, dyn=False, factory=CMyBuffer)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Loongmax96(_MQL5Indicator):
    name = 'loongmax96'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'smootMode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'shift': 0,
    }

