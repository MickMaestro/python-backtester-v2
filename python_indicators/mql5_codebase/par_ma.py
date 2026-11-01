"""Par_MA — converted from MQL5: MQL5 Indicators/Par_MA/Par_MA.mq5

Parabolic Moving Average indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Parabolic MA'}, 'levels': [], 'description': ['Parabolic Moving Average indicator'], 'name': 'Par_MA', 'source': 'MQL5 Indicators/Par_MA/Par_MA.mq5', 'folder': 'Par_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferPMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
sum_x = 0.0
sum_x2 = 0.0
sum_x3 = 0.0
sum_x4 = 0.0
period_pma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_pma, sum_x, sum_x2, sum_x3, sum_x4
    period_pma = (3 if (InpPeriod < 3) else InpPeriod)
    sum_x = ((1.0 + period_pma) * period_pma) / 2.0
    sum_x2 = ((1.0 + period_pma) * ((2.0 * period_pma) + 1.0) * period_pma) / 6.0
    sum_x3 = sum_x * sum_x
    sum_x4 = ((1.0 + period_pma) * period_pma * ((2.0 * period_pma) + 1.0) * ((3.0 * period_pma * period_pma) + (3.0 * period_pma) - 1.0)) / 30.0
    SetIndexBuffer(0, BufferPMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Parabolic MA (' + _str(period_pma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_pma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_pma - 1
        ArrayInitialize(BufferPMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_y = 0.0
        sum_xy = 0.0
        sum_x2y = 0.0
        for j in range(1, period_pma + 1):
            tmp = BufferMA[i + period_pma - j]
            sum_y += tmp
            sum_xy += tmp * j
            sum_x2y += tmp * j * j
        F = sum_x3
        M = sum_x4
        P = sum_y
        R = sum_xy
        S = sum_x2y
        E = sum_x2
        L = sum_x3
        Q = _fdiv(sum_x, period_pma)
        E -= Q * sum_x
        F -= Q * sum_x2
        R -= Q * P
        Q = _fdiv(sum_x2, period_pma)
        L -= Q * sum_x
        M -= Q * sum_x2
        S -= Q * P
        Q = _fdiv(L, E)
        B2 = _fdiv(S - (R * Q), M - (F * Q))
        B1 = _fdiv(R - (F * B2), E)
        B0 = _fdiv(P - (sum_x * B1) - (sum_x2 * B2), period_pma)
        BufferPMA[i] = B0 + ((B1 + (B2 * period_pma)) * period_pma)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ParMA(_MQL5Indicator):
    name = 'Par_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

