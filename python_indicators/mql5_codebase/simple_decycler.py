"""Simple_Decycler — converted from MQL5: MQL5 Indicators/Simple_Decycler/Simple_Decycler.mq5

John F.Ehlers Simple Decycler indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Decicler', 2: 'Top', 3: 'Bottom'}, 'levels': [], 'description': ['John F.Ehlers Simple Decycler indicator'], 'name': 'Simple_Decycler', 'source': 'MQL5 Indicators/Simple_Decycler/Simple_Decycler.mq5', 'folder': 'Simple_Decycler', 'inputs': [{'mql': 'InpPeriodHP', 'py': 'InpPeriodHP', 'param': 'InpPeriodHP', 'type': 'double', 'default': 125.0, 'label': 'HP period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodHP = _input('InpPeriodHP', 125.0)  # HP period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDecicle = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferHP = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_hp = 0.0
angle1 = 0.0
angle2 = 0.0
alpha1 = 0.0
alpha2 = 0.0
handle_ma = 0

def OnInit():
    global alpha1, alpha2, angle1, angle2, handle_ma, period_hp
    period_hp = (2 if (InpPeriodHP < 2) else InpPeriodHP)
    angle1 = _fdiv(1.414 * M_PI, period_hp)
    angle2 = 2.0 * angle1
    alpha1 = _fdiv(cos(angle1) + sin(angle1) - 1.0, cos(angle1))
    alpha2 = _fdiv(cos(angle2) + sin(angle2) - 1.0, cos(angle2))
    SetIndexBuffer(0, BufferDecicle, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferHP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Simple Decycler (' + DoubleToString(period_hp, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDecicle, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferHP, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferDecicle, 0)
        ArrayInitialize(BufferTop, 0)
        ArrayInitialize(BufferBottom, 0)
        ArrayInitialize(BufferHP, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        a1 = 1.0 - alpha1
        a2 = 1.0 - (alpha1 / 2.0)
        a3 = a1 * a1
        a4 = a2 * a2
        pr2 = 2.0 * BufferMA[i + 1]
        pr3 = BufferMA[i] - pr2 + BufferMA[i + 2]
        BufferHP[i] = (a4 * pr3) + (2.0 * a1 * BufferHP[i + 1]) - (a3 * BufferHP[i + 2])
        BufferDecicle[i] = BufferMA[i] - BufferHP[i]
        BufferTop[i] = BufferDecicle[i] * 1.005
        BufferBottom[i] = BufferDecicle[i] * 0.995
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleDecycler(_MQL5Indicator):
    name = 'Simple_Decycler'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodHP': 125.0,  # HP period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

