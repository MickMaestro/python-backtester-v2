"""VPCI — converted from MQL5: MQL5 Indicators/VPCI/VPCI.mq5

Volume price confirmation indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VPCI'}, 'levels': [], 'description': ['Volume price confirmation indicator'], 'name': 'VPCI', 'source': 'MQL5 Indicators/VPCI/VPCI.mq5', 'folder': 'VPCI', 'inputs': [{'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 50, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 10, 'label': 'Fast MA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodSlow = _input('InpPeriodSlow', 50)  # Slow MA period
InpPeriodFast = _input('InpPeriodFast', 10)  # Fast MA period
BufferVPCI = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferCV = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_max = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, period_fast, period_max, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_max = fmax(period_fast, period_slow)
    SetIndexBuffer(0, BufferVPCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferCV, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VPCI (' + _str(period_slow) + ',' + _str(period_fast) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVPCI, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferCV, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, MODE_SMA, PRICE_CLOSE)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, MODE_SMA, PRICE_CLOSE)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_max, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferVPCI, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferCV, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
        BufferCV[i] = close[i] * BufferVol[i]
    for i in range(limit, 0 - 1, -1):
        Volume_Slow = GetSMA(rates_total, i, period_slow, BufferVol) * period_slow
        Volume_Fast = GetSMA(rates_total, i, period_fast, BufferVol) * period_fast
        VWMA_Slow = (_fdiv(GetSMA(rates_total, i, period_slow, BufferCV) * period_slow, Volume_Slow) if (Volume_Slow != 0) else 0)
        VWMA_Fast = (_fdiv(GetSMA(rates_total, i, period_fast, BufferCV) * period_fast, Volume_Fast) if (Volume_Fast != 0) else 0)
        SMA_Fast = BufferFMA[i]
        VPC = VWMA_Slow - BufferSMA[i]
        VPR = (_fdiv(VWMA_Fast, SMA_Fast) if (SMA_Fast != 0) else 1)
        VM = (_fdiv(Volume_Fast * period_slow, Volume_Slow * period_fast) if (Volume_Slow != 0) else 1)
        BufferVPCI[i] = _fdiv(VPC * VPR * VM, Point() * Point())
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


class VPCI(_MQL5Indicator):
    name = 'VPCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSlow': 50,  # Slow MA period
        'InpPeriodFast': 10,  # Fast MA period
    }

