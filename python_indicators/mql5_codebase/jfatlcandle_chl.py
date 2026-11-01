"""JFatlCandle_Chl — converted from MQL5: MQL5 Indicators/JFatlCandle_Chl/JFatlCandle_Chl.mq5

Индикатор JFatl в свечном виде
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 17}, 'colors': {1: [15269855], 2: [16773887], 3: [16747263, 8421504, 16759413]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper Signal Cloud', 2: 'Lower Signal Cloud', 3: 'JFatlCandle Open;JFatlCandle High;JFatlCandle Low;JFatlCandle Close'}, 'levels': [], 'description': ['Индикатор JFatl в свечном виде'], 'name': 'JFatlCandle_Chl', 'source': 'MQL5 Indicators/JFatlCandle_Chl/JFatlCandle_Chl.mq5', 'folder': 'JFatlCandle_Chl', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'uint', 'default': 5, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'параметр JMA сглаживания,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BBLength', 'py': 'BBLength', 'param': 'BBLength', 'type': 'uint', 'default': 10, 'label': 'период Боллинджера', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'девиация', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
JLength = _input('JLength', 5)  # глубина JMA сглаживания
JPhase = _input('JPhase', 100)  # параметр JMA сглаживания,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BBLength = _input('BBLength', 10)  # период Боллинджера
BandsDeviation = _input('BandsDeviation', 1.0)  # девиация
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
FATLSize = 0
dFATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)

def OnInit():
    global FATLSize, min_rates_1, min_rates_total
    min_rates_1 = 39 + 30
    min_rates_total = min_rates_1 + _int(BBLength)
    FATLSize = ArraySize(dFATLTable)
    IndInit(0, UpUpBuffer, INDICATOR_DATA)
    IndInit(1, UpDnBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, 0)
    IndInit(2, DnUpBuffer, INDICATOR_DATA)
    IndInit(3, DnDnBuffer, INDICATOR_DATA)
    PlotInit(1, 0.0, min_rates_total, 0)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotInit(2, 0.0, min_rates_1, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'JFatlCandle_Chl'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    FATLO = 0.0
    FATLH = 0.0
    FATLL = 0.0
    FATLC = 0.0
    stdev = 0.0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FATLSize - 1
        ExtCloseBuffer[first - 1] = close[first - 1]
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        FATLO = 0.0
        for index in range(0, FATLSize):
            FATLO += dFATLTable[index] * open[bar - index]
        O = XMAo.XMASeries(FATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, FATLO, bar, False)
        FATLH = 0.0
        for index in range(0, FATLSize):
            FATLH += dFATLTable[index] * high[bar - index]
        H = XMAh.XMASeries(FATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, FATLH, bar, False)
        FATLL = 0.0
        for index in range(0, FATLSize):
            FATLL += dFATLTable[index] * low[bar - index]
        L = XMAl.XMASeries(FATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, FATLL, bar, False)
        FATLC = 0.0
        for index in range(0, FATLSize):
            FATLC += dFATLTable[index] * close[bar - index]
        C = XMAc.XMASeries(FATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, FATLC, bar, False)
        Max = MathMax(O, C)
        Max = MathMax(Max, L)
        Max = MathMax(Max, H)
        Min = MathMin(O, C)
        Min = MathMin(Min, L)
        Min = MathMin(Min, H)
        ExtOpenBuffer[bar] = O
        ExtHighBuffer[bar] = Max
        ExtLowBuffer[bar] = Min
        ExtCloseBuffer[bar] = C
        if MathAbs(open[bar] - close[bar]) <= Gap:
            ExtOpenBuffer[bar] = ExtCloseBuffer[bar - 1]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        stdev = STDh.StdDevSeries(min_rates_1, prev_calculated, rates_total, BBLength, BandsDeviation, FATLH, ExtHighBuffer[bar], bar, False)
        UpUpBuffer[bar] = ExtHighBuffer[bar] + stdev
        UpDnBuffer[bar] = ExtHighBuffer[bar]
        DnUpBuffer[bar] = ExtLowBuffer[bar]
        stdev = STDl.StdDevSeries(min_rates_1, prev_calculated, rates_total, BBLength, BandsDeviation, FATLL, ExtLowBuffer[bar], bar, False)
        DnDnBuffer[bar] = ExtLowBuffer[bar] - stdev
    return rates_total

# ---- global variables initialised from expressions
XMAo = _alloc(CXMA)
XMAo.__init__()
XMAh = _alloc(CXMA)
XMAh.__init__()
XMAl = _alloc(CXMA)
XMAl.__init__()
XMAc = _alloc(CXMA)
XMAc.__init__()
STDh = _alloc(CStdDeviation)
STDh.__init__()
STDl = _alloc(CStdDeviation)
STDl.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JFatlCandleChl(_MQL5Indicator):
    name = 'JFatlCandle_Chl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 5,  # глубина JMA сглаживания
        'JPhase': 100,  # параметр JMA сглаживания,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BBLength': 10,  # период Боллинджера
        'BandsDeviation': 1.0,  # девиация
    }

