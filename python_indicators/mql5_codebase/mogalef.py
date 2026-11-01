"""Mogalef — converted from MQL5: MQL5 Indicators/Mogalef/Mogalef.mq5

Mogalef Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Top', 2: 'Central', 3: 'Bottom'}, 'levels': [], 'description': ['Mogalef Bands indicator'], 'name': 'Mogalef', 'source': 'MQL5 Indicators/Mogalef/Mogalef.mq5', 'folder': 'Mogalef', 'inputs': [{'mql': 'InpPeriodLG', 'py': 'InpPeriodLG', 'param': 'InpPeriodLG', 'type': 'uint', 'default': 3, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'InpPeriodDev', 'py': 'InpPeriodDev', 'param': 'InpPeriodDev', 'type': 'uint', 'default': 7, 'label': 'Standard deviation period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodLG = _input('InpPeriodLG', 3)  # Linear regression period
InpPeriodDev = _input('InpPeriodDev', 7)  # Standard deviation period
InpMultiplier = _input('InpMultiplier', 2.0)  # Multiplier
BufferTop = Arr(0, 0.0)
BufferCentral = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
multiplier = 0.0
period_lg = 0
period_dv = 0
period_max = 0
handle_dev = 0

def OnInit():
    global handle_dev, multiplier, period_dv, period_lg, period_max
    period_lg = (2 if (InpPeriodLG < 2) else InpPeriodLG)
    period_dv = (1 if (InpPeriodDev < 1) else InpPeriodDev)
    period_max = fmax(period_dv, period_lg)
    multiplier = InpMultiplier
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDev, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mogalef Bands (' + _str(period_lg) + ',' + _str(period_dv) + ',' + DoubleToString(multiplier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max + period_lg + 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_max + period_lg + 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, period_max + period_lg + 1)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_dv, 0, MODE_SMA, PRICE_CLOSE)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_dv), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferTop, 0)
        ArrayInitialize(BufferCentral, 0)
        ArrayInitialize(BufferBottom, 0)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferDev, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferPrice[i] = ((2.0 * close[i]) + open[i] + low[i] + high[i]) / 5.0
        x = 0.0
        y = 0.0
        xy = 0.0
        x2 = 0.0
        for j in range(0, period_lg):
            y += BufferPrice[i + j]
            xy += BufferPrice[i + j] * j
            x += j
            x2 += j * j
        temp = (period_lg * x2) - (x * x)
        m = _fdiv((period_lg * xy) - (x * y), temp)
        yint = _fdiv(y + (m * x), period_lg)
        BufferCentral[i] = yint - (m * period_lg)
        BufferTop[i] = BufferCentral[i] + (multiplier * BufferDev[i])
        BufferBottom[i] = BufferCentral[i] - (multiplier * BufferDev[i])
        if BufferCentral[i] < BufferTop[i + 1] and BufferCentral[i] > BufferBottom[i + 1]:
            BufferTop[i] = BufferTop[i + 1]
            BufferCentral[i] = BufferCentral[i + 1]
            BufferBottom[i] = BufferBottom[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mogalef(_MQL5Indicator):
    name = 'Mogalef'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodLG': 3,  # Linear regression period
        'InpPeriodDev': 7,  # Standard deviation period
        'InpMultiplier': 2.0,  # Multiplier
    }

