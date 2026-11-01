"""PVA — converted from MQL5: MQL5 Indicators/PVA/PVA.mq5

SonicR PVA Volumes indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [12632256, 9498256, 9639167, 32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'PVA'}, 'levels': [], 'description': ['SonicR PVA Volumes indicator'], 'name': 'PVA', 'source': 'MQL5 Indicators/PVA/PVA.mq5', 'folder': 'PVA', 'inputs': [{'mql': 'InpPeriodClimax', 'py': 'InpPeriodClimax', 'param': 'InpPeriodClimax', 'type': 'uint', 'default': 10, 'label': 'Climax period', 'sinput': False}, {'mql': 'InpPeriodRising', 'py': 'InpPeriodRising', 'param': 'InpPeriodRising', 'type': 'uint', 'default': 10, 'label': 'Rising period', 'sinput': False}, {'mql': 'InpFactorRising', 'py': 'InpFactorRising', 'param': 'InpFactorRising', 'type': 'double', 'default': 1.0, 'label': 'Rising factor', 'sinput': False}, {'mql': 'InpFactorExtreme', 'py': 'InpFactorExtreme', 'param': 'InpFactorExtreme', 'type': 'double', 'default': 2.0, 'label': 'Extreme factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodClimax = _input('InpPeriodClimax', 10)  # Climax period
InpPeriodRising = _input('InpPeriodRising', 10)  # Rising period
InpFactorRising = _input('InpFactorRising', 1.0)  # Rising factor
InpFactorExtreme = _input('InpFactorExtreme', 2.0)  # Extreme factor
BufferPVA = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferRange = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
factor_rs = 0.0
factor_ex = 0.0
period_cl = 0
period_rs = 0
period_max = 0

def OnInit():
    global factor_ex, factor_rs, period_cl, period_max, period_rs
    period_cl = (1 if (InpPeriodClimax < 1) else InpPeriodClimax)
    period_rs = (1 if (InpPeriodRising < 1) else InpPeriodRising)
    period_max = fmax(period_cl, period_rs)
    factor_rs = InpFactorRising
    factor_ex = InpFactorExtreme
    SetIndexBuffer(0, BufferPVA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferRange, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SonicR PVA Volumes (' + _str(period_cl) + ',' + _str(period_rs) + ',' + DoubleToString(factor_rs, 1) + ',' + DoubleToString(factor_ex, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPVA, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferRange, True)
    ArraySetAsSeries(BufferMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferPVA, EMPTY_VALUE)
        ArrayInitialize(BufferRange, 0)
        ArrayInitialize(BufferMA, 0)
    for i in range(limit, 0 - 1, -1):
        BufferPVA[i] = float(tick_volume[i])
        BufferRange[i] = (high[i] - low[i]) * tick_volume[i]
    for i in range(limit, 0 - 1, -1):
        MA = GetSMA(rates_total, i, period_rs, BufferPVA)
        bh = ArrayMaximum(BufferRange, i + 1, period_cl)
        if bh == WRONG_VALUE:
            continue
        Max = BufferRange[bh]
        BufferColors[i] = 0.0
        if BufferPVA[i] >= (MA * factor_rs):
            if close[i] > open[i]:
                BufferColors[i] = 1.0
            else:
                BufferColors[i] = 2.0
        if BufferRange[i] >= Max or tick_volume[i] >= (MA * factor_ex):
            if close[i] > open[i]:
                BufferColors[i] = 3.0
            else:
                BufferColors[i] = 4.0
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PVA(_MQL5Indicator):
    name = 'PVA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodClimax': 10,  # Climax period
        'InpPeriodRising': 10,  # Rising period
        'InpFactorRising': 1.0,  # Rising factor
        'InpFactorExtreme': 2.0,  # Extreme factor
    }

