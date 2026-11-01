"""FineTuningMACandle_Chl — converted from MQL5: MQL5 Indicators/FineTuningMACandle_Chl_HTF/FineTuningMACandle_Chl.mq5

Свечной график на более тонком усреднении таймсерий
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 17}, 'colors': {1: [14942122], 2: [12320767], 3: [9639167, 8421504, 15570276]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper Signal Cloud', 2: 'Lower Signal Cloud', 3: 'FineTuningMA Open;FineTuningMA High;FineTuningMA Low;FineTuningMA Close'}, 'levels': [], 'description': ['Свечной график на более тонком усреднении таймсерий'], 'name': 'FineTuningMACandle_Chl', 'source': 'MQL5 Indicators/FineTuningMACandle_Chl_HTF/FineTuningMACandle_Chl.mq5', 'folder': 'FineTuningMACandle_Chl_HTF', 'inputs': [{'mql': 'FTMA', 'py': 'FTMA', 'param': 'FTMA', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'rank1', 'py': 'rank1', 'param': 'rank1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank2', 'py': 'rank2', 'param': 'rank2', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank3', 'py': 'rank3', 'param': 'rank3', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BBLength', 'py': 'BBLength', 'param': 'BBLength', 'type': 'uint', 'default': 10, 'label': 'период Боллинджера', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'девиация', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FTMA = _input('FTMA', 10)
rank1 = _input('rank1', 2.0)
rank2 = _input('rank2', 2.0)
rank3 = _input('rank3', 2.0)
Shift1 = _input('Shift1', 1.0)
Shift2 = _input('Shift2', 1.0)
Shift3 = _input('Shift3', 1.0)
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
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
PM = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global dPriceShift, min_rates_1, min_rates_total
    dPriceShift = Point() * PriceShift
    ArrayResize(PM, FTMA)
    sum_ = 0.0
    for h in range(0, _int(FTMA)):
        PM[h] = Shift1 + (MathPow(_fdiv(h, FTMA - 1.0), rank1) * (1.0 - Shift1))
        PM[h] = (Shift2 + (MathPow(1 - _fdiv(h, FTMA - 1.0), rank2) * (1.0 - Shift2))) * PM[h]
        if _fdiv(h, FTMA - 1.0) < 0.5:
            PM[h] = (Shift3 + (MathPow(1 - (_fdiv(h, FTMA - 1.0) * 2.0), rank3) * (1.0 - Shift3))) * PM[h]
        else:
            PM[h] = (Shift3 + (MathPow((_fdiv(h, FTMA - 1.0) * 2.0) - 1.0, rank3) * (1.0 - Shift3))) * PM[h]
        sum_ += PM[h]
    sum1 = 0.0
    for h in range(0, _int(FTMA)):
        PM[h] = _fdiv(PM[h], sum_)
        sum1 += PM[h]
    min_rates_1 = _int(FTMA) + 1
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'FineTuningMACandle_Chl(' + _str(FTMA) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    stdev = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        O = 0.0
        for index in range(0, _int(FTMA)):
            O += PM[index] * open[bar - index]
        H = 0.0
        for index in range(0, _int(FTMA)):
            H += PM[index] * high[bar - index]
        L = 0.0
        for index in range(0, _int(FTMA)):
            L += PM[index] * low[bar - index]
        C = 0.0
        for index in range(0, _int(FTMA)):
            C += PM[index] * close[bar - index]
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
            ExtOpenBuffer[bar] = ExtCloseBuffer[MathMax(bar - 1, 0)]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        ExtOpenBuffer[bar] += dPriceShift
        ExtHighBuffer[bar] += dPriceShift
        ExtLowBuffer[bar] += dPriceShift
        ExtCloseBuffer[bar] += dPriceShift
        stdev = STDh.StdDevSeries(min_rates_1, prev_calculated, rates_total, BBLength, BandsDeviation, high[bar], ExtHighBuffer[bar], bar, False)
        UpUpBuffer[bar] = ExtHighBuffer[bar] + stdev
        UpDnBuffer[bar] = ExtHighBuffer[bar]
        DnUpBuffer[bar] = ExtLowBuffer[bar]
        stdev = STDl.StdDevSeries(min_rates_1, prev_calculated, rates_total, BBLength, BandsDeviation, low[bar], ExtLowBuffer[bar], bar, False)
        DnDnBuffer[bar] = ExtLowBuffer[bar] - stdev
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
STDh = _alloc(CStdDeviation)
STDh.__init__()
STDl = _alloc(CStdDeviation)
STDl.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FineTuningMACandleChl(_MQL5Indicator):
    name = 'FineTuningMACandle_Chl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FTMA': 10,
        'rank1': 2.0,
        'rank2': 2.0,
        'rank3': 2.0,
        'Shift1': 1.0,
        'Shift2': 1.0,
        'Shift3': 1.0,
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BBLength': 10,  # период Боллинджера
        'BandsDeviation': 1.0,  # девиация
    }

