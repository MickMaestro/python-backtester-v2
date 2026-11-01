"""KOT — converted from MQL5: MQL5 Indicators/Keep On Trading (KOT)/KOT.mq5

Indicator Keep On Trading
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'KOT'}, 'levels': [], 'description': ['Indicator Keep On Trading'], 'name': 'KOT', 'source': 'MQL5 Indicators/Keep On Trading (KOT)/KOT.mq5', 'folder': 'Keep On Trading (KOT)', 'inputs': [{'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 10, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 3, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 3, 'label': 'MA method', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 0.1, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodATR = _input('InpPeriodATR', 10)  # ATR period
InpPeriodMA = _input('InpPeriodMA', 3)  # MA period
InpMethod = _input('InpMethod', MODE_LWMA)  # MA method
InpMultiplier = _input('InpMultiplier', 0.1)  # Multiplier
BufferKOT = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
period_ma = 0
period_atr = 0
handle_mah = 0
handle_mal = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_mah, handle_mal, period_atr, period_ma
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    SetIndexBuffer(0, BufferKOT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KOT')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferKOT, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') on PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mal = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') on PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_atr, period_ma)
    if rates_total < (max_ + 2):
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 3
        ArrayInitialize(BufferKOT, EMPTY_VALUE)
        ArrayInitialize(BufferMAH, EMPTY_VALUE)
        ArrayInitialize(BufferMAL, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        flag = 0
        BufferKOT[i] = EMPTY_VALUE
        if close[i] < low[i + 1] and close[i] < low[i + 2]:
            BufferKOT[i] = BufferMAH[i] + (InpMultiplier * BufferATR[i])
        if close[i] > high[i + 1] and close[i] > high[i + 2]:
            BufferKOT[i] = BufferMAL[i] - (InpMultiplier * BufferATR[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KOT(_MQL5Indicator):
    name = 'KOT'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodATR': 10,  # ATR period
        'InpPeriodMA': 3,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # MA method
        'InpMultiplier': 0.1,  # Multiplier
    }

