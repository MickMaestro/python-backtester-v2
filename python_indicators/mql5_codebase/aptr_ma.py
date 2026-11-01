"""APTR_MA — converted from MQL5: MQL5 Indicators/APTR_MA/APTR_MA.mq5

Average Percentage True Range indicator with MA adjustments
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'APTR MA'}, 'levels': [], 'description': ['Average Percentage True Range indicator with MA adjustments'], 'name': 'APTR_MA', 'source': 'MQL5 Indicators/APTR_MA/APTR_MA.mq5', 'folder': 'APTR_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
BufferAPTR = Arr(0, 0.0)
BufferPTR = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
weight_sum = 0

def OnInit():
    global period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferAPTR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    name = 'APTR ' + MethodToString(InpMethod) + ' (' + _str(period_ma) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, name)
    ArraySetAsSeries(BufferAPTR, True)
    ArraySetAsSeries(BufferPTR, True)
    ArraySetAsSeries(BufferMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferAPTR, EMPTY_VALUE)
        ArrayInitialize(BufferPTR, 0)
        ArrayInitialize(BufferMA, 0)
    for i in range(limit, 0 - 1, -1):
        s1 = (_fdiv(2.0 * (high[i] - low[i]), high[i] + low[i]) if ((high[i] + low[i]) != 0) else 0)
        s2 = (_fdiv(2.0 * (high[i] - close[i + 1]), high[i] + close[i + 1]) if ((high[i] + close[i + 1]) != 0) else 0)
        s3 = (_fdiv(2.0 * (low[i] - close[i + 1]), (3.0 * low[i]) - close[i + 1]) if ((low[i] - close[i + 1]) != 0) else 0)
        BufferPTR[i] = fmax(s1, fmax(s2, s3))
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferPTR, BufferMA) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferPTR, BufferMA) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ma, BufferPTR, BufferMA, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferPTR, BufferMA) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferAPTR[i] = 100.0 * BufferMA[i]
    return rates_total

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class APTRMA(_MQL5Indicator):
    name = 'APTR_MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
    }

