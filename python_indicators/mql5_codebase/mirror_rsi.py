"""Mirror_RSI — converted from MQL5: MQL5 Indicators/Mirror_RSI/Mirror_RSI.mq5

Mirror RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [7451452]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Ascending', 2: 'Descending', 3: 'Signal'}, 'levels': [], 'description': ['Mirror RSI oscillator'], 'name': 'Mirror_RSI', 'source': 'MQL5 Indicators/Mirror_RSI/Mirror_RSI.mq5', 'folder': 'Mirror_RSI', 'inputs': [{'mql': 'InpPeriodRSI1', 'py': 'InpPeriodRSI1', 'param': 'InpPeriodRSI1', 'type': 'uint', 'default': 20, 'label': 'First RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice1', 'py': 'InpAppliedPrice1', 'param': 'InpAppliedPrice1', 'type': 'int', 'default': 1, 'label': 'First RSI applied price', 'sinput': False}, {'mql': 'InpPeriodRSI2', 'py': 'InpPeriodRSI2', 'param': 'InpPeriodRSI2', 'type': 'uint', 'default': 20, 'label': 'Second RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice2', 'py': 'InpAppliedPrice2', 'param': 'InpAppliedPrice2', 'type': 'int', 'default': 2, 'label': 'Second RSI applied price', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 20, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 0, 'label': 'Signal method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodRSI1 = _input('InpPeriodRSI1', 20)  # First RSI period
InpAppliedPrice1 = _input('InpAppliedPrice1', PRICE_CLOSE)  # First RSI applied price
InpPeriodRSI2 = _input('InpPeriodRSI2', 20)  # Second RSI period
InpAppliedPrice2 = _input('InpAppliedPrice2', PRICE_OPEN)  # Second RSI applied price
InpPeriodSig = _input('InpPeriodSig', 20)  # Signal period
InpMethodSig = _input('InpMethodSig', MODE_SMA)  # Signal method
BufferDiff1 = Arr(0, 0.0)
BufferDiff2 = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferRSI1 = Arr(0, 0.0)
BufferRSI2 = Arr(0, 0.0)
period_sig = 0
period_rsi1 = 0
period_rsi2 = 0
period_max = 0
handle_rsi1 = 0
handle_rsi2 = 0
weight_sum = 0

def OnInit():
    global handle_rsi1, handle_rsi2, period_max, period_rsi1, period_rsi2, period_sig
    period_rsi1 = (2 if (InpPeriodRSI1 < 2) else InpPeriodRSI1)
    period_rsi2 = ((period_rsi1 + 1) if (InpPeriodRSI2 == period_rsi1 and InpAppliedPrice2 == InpAppliedPrice1) else 2 if (InpPeriodRSI2 < 2) else InpPeriodRSI2)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    period_max = fmax(period_rsi1, period_rsi2)
    SetIndexBuffer(0, BufferDiff1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDiff2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRSI1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRSI2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mirror RSI (' + _str(period_rsi1) + ',' + _str(period_rsi2) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, period_max)
    ArraySetAsSeries(BufferDiff1, True)
    ArraySetAsSeries(BufferDiff2, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferRSI1, True)
    ArraySetAsSeries(BufferRSI2, True)
    ResetLastError()
    handle_rsi1 = iRSI(None, PERIOD_CURRENT, period_rsi1, InpAppliedPrice1)
    if handle_rsi1 == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi2 = iRSI(None, PERIOD_CURRENT, period_rsi2, InpAppliedPrice2)
    if handle_rsi2 == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_sig, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferDiff1, 0)
        ArrayInitialize(BufferDiff2, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferRSI1, 0)
        ArrayInitialize(BufferRSI2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi1, 0, 0, count, BufferRSI1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi2, 0, 0, count, BufferRSI2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDiff1[i] = BufferRSI1[i] - BufferRSI2[i]
        BufferDiff2[i] = BufferRSI2[i] - BufferRSI1[i]
    _sw1 = InpMethodSig
    if _sw1 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferDiff1, BufferSignal)
    elif _sw1 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferDiff1, BufferSignal)
    elif _sw1 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_max, period_sig, BufferDiff1, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferDiff1, BufferSignal)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MirrorRSI(_MQL5Indicator):
    name = 'Mirror_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI1': 20,  # First RSI period
        'InpAppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First RSI applied price
        'InpPeriodRSI2': 20,  # Second RSI period
        'InpAppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),  # Second RSI applied price
        'InpPeriodSig': 20,  # Signal period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal method
    }

