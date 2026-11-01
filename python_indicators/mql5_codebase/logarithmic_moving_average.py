"""Logarithmic Moving Average — converted from MQL5: MQL5 Indicators/Logarithmic Moving Average/Logarithmic Moving Average.mq5

Copyright: Copyright 2024, Rosh Jardine; Link: https://www.mql5.com/en/users/roshjardine; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rosh Jardine', 'link': 'https://www.mql5.com/en/users/roshjardine', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'LogMALine'}, 'levels': [], 'description': [], 'name': 'Logarithmic Moving Average', 'source': 'MQL5 Indicators/Logarithmic Moving Average/Logarithmic Moving Average.mq5', 'folder': 'Logarithmic Moving Average', 'inputs': [{'mql': 'InputLogMAPeriod', 'py': 'InputLogMAPeriod', 'param': 'InputLogMAPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'InputLogMAShift', 'py': 'InputLogMAShift', 'param': 'InputLogMAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InputAppliedPriceEnum', 'py': 'InputAppliedPriceEnum', 'param': 'InputAppliedPriceEnum', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InputLogMAPeriod = _input('InputLogMAPeriod', 7)
InputLogMAShift = _input('InputLogMAShift', 0)
InputAppliedPriceEnum = _input('InputAppliedPriceEnum', PRICE_CLOSE)
LogMALineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LogMALineBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InputLogMAPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InputLogMAShift)
    short_name = 'LogMA-' + EnumToString(InputAppliedPriceEnum, 'ENUM_APPLIED_PRICE') + '(' + IntegerToString(InputLogMAPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    hp = DBL_MIN
    lp = DBL_MAX
    if rates_total <= 0:
        return 0
    if prev_calculated <= 0:
        for i in range(0, InputLogMAPeriod):
            p = GET_APPLIED_PRICE(open[i], low[i], high[i], close[i])
            hp = (p if (p > hp) else hp)
            lp = (p if (p < lp) else lp)
        Print('hp = ', DoubleToString(hp, Digits()))
        Print('lp = ', DoubleToString(lp, Digits()))
        LogMALineBuffer[InputLogMAPeriod - 1] = _fdiv(hp - lp, MathLog(hp) - MathLog(lp))
        hp = DBL_MIN
        lp = DBL_MAX
        for i in range(InputLogMAPeriod, rates_total):
            for j in range(i, i - InputLogMAPeriod, -1):
                p = GET_APPLIED_PRICE(open[j], low[j], high[j], close[j])
                hp = (p if (p > hp) else hp)
                lp = (p if (p < lp) else lp)
            LogMALineBuffer[i] = _fdiv(hp - lp, MathLog(hp) - MathLog(lp))
            hp = DBL_MIN
            lp = DBL_MAX
        return rates_total
    else:
        for i in range(prev_calculated, rates_total - 1 + 1):
            for j in range(i, i - InputLogMAPeriod, -1):
                p = GET_APPLIED_PRICE(open[j], low[j], high[j], close[j])
                hp = (p if (p > hp) else hp)
                lp = (p if (p < lp) else lp)
            LogMALineBuffer[i] = _fdiv(hp - lp, MathLog(hp) - MathLog(lp))
            hp = DBL_MIN
            lp = DBL_MAX
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


class LogarithmicMovingAverage(_MQL5Indicator):
    name = 'Logarithmic Moving Average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InputLogMAPeriod': 7,
        'InputLogMAShift': 0,
        'InputAppliedPriceEnum': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

