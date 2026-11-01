"""stodiv — converted from MQL5: MQL5 Indicators/StoDiv/stodiv.mq5

Copyright: Copyright © 2005-2006, RickD; Link: http://e2e-fx.net/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005-2006, RickD', 'link': 'http://e2e-fx.net/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [8421376]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'StoDiv Sell', 2: 'StoDiv Buy'}, 'levels': [], 'description': [], 'name': 'stodiv', 'source': 'MQL5 Indicators/StoDiv/stodiv.mq5', 'folder': 'StoDiv', 'inputs': [{'mql': 'DxPeriod', 'py': 'DxPeriod', 'param': 'DxPeriod', 'type': 'uint', 'default': 30, 'label': 'Bars, used to search fractals', 'sinput': False}, {'mql': 'dy', 'py': 'dy', 'param': 'dy', 'type': 'int', 'default': 20, 'label': 'Threshold level in points', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DxPeriod = _input('DxPeriod', 30)  # Bars, used to search fractals
dy = _input('dy', 20)  # Threshold level in points
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
DY = 0.0
ratio = 0.0
Fra_Handle = 0
Sto_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, DY, Fra_Handle, Sto_Handle, min_rates_total, ratio
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, DxPeriod + KPeriod + DPeriod + Slowing) + 5)
    DY = dy * Point()
    ratio = 3.0 / 8.0
    Fra_Handle = iFractals(None, 0)
    if Fra_Handle == INVALID_HANDLE:
        Print(' Error in creation of iFractals indicator')
        return 1
    Sto_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, MA_Method, Price_field)
    if Sto_Handle == INVALID_HANDLE:
        Print(' Error in creation of iStochastic indicator')
        return 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Error in creation of iATR indicator')
        return 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'StoDiv Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'StoDiv Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'StoDivSig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(Sto_Handle) < rates_total or BarsCalculated(Fra_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar2 = 0
    j2 = 0
    total = 0
    Sto = Arr(0, 0.0)
    UpFrac = Arr(0, 0.0)
    DnFrac = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 5
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += _int(5 + DxPeriod)
    if CopyBuffer(Sto_Handle, 0, 0, to_copy, Sto) <= 0:
        return 0
    if CopyBuffer(Fra_Handle, 0, 0, to_copy, UpFrac) <= 0:
        return 0
    if CopyBuffer(Fra_Handle, 1, 0, to_copy, DnFrac) <= 0:
        return 0
    ArraySetAsSeries(Sto, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(UpFrac, True)
    ArraySetAsSeries(DnFrac, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        bar2 = bar + 2
        SellBuffer[bar] = 0.0
        if UpFrac[bar2] == EMPTY_VALUE:
            continue
        total = _int(bar + DxPeriod)
        for j in range(bar + 1, total):
            j2 = j + 2
            if UpFrac[j2] == EMPTY_VALUE:
                continue
            if UpFrac[bar2] > (UpFrac[j2] + DY):
                if Sto[bar2] < Sto[j2]:
                    SellBuffer[bar] = high[bar] + (ATR[bar] * ratio)
                    break
    for bar in range(limit, 0 - 1, -1):
        bar2 = bar + 2
        BuyBuffer[bar] = 0.0
        if DnFrac[bar2] == EMPTY_VALUE:
            continue
        total = _int(bar + DxPeriod)
        for j in range(bar + 1, total):
            j2 = j + 2
            if DnFrac[j2] == EMPTY_VALUE:
                continue
            if DnFrac[bar2] < (DnFrac[j2] - DY):
                if Sto[bar2] > Sto[j2]:
                    BuyBuffer[bar] = low[bar] - (ATR[bar] * ratio)
                    break
    for bar in range(limit, 0 - 1, -1):
        if SellBuffer[bar] and BuyBuffer[bar]:
            BuyBuffer[bar] = 0.0
            SellBuffer[bar] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stodiv(_MQL5Indicator):
    name = 'stodiv'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DxPeriod': 30,  # Bars, used to search fractals
        'dy': 20,  # Threshold level in points
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
    }

