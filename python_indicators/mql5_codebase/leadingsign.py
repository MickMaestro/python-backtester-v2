"""leadingsign — converted from MQL5: MQL5 Indicators/LeadingSign/leadingsign.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'LeadingSign Sell', 2: 'LeadingSign Buy'}, 'levels': [], 'description': [], 'name': 'leadingsign', 'source': 'MQL5 Indicators/LeadingSign/leadingsign.mq5', 'folder': 'LeadingSign', 'inputs': [{'mql': 'Alpha1', 'py': 'Alpha1', 'param': 'Alpha1', 'type': 'double', 'default': 0.25, 'label': '1 коэффициент индикатора', 'sinput': False}, {'mql': 'Alpha2', 'py': 'Alpha2', 'param': 'Alpha2', 'type': 'double', 'default': 0.33, 'label': '2 коэффициент индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha1 = _input('Alpha1', 0.25)  # 1 коэффициент индикатора
Alpha2 = _input('Alpha2', 0.33)  # 2 коэффициент индикатора
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def Get_Price(High, Low, bar):
    return (High[bar] + Low[bar]) / 2

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 2)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 171)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 171)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'LeadingSign'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_EMA_, _s_OnCalculate_Lead_, _s_OnCalculate_NetLead_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    Lead = 0.0
    NetLead = 0.0
    EMA = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    maxbar = rates_total - min_rates_total
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    Lead = _s_OnCalculate_Lead_
    NetLead = _s_OnCalculate_NetLead_
    EMA = _s_OnCalculate_EMA_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_Lead_ = Lead
        if bar < maxbar:
            Lead = (2.0 * Get_Price(high, low, bar)) + ((Alpha1 - 2.0) * Get_Price(high, low, bar + 1)) + ((1.0 - Alpha1) * _s_OnCalculate_Lead_)
            NetLead = (Alpha2 * Lead) + ((1 - Alpha2) * _s_OnCalculate_NetLead_)
            EMA = (0.5 * Get_Price(high, low, bar)) + (0.5 * _s_OnCalculate_EMA_)
        else:
            Lead = Get_Price(high, low, bar)
            NetLead = Lead
            EMA = Lead
            if bar:
                _s_OnCalculate_NetLead_ = NetLead
                _s_OnCalculate_Lead_ = Lead
                _s_OnCalculate_EMA_ = EMA
            continue
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_EMA_ > _s_OnCalculate_Lead_ and EMA < Lead:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_EMA_ < _s_OnCalculate_Lead_ and EMA > Lead:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_NetLead_ = NetLead
            _s_OnCalculate_Lead_ = Lead
            _s_OnCalculate_EMA_ = EMA
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Lead_ = 0.0
_s_OnCalculate_NetLead_ = 0.0
_s_OnCalculate_EMA_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Leadingsign(_MQL5Indicator):
    name = 'leadingsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha1': 0.25,  # 1 коэффициент индикатора
        'Alpha2': 0.33,  # 2 коэффициент индикатора
    }

