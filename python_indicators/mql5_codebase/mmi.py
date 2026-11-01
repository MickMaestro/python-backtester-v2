"""MMI — converted from MQL5: MQL5 Indicators/MMI/MMI.mq5

Market Meanness Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MMI'}, 'levels': [], 'description': ['Market Meanness Index indicator'], 'name': 'MMI', 'source': 'MQL5 Indicators/MMI/MMI.mq5', 'folder': 'MMI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 200, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 76.0, 'label': 'Random boundings', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 74.0, 'label': 'Trend', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 200)  # Period
InpOverbought = _input('InpOverbought', 76.0)  # Random boundings
InpOversold = _input('InpOversold', 74.0)  # Trend
BufferMMI = Arr(0, 0.0)
period = 0
overbought = 0.0
oversold = 0.0

def OnInit():
    global overbought, oversold, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferMMI, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Market Meanness Index (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Random')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Trend')
    ArraySetAsSeries(BufferMMI, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferMMI, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        nl = 0
        nh = 0
        mean = Mean(i, open, close)
        for j in range(i + 1, i + period + 1):
            if open[j] > close[j]:
                if (open[j] - close[j]) > mean and (open[j] - close[j]) > (open[j - 1] - close[j - 1]):
                    nl += 1
            else:
                if (close[j] - open[j]) < mean and (close[j] - open[j]) < (close[j - 1] - open[j - 1]):
                    nh += 1
        BufferMMI[i] = 100.0 - _fdiv(100.0 * (nl + nh), period - 1)
    return rates_total

def Mean(shift, open, close):
    sum_ = 0.0
    for i in range(shift, shift + period):
        sum_ += fabs(open[i] - close[i])
    return _fdiv(sum_, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MMI(_MQL5Indicator):
    name = 'MMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 200,  # Period
        'InpOverbought': 76.0,  # Random boundings
        'InpOversold': 74.0,  # Trend
    }

