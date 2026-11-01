"""Harmonic Moving Average — converted from MQL5: MQL5 Indicators/Harmonic Moving Average/Harmonic Moving Average.mq5

Copyright: Copyright 2024, Rosh Jardine; Link: https://www.mql5.com/en/users/roshjardine; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rosh Jardine', 'link': 'https://www.mql5.com/en/users/roshjardine', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HMALine'}, 'levels': [], 'description': [], 'name': 'Harmonic Moving Average', 'source': 'MQL5 Indicators/Harmonic Moving Average/Harmonic Moving Average.mq5', 'folder': 'Harmonic Moving Average', 'inputs': [{'mql': 'InputHMAPeriod', 'py': 'InputHMAPeriod', 'param': 'InputHMAPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'InputHMAShift', 'py': 'InputHMAShift', 'param': 'InputHMAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InputAppliedPriceEnum', 'py': 'InputAppliedPriceEnum', 'param': 'InputAppliedPriceEnum', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InputHMAPeriod = _input('InputHMAPeriod', 7)
InputHMAShift = _input('InputHMAShift', 0)
InputAppliedPriceEnum = _input('InputAppliedPriceEnum', PRICE_CLOSE)
HMALineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, HMALineBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InputHMAShift)
    PlotIndexSetInteger(0, PLOT_SHIFT, InputHMAShift)
    short_name = 'HMA-' + EnumToString(InputAppliedPriceEnum, 'ENUM_APPLIED_PRICE') + '(' + IntegerToString(InputHMAPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= 0:
        return 0
    if prev_calculated <= 0:
        rsd = 0.0
        for i in range(0, InputHMAPeriod):
            rsd += _fdiv(1, GET_APPLIED_PRICE(open[i], low[i], high[i], close[i]))
            HMALineBuffer[i] = 0.0
        HMALineBuffer[InputHMAPeriod - 1] = _fdiv(InputHMAPeriod, rsd)
        for i in range(InputHMAPeriod, rates_total):
            lrs = _fdiv(InputHMAPeriod, HMALineBuffer[i - 1])
            vlfr = _fdiv(1, GET_APPLIED_PRICE(open[i - InputHMAPeriod], low[i - InputHMAPeriod], high[i - InputHMAPeriod], close[i - InputHMAPeriod]))
            HMALineBuffer[i] = _fdiv(InputHMAPeriod, lrs - vlfr + _fdiv(1, GET_APPLIED_PRICE(open[i], low[i], high[i], close[i])))
        return rates_total
    else:
        for i in range(prev_calculated, rates_total - 1 + 1):
            lrs = _fdiv(float(InputHMAPeriod), HMALineBuffer[i - 1])
            vlfr = _fdiv(1, GET_APPLIED_PRICE(open[i - InputHMAPeriod], low[i - InputHMAPeriod], high[i - InputHMAPeriod], close[i - InputHMAPeriod]))
            HMALineBuffer[i] = _fdiv(InputHMAPeriod, lrs - vlfr + _fdiv(1, GET_APPLIED_PRICE(open[i], low[i], high[i], close[i])))
        return rates_total

def GET_APPLIED_PRICE(ParamOpenPriceDouble, ParamLowPriceDouble, ParamHighPriceDouble, ParamClosePriceDouble):
    PriceResultDouble = ParamClosePriceDouble
    AppliedPriceInt = InputAppliedPriceEnum
    _sw1 = AppliedPriceInt
    if _sw1 == 1:
        PriceResultDouble = ParamOpenPriceDouble
    elif _sw1 == 2:
        PriceResultDouble = ParamLowPriceDouble
    elif _sw1 == 3:
        PriceResultDouble = ParamHighPriceDouble
    elif _sw1 == 4:
        PriceResultDouble = ParamClosePriceDouble
    elif _sw1 == 5:
        PriceResultDouble = (ParamHighPriceDouble + ParamLowPriceDouble) / 2
    elif _sw1 == 6:
        PriceResultDouble = (ParamHighPriceDouble + ParamLowPriceDouble + ParamClosePriceDouble) / 3
    else:
        PriceResultDouble = (ParamHighPriceDouble + ParamLowPriceDouble + ParamClosePriceDouble + ParamClosePriceDouble) / 4
    return PriceResultDouble


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HarmonicMovingAverage(_MQL5Indicator):
    name = 'Harmonic Moving Average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InputHMAPeriod': 7,
        'InputHMAShift': 0,
        'InputAppliedPriceEnum': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

