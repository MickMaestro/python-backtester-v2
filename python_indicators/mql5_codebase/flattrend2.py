"""flattrend2 — converted from MQL5: MQL5 Indicators/FlatTrend2/flattrend2.mq5

Copyright: Copyright © 2007, Kirk Sloan; Link: http://www.metaquotes.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Kirk Sloan', 'link': 'http://www.metaquotes.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [8421504, 255, 2763429, 32768, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'FlatTrend'}, 'levels': [], 'description': [], 'name': 'flattrend2', 'source': 'MQL5 Indicators/FlatTrend2/flattrend2.mq5', 'folder': 'FlatTrend2', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 14, 'label': 'ADX period', 'sinput': False}, {'mql': 'SarStep', 'py': 'SarStep', 'param': 'SarStep', 'type': 'double', 'default': 0.02, 'label': 'Parabolic step', 'sinput': False}, {'mql': 'SarMaximum', 'py': 'SarMaximum', 'param': 'SarMaximum', 'type': 'double', 'default': 0.2, 'label': 'Parabolic maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 14)  # ADX period
SarStep = _input('SarStep', 0.02)  # Parabolic step
SarMaximum = _input('SarMaximum', 0.2)  # Parabolic maximum
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
SAR_Handle = 0
ADX_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, SAR_Handle, min_rates_total
    min_rates_total = _int(ADXPeriod)
    SAR_Handle = iSAR(None, PERIOD_CURRENT, SarStep, SarMaximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iSAR indicator')
    ADX_Handle = iADX(None, PERIOD_CURRENT, ADXPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iADX indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'FlatTrend2( ', ADXPeriod, ', ', SarStep, SarMaximum, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(SAR_Handle) < rates_total or BarsCalculated(ADX_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    SAR = Arr(0, 0.0)
    ADXP = Arr(0, 0.0)
    ADXM = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total + 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(SAR_Handle, 0, 0, to_copy, SAR) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, ADXP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, ADXM) <= 0:
        return 0
    ArraySetAsSeries(SAR, True)
    ArraySetAsSeries(ADXP, True)
    ArraySetAsSeries(ADXM, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 1.0
        ColorBuffer[bar] = 0.0
        if SAR[bar] < close[bar] and ADXP[bar] > ADXM[bar]:
            ColorBuffer[bar] = 3.0
        if SAR[bar] < close[bar] and ADXM[bar] > ADXP[bar]:
            ColorBuffer[bar] = 4.0
        if SAR[bar] > close[bar] and ADXM[bar] > ADXP[bar]:
            ColorBuffer[bar] = 2.0
        if SAR[bar] > close[bar] and ADXP[bar] > ADXM[bar]:
            ColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Flattrend2(_MQL5Indicator):
    name = 'flattrend2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 14,  # ADX period
        'SarStep': 0.02,  # Parabolic step
        'SarMaximum': 0.2,  # Parabolic maximum
    }
    y_range = (0.0, 1.0)

