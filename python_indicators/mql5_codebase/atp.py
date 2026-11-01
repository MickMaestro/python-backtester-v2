"""ATP — converted from MQL5: MQL5 Indicators/Asymmetric Trend Pressure/ATP.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [3329330], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ATP', 2: 'Up', 3: 'Down'}, 'levels': [], 'description': [], 'name': 'ATP', 'source': 'MQL5 Indicators/Asymmetric Trend Pressure/ATP.mq5', 'folder': 'Asymmetric Trend Pressure', 'inputs': [{'mql': 'InpPeriodUP', 'py': 'InpPeriodUP', 'param': 'InpPeriodUP', 'type': 'uint', 'default': 14, 'label': 'Period Up', 'sinput': False}, {'mql': 'InpPeriodDN', 'py': 'InpPeriodDN', 'param': 'InpPeriodDN', 'type': 'uint', 'default': 10, 'label': 'Period Down', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 24, 'label': 'Period', 'sinput': False}, {'mql': 'InpShowUpDn', 'py': 'InpShowUpDn', 'param': 'InpShowUpDn', 'type': 'int', 'default': 0, 'label': 'Show lines Up and Down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodUP = _input('InpPeriodUP', 14)  # Period Up
InpPeriodDN = _input('InpPeriodDN', 10)  # Period Down
InpPeriod = _input('InpPeriod', 24)  # Period
InpShowUpDn = _input('InpShowUpDn', INPUT_NO)  # Show lines Up and Down
BufferATP = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
period_up = 0
period_dn = 0
period = 0

def OnInit():
    global period, period_dn, period_up
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_up = (1 if (InpPeriodUP < 1) else InpPeriodUP)
    period_dn = (1 if (InpPeriodDN < 1) else InpPeriodDN)
    SetIndexBuffer(0, BufferATP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDN, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Asymmetric Trend Pressure(' + _str(period) + ')')
    ArraySetAsSeries(BufferATP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferUP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferATP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferUP, EMPTY_VALUE)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0 - 1, -1):
        summ_up = 0.0
        summ_dn = 0.0
        n = 0
        count_up = 0
        count_dn = 0
        while n < period:
            if close[i + n] > open[i + n] and count_up < period_up:
                count_up += 1
                summ_up += close[i + n] - open[i + n]
            elif close[i + n] < open[i + n] and count_dn < period_dn:
                count_dn += 1
                summ_dn += open[i + n] - close[i + n]
            n += 1
        if InpShowUpDn:
            BufferUP[i] = _fdiv(summ_up, period_up)
            BufferDN[i] = _fdiv(summ_dn, period_dn)
        else:
            BufferDN[i] = EMPTY_VALUE
            BufferUP[i] = BufferDN[i]
        BufferATP[i] = _fdiv(summ_up, period_up) - _fdiv(summ_dn, period_dn)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATP(_MQL5Indicator):
    name = 'ATP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodUP': 14,  # Period Up
        'InpPeriodDN': 10,  # Period Down
        'InpPeriod': 24,  # Period
        'InpShowUpDn': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show lines Up and Down
    }

