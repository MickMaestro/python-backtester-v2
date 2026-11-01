"""MACD_Squeeze — converted from MQL5: MQL5 Indicators/MACD_Squeeze/MACD_Squeeze.mq5

MACD Squeeze oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 10, 2: 5, 3: 5}, 'colors': {1: [32768, 255], 2: [16711680], 3: [12632256]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MACDS', 2: 'Signal IN', 3: 'Signal OUT'}, 'levels': [], 'description': ['MACD Squeeze oscillator'], 'name': 'MACD_Squeeze', 'source': 'MQL5 Indicators/MACD_Squeeze/MACD_Squeeze.mq5', 'folder': 'MACD_Squeeze', 'inputs': [{'mql': 'InpPeriodFastEMA', 'py': 'InpPeriodFastEMA', 'param': 'InpPeriodFastEMA', 'type': 'uint', 'default': 8, 'label': 'MACD Fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlowEMA', 'py': 'InpPeriodSlowEMA', 'param': 'InpPeriodSlowEMA', 'type': 'uint', 'default': 21, 'label': 'MACD Slow EMA period', 'sinput': False}, {'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 20, 'label': 'Bollinger Bands period', 'sinput': False}, {'mql': 'InpDeviationBB', 'py': 'InpDeviationBB', 'param': 'InpDeviationBB', 'type': 'double', 'default': 2.0, 'label': 'Bollinger Bands deviation', 'sinput': False}, {'mql': 'InpMethodBB', 'py': 'InpMethodBB', 'param': 'InpMethodBB', 'type': 'int', 'default': 1, 'label': 'Bollinger Bands MA method', 'sinput': False}, {'mql': 'InpPeriodKeltner', 'py': 'InpPeriodKeltner', 'param': 'InpPeriodKeltner', 'type': 'uint', 'default': 20, 'label': 'Keltner period', 'sinput': False}, {'mql': 'InpDeviationKeltner', 'py': 'InpDeviationKeltner', 'param': 'InpDeviationKeltner', 'type': 'double', 'default': 1.5, 'label': 'Keltner deviation', 'sinput': False}, {'mql': 'InpPeriodATRKeltner', 'py': 'InpPeriodATRKeltner', 'param': 'InpPeriodATRKeltner', 'type': 'uint', 'default': 10, 'label': 'Keltner ATR period', 'sinput': False}, {'mql': 'InpMethodKeltner', 'py': 'InpMethodKeltner', 'param': 'InpMethodKeltner', 'type': 'int', 'default': 1, 'label': 'Keltner MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastEMA = _input('InpPeriodFastEMA', 8)  # MACD Fast EMA period
InpPeriodSlowEMA = _input('InpPeriodSlowEMA', 21)  # MACD Slow EMA period
InpPeriodBB = _input('InpPeriodBB', 20)  # Bollinger Bands period
InpDeviationBB = _input('InpDeviationBB', 2.0)  # Bollinger Bands deviation
InpMethodBB = _input('InpMethodBB', MODE_EMA)  # Bollinger Bands MA method
InpPeriodKeltner = _input('InpPeriodKeltner', 20)  # Keltner period
InpDeviationKeltner = _input('InpDeviationKeltner', 1.5)  # Keltner deviation
InpPeriodATRKeltner = _input('InpPeriodATRKeltner', 10)  # Keltner ATR period
InpMethodKeltner = _input('InpMethodKeltner', MODE_EMA)  # Keltner MA method
BufferMACD = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSqueezeIN = Arr(0, 0.0)
BufferSqueezeOUT = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferBBMA = Arr(0, 0.0)
BufferBBDEV = Arr(0, 0.0)
BufferKMA = Arr(0, 0.0)
BufferKATR = Arr(0, 0.0)
period_fema = 0
period_sema = 0
period_bb = 0
period_klt = 0
period_katr = 0
handle_fma = 0
handle_sma = 0
handle_bbma = 0
handle_bbdev = 0
handle_kma = 0
handle_katr = 0
dev_bb = 0.0
dev_klt = 0.0

def OnInit():
    global dev_bb, dev_klt, handle_bbdev, handle_bbma, handle_fma, handle_katr, handle_kma, handle_sma, period_bb, period_fema, period_katr, period_klt, period_sema
    period_fema = (1 if (InpPeriodFastEMA < 1) else InpPeriodFastEMA)
    period_sema = (1 if (InpPeriodSlowEMA < 1) else InpPeriodSlowEMA)
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    period_klt = (1 if (InpPeriodKeltner < 1) else InpPeriodKeltner)
    period_katr = (1 if (InpPeriodATRKeltner < 1) else InpPeriodATRKeltner)
    dev_bb = InpDeviationBB
    dev_klt = InpDeviationKeltner
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSqueezeIN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSqueezeOUT, INDICATOR_DATA)
    SetIndexBuffer(4, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferBBMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferBBDEV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferKMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferKATR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetInteger(2, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD Squeeze (' + _str(period_fema) + ',' + _str(period_sema) + ',' + _str(period_bb) + ',' + _str(period_klt) + ',' + _str(period_katr) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSqueezeIN, True)
    ArraySetAsSeries(BufferSqueezeOUT, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferBBMA, True)
    ArraySetAsSeries(BufferBBDEV, True)
    ArraySetAsSeries(BufferKMA, True)
    ArraySetAsSeries(BufferKATR, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_fma == INVALID_HANDLE:
        Print(112, ': The iMA(', _str(period_fema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_sma == INVALID_HANDLE:
        Print(118, ': The iMA(', _str(period_sema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_bbma = iMA(None, PERIOD_CURRENT, period_bb, 0, InpMethodBB, PRICE_CLOSE)
    if handle_bbma == INVALID_HANDLE:
        Print(124, ': The iMA(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_bbdev = iStdDev(None, PERIOD_CURRENT, period_bb, 0, MODE_SMA, PRICE_CLOSE)
    if handle_bbdev == INVALID_HANDLE:
        Print(130, ': The iStdDev(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_kma = iMA(None, PERIOD_CURRENT, period_klt, 0, InpMethodKeltner, PRICE_CLOSE)
    if handle_kma == INVALID_HANDLE:
        Print(137, ': The iMA(', _str(period_klt), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_katr = iATR(None, PERIOD_CURRENT, period_katr)
    if handle_katr == INVALID_HANDLE:
        Print(144, ': The iATR(', _str(period_katr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferSqueezeIN, EMPTY_VALUE)
        ArrayInitialize(BufferSqueezeOUT, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferBBMA, 0)
        ArrayInitialize(BufferBBDEV, 0)
        ArrayInitialize(BufferKMA, 0)
        ArrayInitialize(BufferKATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bbma, 0, 0, count, BufferBBMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bbdev, 0, 0, count, BufferBBDEV)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_kma, 0, 0, count, BufferKMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_katr, 0, 0, count, BufferKATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMACD[i] = BufferFMA[i] - BufferSMA[i]
        BufferColors[i] = (1 if (BufferMACD[i] < BufferMACD[i + 1]) else 0)
        BB_MA = BufferBBMA[i]
        BB_StdDev = BufferBBDEV[i]
        BTL = BB_MA + (BB_StdDev * InpDeviationBB)
        BBL = BB_MA - (BB_StdDev * InpDeviationBB)
        K_MA = BufferKMA[i]
        K_ATR = BufferKATR[i]
        KTL = K_MA + (K_ATR * InpDeviationKeltner)
        KBL = K_MA - (K_ATR * InpDeviationKeltner)
        if BTL < KTL and BBL > KBL:
            BufferSqueezeOUT[i] = EMPTY_VALUE
            BufferSqueezeIN[i] = 0.0
        else:
            BufferSqueezeIN[i] = EMPTY_VALUE
            BufferSqueezeOUT[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDSqueeze(_MQL5Indicator):
    name = 'MACD_Squeeze'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastEMA': 8,  # MACD Fast EMA period
        'InpPeriodSlowEMA': 21,  # MACD Slow EMA period
        'InpPeriodBB': 20,  # Bollinger Bands period
        'InpDeviationBB': 2.0,  # Bollinger Bands deviation
        'InpMethodBB': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Bollinger Bands MA method
        'InpPeriodKeltner': 20,  # Keltner period
        'InpDeviationKeltner': 1.5,  # Keltner deviation
        'InpPeriodATRKeltner': 10,  # Keltner ATR period
        'InpMethodKeltner': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Keltner MA method
    }

