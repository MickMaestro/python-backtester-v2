"""stepma_nrtr — converted from MQL5: MQL5 Indicators/StepMA_NRTR/stepma_nrtr.mq5

Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 8.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '8.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [14822282], 2: [55295], 3: [8388352], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper StepMA', 2: 'Lower StepMA', 3: 'StepMA Buy', 4: 'StepMA Sell'}, 'levels': [], 'description': [], 'name': 'stepma_nrtr', 'source': 'MQL5 Indicators/StepMA_NRTR/stepma_nrtr.mq5', 'folder': 'StepMA_NRTR', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Volty Length', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 1.0, 'label': 'Sensivity Factor', 'sinput': False}, {'mql': 'StepSize', 'py': 'StepSize', 'param': 'StepSize', 'type': 'int', 'default': 0, 'label': 'Constant Step Size (if need)', 'sinput': False}, {'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'double', 'default': 0.0, 'label': 'Percentage of Up/Down Moving', 'sinput': False}, {'mql': 'Switch', 'py': 'Switch', 'param': 'Switch', 'type': 'int', 'default': 0, 'label': 'High/Low Mode Switch (more sensitive)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MA_MODE
SMA = 0
LWMA = 1
_enum('MA_MODE', {0: 'SMA', 1: 'LWMA'})

# enum PRICE_MODE
HighLow = 0
CloseClose = 1
_enum('PRICE_MODE', {0: 'HighLow', 1: 'CloseClose'})

# ---- inputs and global variables
Length = _input('Length', 10)  # Volty Length
Kv = _input('Kv', 1.0)  # Sensivity Factor
StepSize = _input('StepSize', 0)  # Constant Step Size (if need)
Percentage = _input('Percentage', 0.0)  # Percentage of Up/Down Moving
Switch = _input('Switch', HighLow)  # High/Low Mode Switch (more sensitive)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ratio = 0.0
trend1 = 0
trend1_ = 0
trend0 = 0
min_rates_total = 0

def StepSizeCalc(High, Low, Len, Km, Size, bar):
    result = 0.0
    if not Size:
        Range = 0.0
        ATRmax = -1000000.0
        ATRmin = 1000000.0
        for iii in range(Len - 1, 0 - 1, -1):
            Range = High[bar + iii] - Low[bar + iii]
            if Range > ATRmax:
                ATRmax = Range
            if Range < ATRmin:
                ATRmin = Range
        result = MathRound(_fdiv(0.5 * Km * (ATRmax + ATRmin), Point()))
    else:
        result = Km * Size
    return result

def StepMACalc(High, Low, Close, HL, Size, bar):
    global _s_StepMACalc_FirstStart, _s_StepMACalc_smax1, _s_StepMACalc_smin1, trend0, trend1, trend1_
    result = 0.0
    smax0 = 0.0
    smin0 = 0.0
    SizeP = 0.0
    Size2P = 0.0
    SizeP = Size * Point()
    Size2P = 2.0 * SizeP
    if _s_StepMACalc_FirstStart:
        trend1 = 0
        _s_StepMACalc_smax1 = Low[bar] + Size2P
        _s_StepMACalc_smin1 = High[bar] - Size2P
        _s_StepMACalc_FirstStart = False
    if HL:
        smax0 = Low[bar] + Size2P
        smin0 = High[bar] - Size2P
    else:
        smax0 = Close[bar] + Size2P
        smin0 = Close[bar] - Size2P
    trend0 = trend1
    if Close[bar] > _s_StepMACalc_smax1:
        trend0 = 1
    if Close[bar] < _s_StepMACalc_smin1:
        trend0 = -1
    if trend0 > 0:
        if smin0 < _s_StepMACalc_smin1:
            smin0 = _s_StepMACalc_smin1
        result = smin0 + SizeP
    else:
        if smax0 > _s_StepMACalc_smax1:
            smax0 = _s_StepMACalc_smax1
        result = smax0 - SizeP
    trend1_ = trend1
    if bar:
        _s_StepMACalc_smax1 = smax0
        _s_StepMACalc_smin1 = smin0
        trend1 = trend0
    return result

def OnInit():
    global min_rates_total, ratio
    min_rates_total = Length + 3
    ratio = (Percentage / 100.0) * Point()
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    shortname = Box("")
    StringConcatenate(shortname, 'StepMA NRTR (', Length, ', ', Kv, ', ', StepSize, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global trend1_
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    StepMA = 0.0
    Step = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        trend1_ = 0
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        BuyBuffer[bar] = EMPTY_VALUE
        Step = StepSizeCalc(high, low, Length, Kv, StepSize, bar)
        if not Step:
            Step = 1.0
        StepMA = StepMACalc(high, low, close, (Switch != 0), Step, bar) + _fdiv(ratio, Step)
        if trend0 > 0:
            UpBuffer[bar] = StepMA - (Step * Point())
            if trend1_ < 0:
                BuyBuffer[bar] = UpBuffer[bar]
            DnBuffer[bar] = EMPTY_VALUE
        if trend0 < 0:
            DnBuffer[bar] = StepMA + (Step * Point())
            if trend1_ > 0:
                SellBuffer[bar] = DnBuffer[bar]
            UpBuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_StepMACalc_smax1 = 0.0
_s_StepMACalc_smin1 = 0.0
_s_StepMACalc_FirstStart = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepmaNrtr(_MQL5Indicator):
    name = 'stepma_nrtr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Volty Length
        'Kv': 1.0,  # Sensivity Factor
        'StepSize': 0,  # Constant Step Size (if need)
        'Percentage': 0.0,  # Percentage of Up/Down Moving
        'Switch': _Choice({0: 'High/Low', 1: 'Close/Close'}, default=0),  # High/Low Mode Switch (more sensitive)
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

