"""Twiggs_Money_Flow — converted from MQL5: MQL5 Indicators/Twiggs_Money_Flow/Twiggs_Money_Flow.mq5

Twiggs Money Flow oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TMF'}, 'levels': [], 'description': ['Twiggs Money Flow oscillator'], 'name': 'Twiggs_Money_Flow', 'source': 'MQL5 Indicators/Twiggs_Money_Flow/Twiggs_Money_Flow.mq5', 'folder': 'Twiggs_Money_Flow', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 21, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 21)  # Period
BufferTMF = Arr(0, 0.0)
BufferADV = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferWMA_ADV = Arr(0, 0.0)
BufferWMA_V = Arr(0, 0.0)
period_tmf = 0
k = 0.0

def OnInit():
    global k, period_tmf
    period_tmf = (1 if (InpPeriod < 1) else InpPeriod)
    k = _fdiv(1.0, period_tmf)
    SetIndexBuffer(0, BufferTMF, INDICATOR_DATA)
    SetIndexBuffer(1, BufferADV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferWMA_ADV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferWMA_V, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Twiggs Money Flow (' + _str(period_tmf) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_tmf)
    ArraySetAsSeries(BufferTMF, True)
    ArraySetAsSeries(BufferADV, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferWMA_ADV, True)
    ArraySetAsSeries(BufferWMA_V, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_tmf, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTMF, EMPTY_VALUE)
        ArrayInitialize(BufferADV, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferWMA_ADV, 0)
        ArrayInitialize(BufferWMA_V, 0)
    for i in range(limit, 0 - 1, -1):
        TRH = fmax(high[i], close[i + 1])
        TRL = fmin(low[i], close[i + 1])
        TR = TRH - TRL
        BufferADV[i] = (_fdiv(tick_volume[i] * ((2.0 * close[i]) - TRL - TRH), TR) if (TR != 0) else 0)
        BufferVol[i] = float(tick_volume[i])
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferWMA_ADV[i] = GetSMA(rates_total, i, period_tmf, BufferADV)
            BufferWMA_V[i] = GetSMA(rates_total, i, period_tmf, BufferVol)
        else:
            BufferWMA_ADV[i] = ((BufferADV[i] - BufferWMA_ADV[i + 1]) * k) + BufferWMA_ADV[i + 1]
            BufferWMA_V[i] = ((BufferVol[i] - BufferWMA_V[i + 1]) * k) + BufferWMA_V[i + 1]
        BufferTMF[i] = (_fdiv(BufferWMA_ADV[i], BufferWMA_V[i] * Point()) if (BufferWMA_V[i] != 0) else 0)
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


class TwiggsMoneyFlow(_MQL5Indicator):
    name = 'Twiggs_Money_Flow'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 21,  # Period
    }

