"""ASO — converted from MQL5: MQL5 Indicators/ASO/ASO.mq5

Average Sentiment Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls', 2: 'Bears'}, 'levels': [], 'description': ['Average Sentiment Oscillator'], 'name': 'ASO', 'source': 'MQL5 Indicators/ASO/ASO.mq5', 'folder': 'ASO', 'inputs': [{'mql': 'InpPeriodRange', 'py': 'InpPeriodRange', 'param': 'InpPeriodRange', 'type': 'uint', 'default': 10, 'label': 'Range period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_MODE
MODE_COMBINED = 0
MODE_INTRA_BAR = 1
MODE_GROUP = 2
_enum('ENUM_MODE', {0: 'MODE_COMBINED', 1: 'MODE_INTRA_BAR', 2: 'MODE_GROUP'})

# ---- inputs and global variables
InpPeriodRange = _input('InpPeriodRange', 10)  # Range period
InpPeriodSm = _input('InpPeriodSm', 10)  # Smoothing period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpMode = _input('InpMode', MODE_COMBINED)  # Mode
BufferBulls = Arr(0, 0.0)
BufferBears = Arr(0, 0.0)
BufferBL = Arr(0, 0.0)
BufferBR = Arr(0, 0.0)
period_range = 0
period_smooth = 0
weight_sum = 0

def OnInit():
    global period_range, period_smooth
    period_range = (1 if (InpPeriodRange < 1) else InpPeriodRange)
    period_smooth = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    SetIndexBuffer(0, BufferBulls, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBears, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferBR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ASO (' + _str(period_range) + ',' + _str(period_smooth) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 100.0)
    ArraySetAsSeries(BufferBulls, True)
    ArraySetAsSeries(BufferBears, True)
    ArraySetAsSeries(BufferBL, True)
    ArraySetAsSeries(BufferBR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_range - 1
        ArrayInitialize(BufferBulls, EMPTY_VALUE)
        ArrayInitialize(BufferBears, EMPTY_VALUE)
        ArrayInitialize(BufferBL, 0)
        ArrayInitialize(BufferBR, 0)
    for i in range(limit, 0 - 1, -1):
        intra_range = high[i] - low[i]
        if intra_range == 0:
            intra_range = 1.0
        bl = LowestHigh(period_range, i)
        bh = HighestLow(period_range, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        group_low = high[bl]
        group_high = low[bh]
        group_open = open[i + period_range]
        group_range = group_high - group_low
        if group_range == 0:
            group_range = 1.0
        intra_bar_bulls = _fdiv(((close[i] - low[i] + (high[i] - open[i])) / 2.0) * 100.0, intra_range)
        group_bulls = _fdiv(((close[i] - group_low + (group_high - group_open)) / 2.0) * 100.0, group_range)
        intra_bar_bears = _fdiv(((high[i] - close[i] + (open[i] - low[i])) / 2.0) * 100.0, intra_range)
        group_bears = _fdiv(((group_high - close[i] + (group_open - group_low)) / 2.0) * 100.0, group_range)
        if InpMode == MODE_COMBINED:
            BufferBL[i] = (intra_bar_bulls + group_bulls) / 2.0
            BufferBR[i] = (intra_bar_bears + group_bears) / 2.0
        else:
            if InpMode == MODE_INTRA_BAR:
                BufferBL[i] = intra_bar_bulls
                BufferBR[i] = intra_bar_bears
            else:
                BufferBL[i] = group_bulls
                BufferBR[i] = group_bears
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferBL, BufferBulls) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferBR, BufferBears) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferBL, BufferBulls) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferBR, BufferBears) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_smooth, BufferBL, BufferBulls, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_smooth, BufferBR, BufferBears, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferBL, BufferBulls) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferBR, BufferBears) == 0:
            return 0
    return rates_total

def HighestLow(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def LowestHigh(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ASO(_MQL5Indicator):
    name = 'ASO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRange': 10,  # Range period
        'InpPeriodSm': 10,  # Smoothing period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpMode': _Choice({0: 'Combined', 1: 'Intra-bar', 2: 'Group algorithm'}, default=0),  # Mode
    }

