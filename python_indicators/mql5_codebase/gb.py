"""GB — converted from MQL5: MQL5 Indicators/GB/GB.mq5

Gaussian Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 7, 7: 7}, 'colors': {1: [16711680], 2: [12695295], 3: [12695295], 4: [9498256], 5: [9498256], 6: [14481663, 14481663], 7: [13499135, 13499135]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Center line', 2: 'Top', 3: 'Upper Top', 4: 'Bottom', 5: 'Lower Bottom', 6: 'Cloud Upper', 7: 'Cloud Lower'}, 'levels': [], 'description': ['Gaussian Bands indicator'], 'name': 'GB', 'source': 'MQL5 Indicators/GB/GB.mq5', 'folder': 'GB', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 12, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'uint', 'default': 12, 'label': 'Deviation period', 'sinput': False}, {'mql': 'InpMultiplier1', 'py': 'InpMultiplier1', 'param': 'InpMultiplier1', 'type': 'double', 'default': 2.0, 'label': 'First multiplier', 'sinput': False}, {'mql': 'InpMultiplier2', 'py': 'InpMultiplier2', 'param': 'InpMultiplier2', 'type': 'double', 'default': 4.0, 'label': 'Second multiplier', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 12)  # Period
InpDeviation = _input('InpDeviation', 12)  # Deviation period
InpMultiplier1 = _input('InpMultiplier1', 2.0)  # First multiplier
InpMultiplier2 = _input('InpMultiplier2', 4.0)  # Second multiplier
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferCentral = Arr(0, 0.0)
BufferTop1 = Arr(0, 0.0)
BufferTop2 = Arr(0, 0.0)
BufferBottom1 = Arr(0, 0.0)
BufferBottom2 = Arr(0, 0.0)
BufferCloudUpper1 = Arr(0, 0.0)
BufferCloudUpper2 = Arr(0, 0.0)
BufferCloudLower1 = Arr(0, 0.0)
BufferCloudLower2 = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferRAW1 = Arr(0, 0.0)
BufferRAW2 = Arr(0, 0.0)
period_ct = 0
period_dev = 0
handle_ma = 0
ac = 0.0
ad = 0.0

def OnInit():
    global ac, ad, handle_ma, period_ct, period_dev
    period_ct = (2 if (InpPeriod < 2) else InpPeriod)
    period_dev = (1 if (InpDeviation < 1) else InpDeviation)
    ac = Alpha(period_ct)
    ad = Alpha(period_dev)
    SetIndexBuffer(0, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTop2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom1, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBottom2, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCloudUpper1, INDICATOR_DATA)
    SetIndexBuffer(6, BufferCloudUpper2, INDICATOR_DATA)
    SetIndexBuffer(7, BufferCloudLower1, INDICATOR_DATA)
    SetIndexBuffer(8, BufferCloudLower2, INDICATOR_DATA)
    SetIndexBuffer(9, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferRAW1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferRAW2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gaussian Bands (' + _str(period_ct) + ',' + _str(period_dev) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(5, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(6, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferTop1, True)
    ArraySetAsSeries(BufferTop2, True)
    ArraySetAsSeries(BufferBottom1, True)
    ArraySetAsSeries(BufferBottom2, True)
    ArraySetAsSeries(BufferCloudUpper1, True)
    ArraySetAsSeries(BufferCloudUpper2, True)
    ArraySetAsSeries(BufferCloudLower1, True)
    ArraySetAsSeries(BufferCloudLower2, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferRAW1, True)
    ArraySetAsSeries(BufferRAW2, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 5
        ArrayInitialize(BufferCentral, 0)
        ArrayInitialize(BufferTop1, EMPTY_VALUE)
        ArrayInitialize(BufferTop2, EMPTY_VALUE)
        ArrayInitialize(BufferBottom1, EMPTY_VALUE)
        ArrayInitialize(BufferBottom2, EMPTY_VALUE)
        ArrayInitialize(BufferCloudUpper1, 0)
        ArrayInitialize(BufferCloudUpper2, 0)
        ArrayInitialize(BufferCloudLower1, 0)
        ArrayInitialize(BufferCloudLower2, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferRAW1, 0)
        ArrayInitialize(BufferRAW2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCentral[i] = Smooth(BufferMA, ac, i, BufferCentral)
        BufferRAW1[i] = fabs(BufferMA[i] - BufferCentral[i])
    for i in range(limit, 0 - 1, -1):
        BufferRAW2[i] = Smooth(BufferRAW1, ad, i, BufferRAW2)
        BufferTop1[i] = BufferCentral[i] + (BufferRAW2[i] * InpMultiplier1)
        BufferTop2[i] = BufferCentral[i] + (BufferRAW2[i] * InpMultiplier2)
        BufferBottom1[i] = BufferCentral[i] - (BufferRAW2[i] * InpMultiplier1)
        BufferBottom2[i] = BufferCentral[i] - (BufferRAW2[i] * InpMultiplier2)
        BufferCloudUpper1[i] = BufferTop2[i]
        BufferCloudUpper2[i] = BufferTop1[i]
        BufferCloudLower1[i] = BufferBottom1[i]
        BufferCloudLower2[i] = BufferBottom2[i]
    return rates_total

def Alpha(period):
    w = _fdiv(2.0 * M_PI, period)
    b = _fdiv(1.0 - cos(w), pow(1.414, 2.0 / 3.0) - 1.0)
    return (-b) + sqrt((b * b) + (2.0 * b))

def Smooth(src, alpha, index, res):
    return (pow(alpha, 4.0) * src[index]) + (4.0 * (1.0 - alpha) * res[index + 1]) - (6.0 * pow(1.0 - alpha, 2.0) * res[index + 2]) + (4.0 * pow(1.0 - alpha, 3.0) * res[index + 3]) - (pow(1.0 - alpha, 4.0) * res[index + 4])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GB(_MQL5Indicator):
    name = 'GB'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 12,  # Period
        'InpDeviation': 12,  # Deviation period
        'InpMultiplier1': 2.0,  # First multiplier
        'InpMultiplier2': 4.0,  # Second multiplier
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

