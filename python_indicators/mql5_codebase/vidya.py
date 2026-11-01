"""vidya — converted from MQL5: MQL5 Indicators/Variable Index Dynamic Average (VIDYA)/vidya.mq5

Variable Index Dynamic Average
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'VIDYA'}, 'levels': [], 'description': ['Variable Index Dynamic Average'], 'name': 'vidya', 'source': 'MQL5 Indicators/Variable Index Dynamic Average (VIDYA)/vidya.mq5', 'folder': 'Variable Index Dynamic Average (VIDYA)', 'inputs': [{'mql': 'InpPeriodCMO', 'py': 'InpPeriodCMO', 'param': 'InpPeriodCMO', 'type': 'int', 'default': 9, 'label': 'Period CMO', 'sinput': False}, {'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 12, 'label': 'Period EMA', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodCMO = _input('InpPeriodCMO', 9)  # Period CMO
InpPeriodEMA = _input('InpPeriodEMA', 12)  # Period EMA
InpShift = _input('InpShift', 0)  # Indicator's shift
VIDYA_Buffer = Arr(0, 0.0)
ExtF = 0.0

def OnInit():
    global ExtF
    SetIndexBuffer(0, VIDYA_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriodEMA + InpPeriodCMO - 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VIDYA(' + _str(InpPeriodCMO) + ',' + _str(InpPeriodEMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'VIDYA(' + _str(InpPeriodCMO) + ',' + _str(InpPeriodEMA) + ')')
    ExtF = _fdiv(2.0, 1.0 + InpPeriodEMA)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (InpPeriodEMA + InpPeriodCMO - 1):
        return 0
    limit = 0
    if prev_calculated < (InpPeriodEMA + InpPeriodCMO - 1):
        limit = InpPeriodEMA + InpPeriodCMO - 1
        for i in range(0, limit):
            VIDYA_Buffer[i] = price[i]
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        mulCMO = fabs(CalculateCMO(i, InpPeriodCMO, price))
        VIDYA_Buffer[i] = (price[i] * ExtF * mulCMO) + (VIDYA_Buffer[i - 1] * (1 - (ExtF * mulCMO)))
    return rates_total

def CalculateCMO(Position, PeriodCMO, price):
    resCMO = 0.0
    UpSum = 0.0
    DownSum = 0.0
    if Position >= PeriodCMO and ArrayRange(price, 0) > Position:
        for i in range(0, PeriodCMO):
            diff = price[Position - i] - price[Position - i - 1]
            if diff > 0.0:
                UpSum += diff
            else:
                DownSum += -diff
        if (UpSum + DownSum) != 0.0:
            resCMO = _fdiv(UpSum - DownSum, UpSum + DownSum)
    return resCMO


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vidya(_MQL5Indicator):
    name = 'vidya'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCMO': 9,  # Period CMO
        'InpPeriodEMA': 12,  # Period EMA
        'InpShift': 0,  # Indicator's shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

