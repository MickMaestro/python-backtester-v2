"""InvestorsVsSpeculatorsDelta — converted from MQL5: MQL5 Indicators/InvestorsVsSpeculatorsDelta/InvestorsVsSpeculatorsDelta.mq5

Investors vs Speculators Delta indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'InvVsSpec Delta'}, 'levels': [], 'description': ['Investors vs Speculators Delta indicator'], 'name': 'InvestorsVsSpeculatorsDelta', 'source': 'MQL5 Indicators/InvestorsVsSpeculatorsDelta/InvestorsVsSpeculatorsDelta.mq5', 'folder': 'InvestorsVsSpeculatorsDelta', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'AD method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_MODE
MODE_CS = 0
MODE_TS = 1
_enum('ENUM_CALC_MODE', {0: 'MODE_CS', 1: 'MODE_TS'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_CS)  # AD method
BufferDelta = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSpeculators = Arr(0, 0.0)
BufferInvestors = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
period_ind = 0

def OnInit():
    global period_ind
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferDelta, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSpeculators, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferInvestors, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAVG, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Investors Vs Speculators Delta (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDelta, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSpeculators, True)
    ArraySetAsSeries(BufferInvestors, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferAVG, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ind, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 2
        ArrayInitialize(BufferDelta, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferSpeculators, 0)
        ArrayInitialize(BufferInvestors, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferAVG, 0)
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        for j in range(1, period_ind + 1):
            sum_ += float(tick_volume[i + j])
        BufferAVG[i] = _fdiv(sum_, period_ind)
        AD = (0 if ((high[i] - low[i]) == 0) else (_fdiv(close[i] - low[i] - (high[i] - close[i]), high[i] - low[i]) * tick_volume[i]) if (InpMethod == MODE_CS) else (_fdiv(close[i] - open[i], high[i] - low[i]) * tick_volume[i]))
        if tick_volume[i] > BufferAVG[i]:
            BufferSpeculators[i] = BufferSpeculators[i + 1]
            BufferInvestors[i] = BufferInvestors[i + 1] + AD
        else:
            BufferInvestors[i] = BufferInvestors[i + 1]
            BufferSpeculators[i] = BufferSpeculators[i + 1] + AD
        BufferDelta[i] = BufferInvestors[i] - BufferSpeculators[i]
        BufferColors[i] = (0 if (BufferDelta[i] > 0) else 1 if (BufferDelta[i] < 0) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InvestorsVsSpeculatorsDelta(_MQL5Indicator):
    name = 'InvestorsVsSpeculatorsDelta'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Classical MT', 1: 'Trade Station'}, default=0),  # AD method
    }

