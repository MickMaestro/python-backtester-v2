"""Lentz_Volatility — converted from MQL5: MQL5 Indicators/Lentz_Volatility/Lentz_Volatility.mq5

Lentz Volatility oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Lentz Vol'}, 'levels': [], 'description': ['Lentz Volatility oscillator'], 'name': 'Lentz_Volatility', 'source': 'MQL5 Indicators/Lentz_Volatility/Lentz_Volatility.mq5', 'folder': 'Lentz_Volatility', 'inputs': [{'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 20, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 20, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodATR = _input('InpPeriodATR', 20)  # ATR period
InpPeriodMA = _input('InpPeriodMA', 20)  # Smoothing period
InpMethod = _input('InpMethod', MODE_EMA)  # Smoothing method
BufferLVOL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferAvgATR = Arr(0, 0.0)
period_atr = 0
period_ma = 0
weight_sum = 0
handle_atr = 0

def OnInit():
    global handle_atr, period_atr, period_ma
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    SetIndexBuffer(0, BufferLVOL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAvgATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Lentz Volatility (' + _str(period_atr) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLVOL, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferAvgATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_ma, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferLVOL, EMPTY_VALUE)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferAvgATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_atr, period_ma, BufferATR, BufferAvgATR) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_atr, period_ma, BufferATR, BufferAvgATR) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_atr, period_ma, BufferATR, BufferAvgATR, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_atr, period_ma, BufferATR, BufferAvgATR) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferLVOL[i] = _fdiv(BufferAvgATR[i] - BufferATR[i], Point())
        BufferColors[i] = (0 if (BufferAvgATR[i] > BufferATR[i]) else 1 if (BufferAvgATR[i] < BufferATR[i]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LentzVolatility(_MQL5Indicator):
    name = 'Lentz_Volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodATR': 20,  # ATR period
        'InpPeriodMA': 20,  # Smoothing period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing method
    }

