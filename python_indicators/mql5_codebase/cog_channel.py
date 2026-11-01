"""COG_Channel — converted from MQL5: MQL5 Indicators/COG_Channel/COG_Channel.mq5

Center of Gravity Channel indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 5}, 'colors': {1: [255], 2: [32768], 3: [15128749], 4: [15128749], 5: [32768], 6: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Top Deviation', 2: 'Bottom Deviation', 3: 'Top ATR', 4: 'Bottom ATR', 5: 'Basis', 6: 'Contraction'}, 'levels': [], 'description': ['Center of Gravity Channel indicator'], 'name': 'COG_Channel', 'source': 'MQL5 Indicators/COG_Channel/COG_Channel.mq5', 'folder': 'COG_Channel', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 34, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpMultiplierDev', 'py': 'InpMultiplierDev', 'param': 'InpMultiplierDev', 'type': 'double', 'default': 2.5, 'label': 'Deviation multiplier', 'sinput': False}, {'mql': 'InpMultiplierATR', 'py': 'InpMultiplierATR', 'param': 'InpMultiplierATR', 'type': 'double', 'default': 2.0, 'label': 'ATR multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 34)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpMultiplierDev = _input('InpMultiplierDev', 2.5)  # Deviation multiplier
InpMultiplierATR = _input('InpMultiplierATR', 2.0)  # ATR multiplier
BufferUL = Arr(0, 0.0)
BufferLL = Arr(0, 0.0)
BufferULS = Arr(0, 0.0)
BufferLLS = Arr(0, 0.0)
BufferBasis = Arr(0, 0.0)
BufferAL = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
mult_dev = 0.0
mult_atr = 0.0
period_ind = 0
handle_ma = 0
handle_dev = 0

def OnInit():
    global handle_dev, handle_ma, mult_atr, mult_dev, period_ind
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    mult_dev = InpMultiplierDev
    mult_atr = InpMultiplierATR
    SetIndexBuffer(0, BufferUL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLL, INDICATOR_DATA)
    SetIndexBuffer(2, BufferULS, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLLS, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBasis, INDICATOR_DATA)
    SetIndexBuffer(5, BufferAL, INDICATOR_DATA)
    SetIndexBuffer(6, BufferTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMA, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'COG Channel (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUL, True)
    ArraySetAsSeries(BufferLL, True)
    ArraySetAsSeries(BufferULS, True)
    ArraySetAsSeries(BufferLLS, True)
    ArraySetAsSeries(BufferBasis, True)
    ArraySetAsSeries(BufferAL, True)
    ArraySetAsSeries(BufferTR, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_ind, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_ind), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_ind, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 2
        ArrayInitialize(BufferUL, EMPTY_VALUE)
        ArrayInitialize(BufferLL, EMPTY_VALUE)
        ArrayInitialize(BufferULS, EMPTY_VALUE)
        ArrayInitialize(BufferLLS, EMPTY_VALUE)
        ArrayInitialize(BufferBasis, EMPTY_VALUE)
        ArrayInitialize(BufferAL, EMPTY_VALUE)
        ArrayInitialize(BufferTR, 0)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        x1 = high[i] - low[i]
        x2 = fabs(high[i] - close[i + 1])
        x3 = fabs(low[i] - close[i + 1])
        BufferTR[i] = fmax(x1, fmax(x2, x3))
    for i in range(limit, 0 - 1, -1):
        x = 0.0
        y = 0.0
        xy = 0.0
        x2 = 0.0
        for j in range(0, period_ind):
            y += BufferMA[i + j]
            xy += BufferMA[i + j] * j
            x += j
            x2 += j * j
        temp = (period_ind * x2) - (x * x)
        m = (_fdiv((period_ind * xy) - (x * y), temp) if (temp != 0) else 0)
        yint = _fdiv(y + (m * x), period_ind)
        BufferBasis[i] = yint - (m * period_ind)
        dev = BufferDev[i] * mult_dev
        BufferUL[i] = BufferBasis[i] + dev
        BufferLL[i] = BufferBasis[i] - dev
        atr = GetSMA(rates_total, i, period_ind, BufferTR) * mult_atr
        BufferULS[i] = BufferBasis[i] + atr
        BufferLLS[i] = BufferBasis[i] - atr
        BufferAL[i] = (BufferBasis[i] if (BufferULS[i] > BufferUL[i] and BufferLLS[i] < BufferLL[i]) else EMPTY_VALUE)
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


class COGChannel(_MQL5Indicator):
    name = 'COG_Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 34,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpMultiplierDev': 2.5,  # Deviation multiplier
        'InpMultiplierATR': 2.0,  # ATR multiplier
    }

