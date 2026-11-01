"""stepma_line — converted from MQL5: MQL5 Indicators/StepMA_Line/stepma_line.mq5

Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 7.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '7.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16748574, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'StepMA Line'}, 'levels': [], 'description': [], 'name': 'stepma_line', 'source': 'MQL5 Indicators/StepMA_Line/stepma_line.mq5', 'folder': 'StepMA_Line', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Volty Length', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 1.0, 'label': 'Sensivity Factor', 'sinput': False}, {'mql': 'StepSize', 'py': 'StepSize', 'param': 'StepSize', 'type': 'int', 'default': 0, 'label': 'Constant Step Size (if need)', 'sinput': False}, {'mql': 'MA_Mode', 'py': 'MA_Mode', 'param': 'MA_Mode', 'type': 'int', 'default': 0, 'label': 'Volty MA Mode : SMA, LWMA', 'sinput': False}, {'mql': 'Advance', 'py': 'Advance', 'param': 'Advance', 'type': 'int', 'default': 0, 'label': 'Offset', 'sinput': False}, {'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'double', 'default': 0.0, 'label': 'Percentage of Up/Down Moving', 'sinput': False}, {'mql': 'Switch', 'py': 'Switch', 'param': 'Switch', 'type': 'int', 'default': 0, 'label': 'High/Low Mode Switch (more sensitive)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
MA_Mode = _input('MA_Mode', SMA)  # Volty MA Mode : SMA, LWMA
Advance = _input('Advance', 0)  # Offset
Percentage = _input('Percentage', 0.0)  # Percentage of Up/Down Moving
Switch = _input('Switch', HighLow)  # High/Low Mode Switch (more sensitive)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
ratio = 0.0
trend1 = 0
trend0 = 0
min_rates_total = 0

def StepSizeCalc(High, Low, Len, Km, Size, bar):
    global _s_StepSizeCalc_ATRmax, _s_StepSizeCalc_ATRmax_, _s_StepSizeCalc_ATRmin, _s_StepSizeCalc_ATRmin_
    ATR0 = 0.0
    result = 0.0
    alfa = 0.0
    if bar == 0:
        _s_StepSizeCalc_ATRmax = _s_StepSizeCalc_ATRmax_
        _s_StepSizeCalc_ATRmin = _s_StepSizeCalc_ATRmin_
    if Size == 0:
        AvgRange = 0.0
        for iii in range(Len - 1, 0 - 1, -1):
            if MA_Mode == SMA:
                alfa = 1.0
            else:
                alfa = 1.0 + _fdiv(1.0 * (Len - iii), Len)
            AvgRange += alfa * (High[bar + iii] - Low[bar + iii])
        ATR0 = _fdiv(AvgRange, Len)
        if ATR0 > _s_StepSizeCalc_ATRmax:
            _s_StepSizeCalc_ATRmax = ATR0
        if ATR0 < _s_StepSizeCalc_ATRmin:
            _s_StepSizeCalc_ATRmin = ATR0
        result = MathRound(_fdiv(0.5 * Km * (_s_StepSizeCalc_ATRmax + _s_StepSizeCalc_ATRmin), Point()))
    else:
        result = Km * StepSize
    if bar == 1:
        _s_StepSizeCalc_ATRmax_ = _s_StepSizeCalc_ATRmax
        _s_StepSizeCalc_ATRmin_ = _s_StepSizeCalc_ATRmin
    return result

def StepMACalc(High, Low, Close, HL, Size, bar):
    global _s_StepMACalc_FirstStart, _s_StepMACalc_smax1, _s_StepMACalc_smin1, trend0, trend1
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
    if bar != 0:
        _s_StepMACalc_smax1 = smax0
        _s_StepMACalc_smin1 = smin0
        trend1 = trend0
    return result

def OnInit():
    global min_rates_total, ratio
    min_rates_total = Length + 3
    ratio = (Percentage / 100.0) * Point()
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorExtBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'StepMA Line (', Length, ', ', Kv, ', ', StepSize, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Step = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Step = StepSizeCalc(high, low, Length, Kv, StepSize, bar)
        if not Step:
            Step = close[bar]
        ExtBuffer[bar] = StepMACalc(high, low, close, (Switch != 0), Step, bar) + _fdiv(ratio, Step)
        if trend0 > 0:
            ColorExtBuffer[bar] = 1.0
        elif trend0 < 0:
            ColorExtBuffer[bar] = 2.0
        else:
            ColorExtBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_StepSizeCalc_ATRmax = -100000.0
_s_StepSizeCalc_ATRmin = 1000000.0
_s_StepSizeCalc_ATRmax_ = 0.0
_s_StepSizeCalc_ATRmin_ = 0.0
_s_StepMACalc_smax1 = 0.0
_s_StepMACalc_smin1 = 0.0
_s_StepMACalc_FirstStart = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepmaLine(_MQL5Indicator):
    name = 'stepma_line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Volty Length
        'Kv': 1.0,  # Sensivity Factor
        'StepSize': 0,  # Constant Step Size (if need)
        'MA_Mode': _Choice({0: 'SMA', 1: 'LWMA'}, default=0),  # Volty MA Mode : SMA, LWMA
        'Advance': 0,  # Offset
        'Percentage': 0.0,  # Percentage of Up/Down Moving
        'Switch': _Choice({0: 'High/Low', 1: 'Close/Close'}, default=0),  # High/Low Mode Switch (more sensitive)
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

