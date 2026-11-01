"""ASH — converted from MQL5: MQL5 Indicators/ASH/ASH.mq5

Absolute Strength Histogram oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ASH'}, 'levels': [], 'description': ['Absolute Strength Histogram oscillator'], 'name': 'ASH', 'source': 'MQL5 Indicators/ASH/ASH.mq5', 'folder': 'ASH', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 2, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Mode', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_MODE
MODE_RSI = 0
MODE_STO = 1
_enum('ENUM_MODE', {0: 'MODE_RSI', 1: 'MODE_STO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # Period
InpPeriodSm = _input('InpPeriodSm', 2)  # Smoothing
InpMode = _input('InpMode', MODE_RSI)  # Mode
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferASH = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferBL = Arr(0, 0.0)
BufferBR = Arr(0, 0.0)
BufferAvgBL = Arr(0, 0.0)
BufferAvgBR = Arr(0, 0.0)
BufferAvgSmBL = Arr(0, 0.0)
BufferAvgSmBR = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ind = 0
period_sm = 0
period_max = 0
handle_ma = 0
weight_sum_bl = 0
weight_sum_br = 0
weight_sum_sbl = 0
weight_sum_sbr = 0

def OnInit():
    global handle_ma, period_ind, period_max, period_sm
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    period_max = fmax(period_ind, period_sm)
    SetIndexBuffer(0, BufferASH, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferBL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferBR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferAvgBL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgBR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgSmBL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferAvgSmBR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMA, INDICATOR_CALCULATIONS)
    method = StringSubstr(EnumToString(InpMode, 'ENUM_MODE'), 5)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ASH (' + _str(period_ind) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferASH, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferBL, True)
    ArraySetAsSeries(BufferBR, True)
    ArraySetAsSeries(BufferAvgBL, True)
    ArraySetAsSeries(BufferAvgBR, True)
    ArraySetAsSeries(BufferAvgSmBL, True)
    ArraySetAsSeries(BufferAvgSmBR, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferASH, EMPTY_VALUE)
        ArrayInitialize(BufferBL, 0)
        ArrayInitialize(BufferBR, 0)
        ArrayInitialize(BufferAvgBL, 0)
        ArrayInitialize(BufferAvgBR, 0)
        ArrayInitialize(BufferAvgSmBL, 0)
        ArrayInitialize(BufferAvgSmBR, 0)
        ArrayInitialize(BufferMA, 0)
    bars = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, bars, BufferMA)
    if copied != bars:
        return 0
    for i in range(limit, 0 - 1, -1):
        Pr0 = BufferMA[i]
        Pr1 = BufferMA[i + 1]
        if InpMode == MODE_RSI:
            BufferBL[i] = (0.5 * fabs(Pr0 - Pr1)) + Pr0 - Pr1
            BufferBR[i] = (0.5 * fabs(Pr0 - Pr1)) - Pr0 + Pr1
        else:
            bh = Highest(period_ind, i)
            bl = Lowest(period_ind, i)
            if bh == WRONG_VALUE or bl == WRONG_VALUE:
                continue
            max_ = high[bh]
            min_ = low[bl]
            BufferBL[i] = Pr0 - min_
            BufferBR[i] = max_ - Pr0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBL, BufferAvgBL) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBR, BufferAvgBR) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBL, BufferAvgBL) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBR, BufferAvgBR) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferBL, BufferAvgBL, _GlobRef(globals(), 'weight_sum_bl')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferBR, BufferAvgBR, _GlobRef(globals(), 'weight_sum_br')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBL, BufferAvgBL) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBR, BufferAvgBR) == 0:
            return 0
    _sw2 = InpMethod
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBL, BufferAvgSmBL) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBR, BufferAvgSmBR) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBL, BufferAvgSmBL) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBR, BufferAvgSmBR) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBL, BufferAvgSmBL, _GlobRef(globals(), 'weight_sum_sbl')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBR, BufferAvgSmBR, _GlobRef(globals(), 'weight_sum_sbr')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBL, BufferAvgSmBL) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferAvgBR, BufferAvgSmBR) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferASH[i] = _fdiv(BufferAvgSmBL[i] - BufferAvgSmBR[i], Point())
        BufferColors[i] = (0 if (BufferASH[i] > BufferASH[i + 1]) else 1 if (BufferASH[i] < BufferASH[i + 1]) else 2)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ASH(_MQL5Indicator):
    name = 'ASH'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # Period
        'InpPeriodSm': 2,  # Smoothing
        'InpMode': _Choice({0: 'RSI', 1: 'Stochastic'}, default=0),  # Mode
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

