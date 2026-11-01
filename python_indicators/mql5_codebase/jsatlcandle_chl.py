"""JSatlCandle_Chl — converted from MQL5: MQL5 Indicators/JSatlCandle_Chl/JSatlCandle_Chl.mq5

Индикатор JSatl в свечном виде
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 17}, 'colors': {1: [15269855], 2: [16773887], 3: [7983359, 8421504, 16777066]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper Signal Cloud', 2: 'Lower Signal Cloud', 3: 'JSatlCandle Open;JSatlCandle High;JSatlCandle Low;JSatlCandle Close'}, 'levels': [], 'description': ['Индикатор JSatl в свечном виде'], 'name': 'JSatlCandle_Chl', 'source': 'MQL5 Indicators/JSatlCandle_Chl/JSatlCandle_Chl.mq5', 'folder': 'JSatlCandle_Chl', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'uint', 'default': 5, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'параметр JMA сглаживания,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BBLength', 'py': 'BBLength', 'param': 'BBLength', 'type': 'uint', 'default': 20, 'label': 'период Боллинджера', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 3.0, 'label': 'девиация', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
JLength = _input('JLength', 5)  # глубина JMA сглаживания
JPhase = _input('JPhase', 100)  # параметр JMA сглаживания,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BBLength = _input('BBLength', 20)  # период Боллинджера
BandsDeviation = _input('BandsDeviation', 3.0)  # девиация
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
SATLSize = 0
dSATLTable = Arr.of([-0.00514293, -0.00398417, -0.00262594, -0.00107121, 0.00066887, 0.00258172, 0.00465269, 0.00686394, 0.00919334, 0.0116172, 0.01411056, 0.01664635, 0.01919533, 0.02172747, 0.0242132, 0.02662203, 0.02892446, 0.03109071, 0.03309496, 0.03490921, 0.03651145, 0.03788045, 0.03899804, 0.03984915, 0.04042329, 0.04071263, 0.04071263, 0.04042329, 0.03984915, 0.03899804, 0.03788045, 0.03651145, 0.03490921, 0.03309496, 0.03109071, 0.02892446, 0.02662203, 0.0242132, 0.02172747, 0.01919533, 0.01664635, 0.01411056, 0.0116172, 0.00919334, 0.00686394, 0.00465269, 0.00258172, 0.00066887, -0.00107121, -0.00262594, -0.00398417, -0.00514293, -0.00609634, -0.00684602, -0.00739452, -0.00774847, -0.0079163, -0.0079094, -0.00774085, -0.00742482, -0.00697718, -0.00641613, -0.00576108, -0.00502957, -0.00423873, -0.00340812, -0.00255923, -0.00170217, -0.00085902, -4.113e-05, 0.000737, 0.00146422, 0.00213007, 0.00272649, 0.00324752, 0.00368922, 0.00405, 0.00433024, 0.00453068, 0.00465046, 0.00469058, 0.00466041, 0.00457855, 0.00442491, 0.00423019, 0.00399201, 0.00372169, 0.00342736, 0.00311822, 0.00280309, 0.00249088, 0.00219089, 0.00191283, 0.00166683, 0.00146419, 0.00131867, 0.00124645, 0.00126836, -0.00401854], fill=0.0)

def OnInit():
    global SATLSize, min_rates_1, min_rates_total
    SATLSize = ArraySize(dSATLTable)
    min_rates_1 = SATLSize + 30
    min_rates_total = min_rates_1 + _int(BBLength)
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
    short_name = 'JSatlCandle_Chl'
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
    SATLO = 0.0
    SATLH = 0.0
    SATLL = 0.0
    SATLC = 0.0
    stdev = 0.0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = SATLSize - 1
        ExtCloseBuffer[first - 1] = close[first - 1]
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        SATLO = 0.0
        for index in range(0, SATLSize):
            SATLO += dSATLTable[index] * open[bar - index]
        O = XMAo.XMASeries(SATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, SATLO, bar, False)
        SATLH = 0.0
        for index in range(0, SATLSize):
            SATLH += dSATLTable[index] * high[bar - index]
        H = XMAh.XMASeries(SATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, SATLH, bar, False)
        SATLL = 0.0
        for index in range(0, SATLSize):
            SATLL += dSATLTable[index] * low[bar - index]
        L = XMAl.XMASeries(SATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, SATLL, bar, False)
        SATLC = 0.0
        for index in range(0, SATLSize):
            SATLC += dSATLTable[index] * close[bar - index]
        C = XMAc.XMASeries(SATLSize - 1, prev_calculated, rates_total, 5, JPhase, JLength, SATLC, bar, False)
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
        stdev = STDh.StdDevSeries(min_rates_1, prev_calculated, rates_total, BBLength, BandsDeviation, SATLH, ExtHighBuffer[bar], bar, False)
        UpUpBuffer[bar] = ExtHighBuffer[bar] + stdev
        UpDnBuffer[bar] = ExtHighBuffer[bar]
        DnUpBuffer[bar] = ExtLowBuffer[bar]
        stdev = STDl.StdDevSeries(min_rates_1, prev_calculated, rates_total, BBLength, BandsDeviation, SATLL, ExtLowBuffer[bar], bar, False)
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


class JSatlCandleChl(_MQL5Indicator):
    name = 'JSatlCandle_Chl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 5,  # глубина JMA сглаживания
        'JPhase': 100,  # параметр JMA сглаживания,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BBLength': 20,  # период Боллинджера
        'BandsDeviation': 3.0,  # девиация
    }

