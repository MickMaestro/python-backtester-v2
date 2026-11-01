"""Total_Power — converted from MQL5: MQL5 Indicators/Total_Power/Total_Power.mq5

Total Power indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Total Power', 2: 'Bear Power', 3: 'Bull Power'}, 'levels': [], 'description': ['Total Power indicator'], 'name': 'Total_Power', 'source': 'MQL5 Indicators/Total_Power/Total_Power.mq5', 'folder': 'Total_Power', 'inputs': [{'mql': 'InpPeriodPW', 'py': 'InpPeriodPW', 'param': 'InpPeriodPW', 'type': 'uint', 'default': 40, 'label': 'Power period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 10, 'label': 'EMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodPW = _input('InpPeriodPW', 40)  # Power period
InpPeriodMA = _input('InpPeriodMA', 10)  # EMA period
BufferPower = Arr(0, 0.0)
BufferPowerBear = Arr(0, 0.0)
BufferPowerBull = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
period_pw = 0
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, period_pw
    period_pw = (1 if (InpPeriodPW < 1) else InpPeriodPW)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    SetIndexBuffer(0, BufferPower, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPowerBear, INDICATOR_DATA)
    SetIndexBuffer(2, BufferPowerBull, INDICATOR_DATA)
    SetIndexBuffer(3, BufferEMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Total Power (' + _str(period_pw) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPower, True)
    ArraySetAsSeries(BufferPowerBear, True)
    ArraySetAsSeries(BufferPowerBull, True)
    ArraySetAsSeries(BufferEMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_pw - 1
        ArrayInitialize(BufferPower, EMPTY_VALUE)
        ArrayInitialize(BufferPowerBear, EMPTY_VALUE)
        ArrayInitialize(BufferPowerBull, EMPTY_VALUE)
        ArrayInitialize(BufferEMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferEMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BullCount = 0.0
        BearCount = 0.0
        for j in range(0, period_pw - 1 + 1):
            if high[i + j] > BufferEMA[i + j]:
                BullCount += 1
            if low[i + j] < BufferEMA[i + j]:
                BearCount += 1
        BufferPowerBull[i] = _fdiv(BullCount * 100, period_pw)
        BufferPowerBear[i] = _fdiv(BearCount * 100, period_pw)
        BufferPower[i] = _fdiv(fabs(BearCount - BullCount) * 100, period_pw)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TotalPower(_MQL5Indicator):
    name = 'Total_Power'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodPW': 40,  # Power period
        'InpPeriodMA': 10,  # EMA period
    }

