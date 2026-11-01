"""ama — converted from MQL5: MQL5 Indicators/Adaptive Moving Average (AMA)/ama.mq5

Adaptive Moving Average
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'AMA'}, 'levels': [], 'description': ['Adaptive Moving Average'], 'name': 'ama', 'source': 'MQL5 Indicators/Adaptive Moving Average (AMA)/ama.mq5', 'folder': 'Adaptive Moving Average (AMA)', 'inputs': [{'mql': 'InpPeriodAMA', 'py': 'InpPeriodAMA', 'param': 'InpPeriodAMA', 'type': 'int', 'default': 10, 'label': 'AMA period', 'sinput': False}, {'mql': 'InpFastPeriodEMA', 'py': 'InpFastPeriodEMA', 'param': 'InpFastPeriodEMA', 'type': 'int', 'default': 2, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowPeriodEMA', 'py': 'InpSlowPeriodEMA', 'param': 'InpSlowPeriodEMA', 'type': 'int', 'default': 30, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpShiftAMA', 'py': 'InpShiftAMA', 'param': 'InpShiftAMA', 'type': 'int', 'default': 0, 'label': 'AMA shift', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodAMA = _input('InpPeriodAMA', 10)  # AMA period
InpFastPeriodEMA = _input('InpFastPeriodEMA', 2)  # Fast EMA period
InpSlowPeriodEMA = _input('InpSlowPeriodEMA', 30)  # Slow EMA period
InpShiftAMA = _input('InpShiftAMA', 0)  # AMA shift
ExtAMABuffer = Arr(0, 0.0)
ExtFastSC = 0.0
ExtSlowSC = 0.0
ExtPeriodAMA = 0
ExtSlowPeriodEMA = 0
ExtFastPeriodEMA = 0

def OnInit():
    global ExtFastPeriodEMA, ExtFastSC, ExtPeriodAMA, ExtSlowPeriodEMA, ExtSlowSC
    if InpPeriodAMA <= 0:
        ExtPeriodAMA = 10
        printf('Input parameter InpPeriodAMA has incorrect value (%d). Indicator will use value %d for calculations.', InpPeriodAMA, ExtPeriodAMA)
    else:
        ExtPeriodAMA = InpPeriodAMA
    if InpSlowPeriodEMA <= 0:
        ExtSlowPeriodEMA = 30
        printf('Input parameter InpSlowPeriodEMA has incorrect value (%d). Indicator will use value %d for calculations.', InpSlowPeriodEMA, ExtSlowPeriodEMA)
    else:
        ExtSlowPeriodEMA = InpSlowPeriodEMA
    if InpFastPeriodEMA <= 0:
        ExtFastPeriodEMA = 2
        printf('Input parameter InpFastPeriodEMA has incorrect value (%d). Indicator will use value %d for calculations.', InpFastPeriodEMA, ExtFastPeriodEMA)
    else:
        ExtFastPeriodEMA = InpFastPeriodEMA
    SetIndexBuffer(0, ExtAMABuffer, INDICATOR_DATA)
    short_name = 'AMA(' + IntegerToString(ExtPeriodAMA) + ',' + IntegerToString(ExtFastPeriodEMA) + ',' + IntegerToString(ExtSlowPeriodEMA) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodAMA)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShiftAMA)
    ExtFastSC = _fdiv(2.0, ExtFastPeriodEMA + 1.0)
    ExtSlowSC = _fdiv(2.0, ExtSlowPeriodEMA + 1.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    if rates_total < (ExtPeriodAMA + begin):
        return 0
    if begin != 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodAMA + begin)
    pos = prev_calculated - 1
    if pos < (ExtPeriodAMA + begin):
        pos = ExtPeriodAMA + begin
        i = 0
        for i in range(i, pos - 1):
            ExtAMABuffer[i] = 0.0
        else:
            i = _range_end(i, pos - 1, 1)
        ExtAMABuffer[pos - 1] = price[pos - 1]
    i = pos
    for i in range(i, rates_total):
        dCurrentSSC = (CalculateER(i, price) * (ExtFastSC - ExtSlowSC)) + ExtSlowSC
        dPrevAMA = ExtAMABuffer[i - 1]
        ExtAMABuffer[i] = (pow(dCurrentSSC, 2) * (price[i] - dPrevAMA)) + dPrevAMA
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def CalculateER(nPosition, PriceData):
    dSignal = fabs(PriceData[nPosition] - PriceData[nPosition - ExtPeriodAMA])
    dNoise = 0.0
    for delta in range(0, ExtPeriodAMA):
        dNoise += fabs(PriceData[nPosition - delta] - PriceData[nPosition - delta - 1])
    if dNoise != 0.0:
        return _fdiv(dSignal, dNoise)
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ama(_MQL5Indicator):
    name = 'ama'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodAMA': 10,  # AMA period
        'InpFastPeriodEMA': 2,  # Fast EMA period
        'InpSlowPeriodEMA': 30,  # Slow EMA period
        'InpShiftAMA': 0,  # AMA shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

