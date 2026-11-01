"""Geometric Moving Average — converted from MQL5: MQL5 Indicators/Geometric Moving Average/Geometric Moving Average.mq5

Copyright: Copyright 2024, Lyn Astara; Link: https://www.mql5.com/en/users/roshjardine; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Lyn Astara', 'link': 'https://www.mql5.com/en/users/roshjardine', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'GeoMALine'}, 'levels': [], 'description': [], 'name': 'Geometric Moving Average', 'source': 'MQL5 Indicators/Geometric Moving Average/Geometric Moving Average.mq5', 'folder': 'Geometric Moving Average', 'inputs': [{'mql': 'InputGeoMAPeriod', 'py': 'InputGeoMAPeriod', 'param': 'InputGeoMAPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'InputGeoMAShift', 'py': 'InputGeoMAShift', 'param': 'InputGeoMAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InputAppliedPriceEnum', 'py': 'InputAppliedPriceEnum', 'param': 'InputAppliedPriceEnum', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InputGeoMAPeriod = _input('InputGeoMAPeriod', 7)
InputGeoMAShift = _input('InputGeoMAShift', 0)
InputAppliedPriceEnum = _input('InputAppliedPriceEnum', PRICE_CLOSE)
GeoMALineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, GeoMALineBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InputGeoMAPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InputGeoMAShift)
    short_name = 'GeoMA-' + EnumToString(InputAppliedPriceEnum, 'ENUM_APPLIED_PRICE') + '(' + IntegerToString(InputGeoMAPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    p_t = 0.0
    p_0 = 0.0
    if rates_total <= 0:
        return 0
    if prev_calculated <= 0:
        p_t = GET_APPLIED_PRICE(open[0], low[0], high[0], close[0])
        GeoMALineBuffer[0] = EMPTY_VALUE
        for i in range(1, InputGeoMAPeriod):
            p_t *= GET_APPLIED_PRICE(open[i], low[i], high[i], close[i])
        GeoMALineBuffer[InputGeoMAPeriod - 1] = MathPow(p_t, _s_OnCalculate_x)
        for i in range(InputGeoMAPeriod, rates_total):
            p_0 = _fdiv(p_t, GET_APPLIED_PRICE(open[i - InputGeoMAPeriod], low[i - InputGeoMAPeriod], high[i - InputGeoMAPeriod], close[i - InputGeoMAPeriod]))
            p_t = p_0 * GET_APPLIED_PRICE(open[i], low[i], high[i], close[i])
            GeoMALineBuffer[i] = MathPow(p_t, _s_OnCalculate_x)
        return rates_total
    for i in range(prev_calculated, rates_total - 1 + 1):
        p_0 = _fdiv(p_t, GET_APPLIED_PRICE(open[i - InputGeoMAPeriod], low[i - InputGeoMAPeriod], high[i - InputGeoMAPeriod], close[i - InputGeoMAPeriod]))
        p_t = p_0 * GET_APPLIED_PRICE(open[i], low[i], high[i], close[i])
        GeoMALineBuffer[i] = MathPow(p_t, _s_OnCalculate_x)
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

# ---- static local variables
_s_OnCalculate_x = 1.0 / float(InputGeoMAPeriod)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GeometricMovingAverage(_MQL5Indicator):
    name = 'Geometric Moving Average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InputGeoMAPeriod': 7,
        'InputGeoMAShift': 0,
        'InputAppliedPriceEnum': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

