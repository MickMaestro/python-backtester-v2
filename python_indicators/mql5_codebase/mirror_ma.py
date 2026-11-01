"""Mirror_MA — converted from MQL5: MQL5 Indicators/Mirror_MA/Mirror_MA.mq5

Mirror MA oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Direct', 2: 'Reverse', 3: 'Signal'}, 'levels': [], 'description': ['Mirror MA oscillator'], 'name': 'Mirror_MA', 'source': 'MQL5 Indicators/Mirror_MA/Mirror_MA.mq5', 'folder': 'Mirror_MA', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 20, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpAppliedPrice1', 'py': 'InpAppliedPrice1', 'param': 'InpAppliedPrice1', 'type': 'int', 'default': 1, 'label': 'First MA applied price', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 20, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpAppliedPrice2', 'py': 'InpAppliedPrice2', 'param': 'InpAppliedPrice2', 'type': 'int', 'default': 2, 'label': 'Second MA applied price', 'sinput': False}, {'mql': 'InpPeriodS', 'py': 'InpPeriodS', 'param': 'InpPeriodS', 'type': 'uint', 'default': 20, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethodS', 'py': 'InpMethodS', 'param': 'InpMethodS', 'type': 'int', 'default': 0, 'label': 'Signal method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 20)  # First MA period
InpMethod1 = _input('InpMethod1', MODE_SMA)  # First MA method
InpAppliedPrice1 = _input('InpAppliedPrice1', PRICE_CLOSE)  # First MA applied price
InpPeriod2 = _input('InpPeriod2', 20)  # Second MA period
InpMethod2 = _input('InpMethod2', MODE_SMA)  # Second MA method
InpAppliedPrice2 = _input('InpAppliedPrice2', PRICE_OPEN)  # Second MA applied price
InpPeriodS = _input('InpPeriodS', 20)  # Signal period
InpMethodS = _input('InpMethodS', MODE_SMA)  # Signal method
BufferB1 = Arr(0, 0.0)
BufferB2 = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
period1 = 0
period2 = 0
periodS = 0
period_max = 0
weight_sum = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma1, handle_ma2, period1, period2, periodS, period_max
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    periodS = (2 if (InpPeriodS < 2) else InpPeriodS)
    period_max = fmax(period1, fmax(period2, periodS))
    if (InpAppliedPrice2 == InpAppliedPrice1 and period1 == period2) and InpMethod1 == InpMethod2:
        Alert('The Applied price, Period and Method of the second MA can not be the same as the Applied price, Period and Method of the first MA.')
        return INIT_FAILED
    SetIndexBuffer(0, BufferB1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferB2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSig, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mirror MA oscillator (' + _str(period1) + ',' + _str(period2) + ',' + _str(periodS) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferB1, True)
    ArraySetAsSeries(BufferB2, True)
    ArraySetAsSeries(BufferSig, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period1, 0, InpMethod1, InpAppliedPrice1)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period1), ') by ', EnumToString(InpAppliedPrice1, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period2, 0, InpMethod2, InpAppliedPrice2)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period2), ') by ', EnumToString(InpAppliedPrice2, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferB1, 0)
        ArrayInitialize(BufferB2, 0)
        ArrayInitialize(BufferSig, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferB1[i] = BufferMA1[i] - BufferMA2[i]
        BufferB2[i] = BufferMA2[i] - BufferMA1[i]
    _sw1 = InpMethodS
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_max, periodS, BufferB1, BufferSig) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_max, periodS, BufferB1, BufferSig) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_max, periodS, BufferB1, BufferSig, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_max, periodS, BufferB1, BufferSig) == 0:
            return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MirrorMA(_MQL5Indicator):
    name = 'Mirror_MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 20,  # First MA period
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpAppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First MA applied price
        'InpPeriod2': 20,  # Second MA period
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
        'InpAppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),  # Second MA applied price
        'InpPeriodS': 20,  # Signal period
        'InpMethodS': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal method
    }

