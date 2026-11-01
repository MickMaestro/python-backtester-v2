"""JFatl_Digit_System — converted from MQL5: MQL5 Indicators/JFatl_Digit_System/JFatl_Digit_System.mq5

Пробойная система с использованием индикатора JFatl_Digit
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 11}, 'colors': {1: [16119285], 2: [7451452], 3: [16711935], 4: [9639167, 8388736, 8421504, 13434880, 16748574]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'JFatl_Digit', 2: 'Upper JFatl_Digit', 3: 'Lower JFatl_Digit', 4: 'JFatl_Digit_BARS'}, 'levels': [], 'description': ['Пробойная система с использованием индикатора JFatl_Digit'], 'name': 'JFatl_Digit_System', 'source': 'MQL5 Indicators/JFatl_Digit_System/JFatl_Digit_System.mq5', 'folder': 'JFatl_Digit_System', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorJFatl_Digit', 'label': 'первая часть имени графических объектов', 'sinput': False}, {'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 5, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': -100, 'label': 'параметр JMA сглаживания,', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг канала по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 2, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Up_Price_color', 'py': 'Up_Price_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'Dn_Price_color', 'py': 'Dn_Price_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
SirName = _input('SirName', 'ColorJFatl_Digit')  # первая часть имени графических объектов
JLength = _input('JLength', 5)  # глубина JMA сглаживания
JPhase = _input('JPhase', -100)  # параметр JMA сглаживания,
PriceShift = _input('PriceShift', 0)  # cдвиг канала по вертикали в пунктах
Shift = _input('Shift', 2)  # сдвиг канала по горизонтали в барах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Up_Price_color = _input('Up_Price_color', clrTeal)
Dn_Price_color = _input('Dn_Price_color', clrMagenta)
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
FATLPeriod = 39
FATLSize = 0
dPriceShift = 0.0
PointPow10 = 0.0
Dn_Price_name = ""
Up_Price_name = ""
dFATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)

def OnInit():
    global Dn_Price_name, FATLSize, PointPow10, Up_Price_name, dPriceShift, min_rates_total
    FATLSize = ArraySize(dFATLTable)
    min_rates_total = FATLSize + 30 + _int(Shift)
    dPriceShift = Point() * PriceShift
    PointPow10 = Point() * MathPow(10, Digit)
    Up_Price_name = SirName + 'Up_Price'
    Dn_Price_name = SirName + 'Dn_Price'
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, DnIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_SHIFT, 0)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'JFatl_Digit_System(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, Up_Price_name)
    ObjectDelete(0, Dn_Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_fstart
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    jfatl = 0.0
    FATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FATLPeriod - 1
        _s_OnCalculate_fstart = first
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FATL = 0.0
        for iii in range(0, FATLSize):
            FATL += dFATLTable[iii] * high[bar - iii]
        jfatl = HJMA.JJMASeries(_s_OnCalculate_fstart, prev_calculated, rates_total, 0, JPhase, JLength, FATL, bar, False)
        jfatl += dPriceShift
        Up2Buffer[bar] = PointPow10 * MathRound(_fdiv(jfatl, PointPow10))
        Up1Buffer[bar] = Up2Buffer[bar]
        FATL = 0.0
        for iii in range(0, FATLSize):
            FATL += dFATLTable[iii] * low[bar - iii]
        jfatl = LJMA.JJMASeries(_s_OnCalculate_fstart, prev_calculated, rates_total, 0, JPhase, JLength, FATL, bar, False)
        jfatl += dPriceShift
        Dn2Buffer[bar] = PointPow10 * MathRound(_fdiv(jfatl, PointPow10))
        Dn1Buffer[bar] = Dn2Buffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        UpIndBuffer[bar] = 0.0
        DnIndBuffer[bar] = 0.0
        if close[bar] > Up1Buffer[bar - Shift]:
            if open[bar] < close[bar]:
                clr = 4
            else:
                clr = 3
            UpIndBuffer[bar] = high[bar]
            DnIndBuffer[bar] = low[bar]
        if close[bar] < Dn1Buffer[bar - Shift]:
            if open[bar] > close[bar]:
                clr = 0
            else:
                clr = 1
            UpIndBuffer[bar] = high[bar]
            DnIndBuffer[bar] = low[bar]
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (Shift * PeriodSeconds())
        SetRightPrice(0, Up_Price_name, 0, time0, Up1Buffer[bar0 - Shift], Up_Price_color)
        SetRightPrice(0, Dn_Price_name, 0, time0, Dn1Buffer[bar0 - Shift], Dn_Price_color)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- global variables initialised from expressions
HJMA = _alloc(CJJMA)
HJMA.__init__()
LJMA = _alloc(CJJMA)
LJMA.__init__()

# ---- static local variables
_s_OnCalculate_fstart = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JFatlDigitSystem(_MQL5Indicator):
    name = 'JFatl_Digit_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 5,  # глубина JMA сглаживания
        'JPhase': -100,  # параметр JMA сглаживания,
        'PriceShift': 0,  # cдвиг канала по вертикали в пунктах
        'Shift': 2,  # сдвиг канала по горизонтали в барах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

