"""Modified_Advance_Decline_Line — converted from MQL5: MQL5 Indicators/Modified_Advance_Decline_Line/Modified_Advance_Decline_Line.mq5

Modified Advance Decline Line indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MADL'}, 'levels': [], 'description': ['Modified Advance Decline Line indicator'], 'name': 'Modified_Advance_Decline_Line', 'source': 'MQL5 Indicators/Modified_Advance_Decline_Line/Modified_Advance_Decline_Line.mq5', 'folder': 'Modified_Advance_Decline_Line', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferMAD = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
period_ma = 0

def OnInit():
    global period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferMAD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferVol, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MADL (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMAD, True)
    ArraySetAsSeries(BufferVol, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMAD, 0)
        ArrayInitialize(BufferVol, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
    for i in range(limit, 0 - 1, -1):
        MA = GetSMA(rates_total, i, period_ma, BufferVol)
        BufferMAD[i] = (BufferMAD[i + 1] if ((high[i] - low[i]) == 0) else (BufferMAD[i + 1] + (_fdiv((2.0 * close[i]) - high[i] - low[i], high[i] - low[i]) * (BufferVol[i] + MA))))
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


class ModifiedAdvanceDeclineLine(_MQL5Indicator):
    name = 'Modified_Advance_Decline_Line'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

