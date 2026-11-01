"""iStochKomposter — converted from MQL5: MQL5 Indicators/iStochKomposter_HTF_Signal/iStochKomposter.mq5

Copyright: Copyright © 2006, komposter; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, komposter', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [8036607], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'iStochKomposter Sell', 2: 'iStochKomposter Buy'}, 'levels': [], 'description': [], 'name': 'iStochKomposter', 'source': 'MQL5 Indicators/iStochKomposter_HTF_Signal/iStochKomposter.mq5', 'folder': 'iStochKomposter_HTF_Signal', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 70, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 14)
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
STO_Method = _input('STO_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
UpLevel = _input('UpLevel', 70)  # уровень перекупленности
DnLevel = _input('DnLevel', 30)  # уровень перепроданности
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Sto_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, Sto_Handle, min_rates_total
    min_rates_total = _int(MathMax(KPeriod + DPeriod + Slowing + 1, ATR_Period)) + 1
    Sto_Handle = iStochastic(Symbol(), None, KPeriod, DPeriod, Slowing, STO_Method, Price_field)
    if Sto_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора Stochastic')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'iStochKomposter'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Sto_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    STO = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Sto_Handle, 0, MAIN_LINE, to_copy + 1, STO) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(STO, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if STO[bar] > DnLevel and STO[bar + 1] <= DnLevel:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if STO[bar] < UpLevel and STO[bar + 1] >= UpLevel:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IStochKomposter(_MQL5Indicator):
    name = 'iStochKomposter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 14,
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel': 70,  # уровень перекупленности
        'DnLevel': 30,  # уровень перепроданности
    }

