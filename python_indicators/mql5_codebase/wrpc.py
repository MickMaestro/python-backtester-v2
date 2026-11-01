"""WRPC — converted from MQL5: MQL5 Indicators/Wilson Relative Price Channel/WRPC.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {1: 1, 2: 4, 3: 1, 4: 1, 5: 4, 6: 1}, 'colors': {1: [36095], 2: [36095], 3: [36095], 4: [16760576], 5: [16760576], 6: [16760576]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Upper overbought', 2: 'Overbought zone', 3: 'Neutral Up', 4: 'Neutral Down', 5: 'Oversold zone', 6: 'Lower oversold'}, 'levels': [], 'description': [], 'name': 'WRPC', 'source': 'MQL5 Indicators/Wilson Relative Price Channel/WRPC.mq5', 'folder': 'Wilson Relative Price Channel', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 34, 'label': 'Channels period', 'sinput': False}, {'mql': 'InpSmoothing', 'py': 'InpSmoothing', 'param': 'InpSmoothing', 'type': 'uint', 'default': 14, 'label': 'Period of smoothing', 'sinput': False}, {'mql': 'InpOverBought', 'py': 'InpOverBought', 'param': 'InpOverBought', 'type': 'double', 'default': 70.0, 'label': 'Overbought level', 'sinput': False}, {'mql': 'InpUpperNeutral', 'py': 'InpUpperNeutral', 'param': 'InpUpperNeutral', 'type': 'double', 'default': 55.0, 'label': 'Upper level of neutral zone', 'sinput': False}, {'mql': 'InpLowerNeutral', 'py': 'InpLowerNeutral', 'param': 'InpLowerNeutral', 'type': 'double', 'default': 45.0, 'label': 'Lower level of neutral zone', 'sinput': False}, {'mql': 'InpOverSold', 'py': 'InpOverSold', 'param': 'InpOverSold', 'type': 'double', 'default': 30.0, 'label': 'Oversold level', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpColorOverbough', 'py': 'InpColorOverbough', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color of overbought zone', 'sinput': False}, {'mql': 'InpColorOversold', 'py': 'InpColorOversold', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Color of oversold zone', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 34)  # Channels period
InpSmoothing = _input('InpSmoothing', 14)  # Period of smoothing
InpOverBought = _input('InpOverBought', 70.0)  # Overbought level
InpUpperNeutral = _input('InpUpperNeutral', 55.0)  # Upper level of neutral zone
InpLowerNeutral = _input('InpLowerNeutral', 45.0)  # Lower level of neutral zone
InpOverSold = _input('InpOverSold', 30.0)  # Oversold level
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpColorOverbough = _input('InpColorOverbough', clrDeepSkyBlue)  # Color of overbought zone
InpColorOversold = _input('InpColorOversold', clrDarkOrange)  # Color of oversold zone
BufferUpper = Arr(0, 0.0)
BufferOverBought1 = Arr(0, 0.0)
BufferOverBought2 = Arr(0, 0.0)
BufferNeutralUP = Arr(0, 0.0)
BufferNeutralDN = Arr(0, 0.0)
BufferOverSold1 = Arr(0, 0.0)
BufferOverSold2 = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferMAOnRSI = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
handle_rsi = 0
handle_ma_on_rsi = 0
handle_ma1 = 0
period = 0
smoothing = 0
overbough = 0.0
upper_neutral = 0.0
lower_neutral = 0.0
oversold = 0.0

def OnInit():
    global handle_ma1, handle_ma_on_rsi, handle_rsi, lower_neutral, overbough, oversold, period, smoothing, upper_neutral
    period = (1 if (InpPeriod < 1) else InpPeriod)
    smoothing = (1 if (InpSmoothing < 1) else InpSmoothing)
    overbough = (1 if (InpOverBought < 1) else 99.9 if (InpOverBought > 99.9) else InpOverBought)
    upper_neutral = (0.5 if (InpUpperNeutral < 0.5) else 99.5 if (InpUpperNeutral > 99.5) else InpUpperNeutral)
    lower_neutral = (0.5 if (InpLowerNeutral < 0.5) else 99.5 if (InpLowerNeutral > 99.5) else InpLowerNeutral)
    oversold = (0.1 if (InpOverSold < 0.1) else 99 if (InpOverSold > 99) else InpOverSold)
    if overbough <= upper_neutral:
        upper_neutral = overbough - 0.1
    if upper_neutral <= lower_neutral:
        lower_neutral = upper_neutral - 0.1
    if lower_neutral < (-oversold):
        oversold = lower_neutral - 0.1
    if oversold >= lower_neutral:
        lower_neutral = oversold + 0.1
    if lower_neutral >= upper_neutral:
        upper_neutral = lower_neutral + 0.1
    if upper_neutral >= overbough:
        overbough = upper_neutral + 0.1
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferOverBought1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOverBought2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferNeutralUP, INDICATOR_DATA)
    SetIndexBuffer(4, BufferNeutralDN, INDICATOR_DATA)
    SetIndexBuffer(5, BufferOverSold1, INDICATOR_DATA)
    SetIndexBuffer(6, BufferOverSold2, INDICATOR_DATA)
    SetIndexBuffer(7, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(8, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMAOnRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferMA1, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wilson relative price channel')
    for i in range(0, 8):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, period)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, (InpColorOverbough if (i < 3) else InpColorOversold))
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferOverBought1, True)
    ArraySetAsSeries(BufferOverBought2, True)
    ArraySetAsSeries(BufferNeutralUP, True)
    ArraySetAsSeries(BufferNeutralDN, True)
    ArraySetAsSeries(BufferOverSold1, True)
    ArraySetAsSeries(BufferOverSold2, True)
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferMAOnRSI, True)
    ArraySetAsSeries(BufferMA1, True)
    ResetLastError()
    handle_rsi = iRSI(Symbol(), PERIOD_CURRENT, period, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma_on_rsi = iMA(Symbol(), PERIOD_CURRENT, smoothing, 0, MODE_EMA, handle_rsi)
    if handle_ma_on_rsi == INVALID_HANDLE:
        Print('The iMAOnRSI(', _str(smoothing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma1 = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period + smoothing):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferOverBought1, 0)
        ArrayInitialize(BufferNeutralUP, EMPTY_VALUE)
        ArrayInitialize(BufferNeutralDN, EMPTY_VALUE)
        ArrayInitialize(BufferOverSold1, EMPTY_VALUE)
        ArrayInitialize(BufferOverSold2, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma_on_rsi, 0, 0, count, BufferMAOnRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA = BufferMAOnRSI[i]
        MA0 = BufferMA1[i]
        BufferUpper[i] = MA0 * (1 - ((MA - overbough) / 100.0))
        BufferOverBought1[i] = BufferUpper[i]
        BufferNeutralUP[i] = MA0 * (1.0 - ((MA - upper_neutral) / 100.0))
        BufferOverBought2[i] = BufferNeutralUP[i]
        BufferNeutralDN[i] = MA0 * (1.0 - ((MA - lower_neutral) / 100.0))
        BufferOverSold1[i] = BufferNeutralDN[i]
        BufferLower[i] = MA0 * (1.0 - ((MA - oversold) / 100.0))
        BufferOverSold2[i] = BufferLower[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WRPC(_MQL5Indicator):
    name = 'WRPC'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 34,  # Channels period
        'InpSmoothing': 14,  # Period of smoothing
        'InpOverBought': 70.0,  # Overbought level
        'InpUpperNeutral': 55.0,  # Upper level of neutral zone
        'InpLowerNeutral': 45.0,  # Lower level of neutral zone
        'InpOverSold': 30.0,  # Oversold level
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

