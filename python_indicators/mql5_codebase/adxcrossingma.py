"""ADXCrossingMA — converted from MQL5: MQL5 Indicators/ADXCrossingMA/ADXCrossingMA.mq5

Copyright: Copyright © 2012, Amir; Link: http://www.forex-instruments.info; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Amir', 'link': 'http://www.forex-instruments.info', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [42495], 2: [65280]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'ADXCrossingMA Sell', 2: 'ADXCrossingMA Buy'}, 'levels': [], 'description': [], 'name': 'ADXCrossingMA', 'source': 'MQL5 Indicators/ADXCrossingMA/ADXCrossingMA.mq5', 'folder': 'ADXCrossingMA', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 0.33, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 14)
alpha1 = _input('alpha1', 0.25)
alpha2 = _input('alpha2', 0.33)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ADX_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(period, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    ADX_Handle = iADX(None, 0, period)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ADX')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ADXCrossingMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DiMinus_, _s_OnCalculate_DiPlus_, _s_OnCalculate_SDiMinus_, _s_OnCalculate_SDiPlus_
    if (BarsCalculated(ADX_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    DIP = Arr(0, 0.0)
    DIM = Arr(0, 0.0)
    DiPlus = 0.0
    DiMinus = 0.0
    SDiPlus = 0.0
    SDiMinus = 0.0
    diff_DI = 0.0
    diff_DI_ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_SDiPlus_ = 0.0
        _s_OnCalculate_SDiMinus_ = 0.0
        _s_OnCalculate_DiPlus_ = 0.0
        _s_OnCalculate_DiMinus_ = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, DIP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, DIM) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(DIP, True)
    ArraySetAsSeries(DIM, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        DiPlus = (2 * DIP[bar]) + ((alpha1 - 2) * DIP[bar + 1]) + ((1 - alpha1) * _s_OnCalculate_DiPlus_)
        DiMinus = (2 * DIM[bar]) + ((alpha1 - 2) * DIM[bar + 1]) + ((1 - alpha1) * _s_OnCalculate_DiMinus_)
        SDiPlus = (alpha2 * DiPlus) + ((1 - alpha2) * _s_OnCalculate_SDiPlus_)
        SDiMinus = (alpha2 * DiMinus) + ((1 - alpha2) * _s_OnCalculate_SDiMinus_)
        diff_DI = SDiPlus - SDiMinus
        diff_DI_ = _s_OnCalculate_SDiPlus_ - _s_OnCalculate_SDiMinus_
        if diff_DI_ <= 0 and diff_DI > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if diff_DI_ >= 0 and diff_DI < 0:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_DiPlus_ = DiPlus
            _s_OnCalculate_DiMinus_ = DiMinus
            _s_OnCalculate_SDiPlus_ = SDiPlus
            _s_OnCalculate_SDiMinus_ = SDiMinus
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_DiPlus_ = 0.0
_s_OnCalculate_DiMinus_ = 0.0
_s_OnCalculate_SDiPlus_ = 0.0
_s_OnCalculate_SDiMinus_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXCrossingMA(_MQL5Indicator):
    name = 'ADXCrossingMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 14,
        'alpha1': 0.25,
        'alpha2': 0.33,
    }

