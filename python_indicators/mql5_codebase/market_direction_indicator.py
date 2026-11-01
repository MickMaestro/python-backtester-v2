"""Market_Direction_Indicator — converted from MQL5: MQL5 Indicators/Market_Direction_Indicator/Market_Direction_Indicator.mq5

Market Direction Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11119017, 65280, 7451452, 255, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MDI'}, 'levels': [], 'description': ['Market Direction Indicator'], 'name': 'Market_Direction_Indicator', 'source': 'MQL5 Indicators/Market_Direction_Indicator/Market_Direction_Indicator.mq5', 'folder': 'Market_Direction_Indicator', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 13, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 55, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpCutoff', 'py': 'InpCutoff', 'param': 'InpCutoff', 'type': 'uint', 'default': 2, 'label': 'Cutoff in points', 'sinput': False}, {'mql': 'InpShowBelowZero', 'py': 'InpShowBelowZero', 'param': 'InpShowBelowZero', 'type': 'int', 'default': 1, 'label': 'Show below zero', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 13)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 55)  # Slow MA period
InpCutoff = _input('InpCutoff', 2)  # Cutoff in points
InpShowBelowZero = _input('InpShowBelowZero', INPUT_YES)  # Show below zero
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMDI = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferCP = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
cutoff = 0.0
period_fma = 0
period_sma = 0
period_max = 0
handle_fma = 0
handle_sma = 0
handle_ma1 = 0

def OnInit():
    global cutoff, handle_fma, handle_ma1, handle_sma, period_fma, period_max, period_sma
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_sma = ((period_fma + 1) if (InpPeriodSlow == period_fma) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_max = fmax(period_fma, period_sma)
    cutoff = _fdiv(InpCutoff, Point())
    SetIndexBuffer(0, BufferMDI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferCP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MDI (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(InpCutoff) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max + 2)
    ArraySetAsSeries(BufferMDI, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferCP, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, MODE_SMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferMDI, 0)
        ArrayInitialize(BufferColors, 0)
        ArrayInitialize(BufferCP, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCP[i] = period_fma * period_sma * (BufferSMA[i] - _fdiv(BufferFMA[i], period_sma - period_fma))
        sum_ = BufferMA1[i] + BufferMA1[i + 1]
        if sum_ != 0:
            if InpShowBelowZero:
                BufferMDI[i] = _fdiv(_fdiv(200.0 * (BufferCP[i + 1] - BufferCP[i]), sum_), Point())
            else:
                BufferMDI[i] = _fdiv(200.0 * fabs(_fdiv(BufferCP[i + 1] - BufferCP[i], sum_)), Point())
        else:
            BufferMDI[i] = 0.0
        BufferColors[i] = ((3 if (BufferMDI[i] > BufferMDI[i + 1]) else 4) if (BufferMDI[i] < (-cutoff)) else (1 if (BufferMDI[i] > BufferMDI[i + 1]) else 2) if (BufferMDI[i] > cutoff) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MarketDirectionIndicator(_MQL5Indicator):
    name = 'Market_Direction_Indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 13,  # Fast MA period
        'InpPeriodSlow': 55,  # Slow MA period
        'InpCutoff': 2,  # Cutoff in points
        'InpShowBelowZero': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show below zero
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

