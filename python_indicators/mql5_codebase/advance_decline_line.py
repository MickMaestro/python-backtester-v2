"""Advance_Decline_Line — converted from MQL5: MQL5 Indicators/Advance_Decline_Line/Advance_Decline_Line.mq5

Advance Decline Line
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ADL'}, 'levels': [], 'description': ['Advance Decline Line'], 'name': 'Advance_Decline_Line', 'source': 'MQL5 Indicators/Advance_Decline_Line/Advance_Decline_Line.mq5', 'folder': 'Advance_Decline_Line', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpCumulative', 'py': 'InpCumulative', 'param': 'InpCumulative', 'type': 'int', 'default': 1, 'label': 'Cumulative', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpCumulative = _input('InpCumulative', INPUT_YES)  # Cumulative
BufferADL = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferADL, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADL(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferADL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferADL, 0)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferADL[i] = 0.0
        else:
            rs = 0
            fs = 0
            for j in range(0, period):
                if close[i + j] > open[i + j]:
                    rs += 1
                elif close[i + j] < open[i + j]:
                    fs += 1
                BufferADL[i] = ((rs - fs + BufferADL[i + 1]) if InpCumulative else (rs - fs))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvanceDeclineLine(_MQL5Indicator):
    name = 'Advance_Decline_Line'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpCumulative': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Cumulative
    }

