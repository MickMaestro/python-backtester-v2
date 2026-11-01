"""Trend_Score — converted from MQL5: MQL5 Indicators/Trend_Score/Trend_Score.mq5

Trend score oscillator by Tushar S.Chande
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TrendScore'}, 'levels': [], 'description': ['Trend score oscillator by Tushar S.Chande'], 'name': 'Trend_Score', 'source': 'MQL5 Indicators/Trend_Score/Trend_Score.mq5', 'folder': 'Trend_Score', 'inputs': [{'mql': 'InpMethodPrice', 'py': 'InpMethodPrice', 'param': 'InpMethodPrice', 'type': 'int', 'default': 0, 'label': 'Price method', 'sinput': False}, {'mql': 'InpMethodPeriod', 'py': 'InpMethodPeriod', 'param': 'InpMethodPeriod', 'type': 'int', 'default': 0, 'label': 'Period method', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'int', 'default': 5, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'int', 'default': -5, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_PRICE
PRICE_OPEN_CLOSE = 0
PRICE_CLOSE_CLOSE = 1
_enum('ENUM_METHOD_PRICE', {0: 'PRICE_OPEN_CLOSE', 1: 'PRICE_CLOSE_CLOSE'})

# enum ENUM_METHOD_PERIOD
PERIOD_USE_ON = 0
PERIOD_USE_OFF = 1
_enum('ENUM_METHOD_PERIOD', {0: 'PERIOD_USE_ON', 1: 'PERIOD_USE_OFF'})

# ---- inputs and global variables
InpMethodPrice = _input('InpMethodPrice', PRICE_OPEN_CLOSE)  # Price method
InpMethodPeriod = _input('InpMethodPeriod', PERIOD_USE_ON)  # Period method
InpPeriod = _input('InpPeriod', 10)  # Period
InpOverbought = _input('InpOverbought', 5)  # Overbought
InpOversold = _input('InpOversold', -5)  # Oversold
BufferTrendScore = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0

def OnInit():
    global overbought, oversold, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = (0 if (fabs(InpOverbought) < 0) else fabs(InpOverbought))
    oversold = (0 if ((-fabs(InpOversold)) > 0) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferTrendScore, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend score (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferTrendScore, True)
    ArraySetAsSeries(BufferRAW, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    max_ = (period if (InpMethodPeriod == PERIOD_USE_ON) else 4)
    if rates_total < fmax(max_, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTrendScore, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
    PrevPrice = 0.0
    for i in range(limit, 0 - 1, -1):
        if InpMethodPeriod == PERIOD_USE_ON:
            PrevPrice = (open[i] if (InpMethodPrice == PRICE_OPEN_CLOSE) else close[i + 1])
            BufferRAW[i] = (1 if (close[i] > PrevPrice) else -1 if (close[i] < PrevPrice) else 0)
            sum_ = 0.0
            if i < (rates_total - period):
                sum_ = 0.0
                for j in range(0, period):
                    sum_ = sum_ + BufferRAW[i + j]
            BufferTrendScore[i] = sum_
        else:
            PrevPrice = (open[i] if (InpMethodPrice == PRICE_OPEN_CLOSE) else close[i + 1])
            if close[i] > PrevPrice:
                BufferTrendScore[i] = ((BufferTrendScore[i + 1] + 1) if (BufferTrendScore[i + 1] >= 0) else 1)
            elif close[i] < PrevPrice:
                BufferTrendScore[i] = ((BufferTrendScore[i + 1] - 1) if (BufferTrendScore[i + 1] < 0) else -1)
            else:
                BufferTrendScore[i] = BufferTrendScore[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendScore(_MQL5Indicator):
    name = 'Trend_Score'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethodPrice': _Choice({0: 'Open/Close', 1: 'Close/Close'}, default=0),  # Price method
        'InpMethodPeriod': _Choice({0: 'Use period', 1: 'Do not use period'}, default=0),  # Period method
        'InpPeriod': 10,  # Period
        'InpOverbought': 5,  # Overbought
        'InpOversold': -5,  # Oversold
    }

