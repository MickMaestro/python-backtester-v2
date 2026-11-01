"""imafan — converted from MQL5: MQL5 Indicators/iMAFan/imafan.mq5

Copyright: Integer; Link: http://dmffx.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'http://dmffx.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 512, 'indicator_plots': 512}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'imafan', 'source': 'MQL5 Indicators/iMAFan/imafan.mq5', 'folder': 'iMAFan', 'inputs': [{'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'PeriodFrom', 'py': 'PeriodFrom', 'param': 'PeriodFrom', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'PeriodStep', 'py': 'PeriodStep', 'param': 'PeriodStep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Count', 'py': 'Count', 'param': 'Count', 'type': 'int', 'default': 33, 'label': '', 'sinput': False}, {'mql': 'Colors', 'py': 'Colors', 'param': 'Colors', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Color_1', 'py': 'Color_1', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Color_2', 'py': 'Color_2', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Color_3', 'py': 'Color_3', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Color_4', 'py': 'Color_4', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Color_5', 'py': 'Color_5', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Color_6', 'py': 'Color_6', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
MAMethod = _input('MAMethod', 1)
MAPrice = _input('MAPrice', PRICE_CLOSE)
PeriodFrom = _input('PeriodFrom', 10)
PeriodStep = _input('PeriodStep', 3)
Count = _input('Count', 33)
Colors = _input('Colors', 6)
Handle_v = Arr(0, 0)
C = Arr(0, 0)
_Count = 0

class BUF(MqlObject):
    _q_fields = ('Buf',)
    def __init__(self, *args):
        self.Buf = Arr(0, 0.0)

def OnInit():
    global _Count
    _Count = MathMin(Count, 512)
    ArrayResize(B, _Count)
    ArrayResize(Handle_v, _Count)
    ArrayResize(C, 6)
    C[0] = Color_1
    C[1] = Color_2
    C[2] = Color_3
    C[3] = Color_4
    C[4] = Color_5
    C[5] = Color_6
    _Colors = Colors
    if _Colors > 6:
        _Colors = 6
    ArrayResize(C, _Colors)
    for i in range(0, _idiv(_Colors, 2)):
        tmp = C[i]
        C[i] = C[_Colors - 1 - i]
        C[_Colors - 1 - i] = tmp
    CI = Arr(0, 0, dims=(3,))
    ArrayResize(CI, _Count)
    for i in range(0, _Count):
        CI[i][0] = _idiv((_Colors - 1) * i, _Count)
    z = 0
    for i in range(0, _Count - 1):
        if CI[i][0] != CI[i + 1][0]:
            for j in range(z, i + 1):
                CI[j][1] = j - z
                CI[j][2] = i - z + 1
            z = i + 1
    for j in range(z, _Count):
        CI[j][1] = j - z
        CI[j][2] = _Count - z
    for i in range(0, 512):
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, CLR_NONE)
    i = 0
    while i < _Count:
        SetIndexBuffer(i, B[i].Buf, INDICATOR_DATA)
        map_ = PeriodFrom + ((_Count - 1 - i) * PeriodStep)
        PlotIndexSetString(i, PLOT_LABEL, 'MA(' + IntegerToString(map_) + ')')
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, STYLE_SOLID)
        PlotIndexSetInteger(i, PLOT_COLOR_INDEXES, 1)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, GetColor(_fdiv(1.0 * CI[i][1], CI[i][2]), C[CI[i][0]], C[CI[i][0] + 1]))
        PlotIndexSetInteger(i, PLOT_LINE_WIDTH, 1)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0)
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, map_)
        Handle_v[i] = iMA(None, PERIOD_CURRENT, map_, 0, MAMethod, MAPrice)
        i += 1
    return 0

def OnDeinit(reason):
    for i in range(0, _Count):
        ArrayInitialize(B[i].Buf, EMPTY_VALUE)
    for i in range(0, _Count):
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, CLR_NONE)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_NONE)
        IndicatorRelease(Handle_v[i])
    ArrayFree(B)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    for i in range(0, Count):
        if CopyBuffer(Handle_v[i], 0, 0, rates_total - start, B[i].Buf) == -1:
            _s_OnCalculate_error = True
            Alert('er')
            return 0
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
Color_1 = _input('Color_1', _uint(Red))
Color_2 = _input('Color_2', _uint(Yellow))
Color_3 = _input('Color_3', _uint(Lime))
Color_4 = _input('Color_4', _uint(Aqua))
Color_5 = _input('Color_5', _uint(Blue))
Color_6 = _input('Color_6', _uint(Magenta))
B = Arr(0, 0, factory=BUF)

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Imafan(_MQL5Indicator):
    name = 'imafan'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'PeriodFrom': 10,
        'PeriodStep': 3,
        'Count': 33,
        'Colors': 6,
    }

