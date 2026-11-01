"""Ehlers_CG — converted from MQL5: MQL5 Indicators/Ehlers_CG/Ehlers_CG.mq5

Ehlers Center of Gravity indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'CoG Main', 2: 'CoG Signal'}, 'levels': [], 'description': ['Ehlers Center of Gravity indicator'], 'name': 'Ehlers_CG', 'source': 'MQL5 Indicators/Ehlers_CG/Ehlers_CG.mq5', 'folder': 'Ehlers_CG', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
BufferCG0 = Arr(0, 0.0)
BufferCG1 = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferCG0, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCG1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Ehler's Center of Gravity (" + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCG0, True)
    ArraySetAsSeries(BufferCG1, True)
    ArraySetAsSeries(BufferPrice, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferCG0, EMPTY_VALUE)
        ArrayInitialize(BufferCG1, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
    num = 0.0
    demon = 0.0
    for i in range(limit, 0 - 1, -1):
        demon = 0.0
        num = demon
        BufferPrice[i] = (high[i] + low[i]) / 2.0
        for j in range(0, period - 1):
            num += (j + 1) * BufferPrice[i + j]
            demon += BufferPrice[i + j]
        BufferCG0[i] = _fdiv(-num, demon) + ((period + 1) / 2.0)
        BufferCG1[i] = BufferCG0[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersCG(_MQL5Indicator):
    name = 'Ehlers_CG'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
    }

