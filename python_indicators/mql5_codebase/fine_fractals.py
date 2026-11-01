"""fine_fractals — converted from MQL5: MQL5 Indicators/Fine_Fractals_MTF/fine_fractals.mq5

Fine Fractals
Copyright: Copyright © 2009 Денис Орлов; Link: http://denis-or-love.narod.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009 Денис Орлов', 'link': 'http://denis-or-love.narod.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': ['Fine Fractals'], 'name': 'fine_fractals', 'source': 'MQL5 Indicators/Fine_Fractals_MTF/fine_fractals.mq5', 'folder': 'Fine_Fractals_MTF', 'inputs': [{'mql': 'Fine', 'py': 'Fine', 'param': 'Fine', 'type': 'bool', 'default': True, 'label': 'Sensibility', 'sinput': False}, {'mql': 'FlatShift', 'py': 'FlatShift', 'param': 'FlatShift', 'type': 'bool', 'default': True, 'label': 'Shift', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 164, 'label': 'Upper fractal symbol code', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 164, 'label': 'Lower fractal symbol code', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fine = _input('Fine', True)  # Sensibility
FlatShift = _input('FlatShift', True)  # Shift
UpLable = _input('UpLable', 164)  # Upper fractal symbol code
DnLable = _input('DnLable', 164)  # Lower fractal symbol code
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
StartBars = 0
FRA_Handle = 0

def OnInit():
    global FRA_Handle, StartBars
    StartBars = 6
    FRA_Handle = iFractals(None, 0)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Up Fractal')
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Down Fractal')
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fine Fractals'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    HP1 = 0.0
    HP2 = 0.0
    HP3 = 0.0
    HPi = 0.0
    LP1 = 0.0
    LP2 = 0.0
    LP3 = 0.0
    LPi = 0.0
    res = 0.0
    UpFractal = Arr(0, 0.0)
    DnFractal = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars - 1
    else:
        to_copy = rates_total - prev_calculated + 5
        limit = rates_total - prev_calculated + 2
    if CopyBuffer(FRA_Handle, 0, 0, to_copy, UpFractal) <= 0:
        return 0
    if CopyBuffer(FRA_Handle, 1, 0, to_copy, DnFractal) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(UpFractal, True)
    ArraySetAsSeries(DnFractal, True)
    bar = 2
    while bar <= limit:
        HP1 = high[bar + 1]
        HP2 = high[bar]
        HP3 = high[bar - 1]
        HPi = high[bar - 2]
        LP1 = low[bar + 1]
        LP2 = low[bar]
        LP3 = low[bar - 1]
        LPi = low[bar - 2]
        res = UpFractal[bar]
        if res == 0 and Fine:
            if (HP1 < HP2 and HP2 > HP3) and (LP2 >= LP3 or HP2 > HPi):
                res = HP2
        if FlatShift and res != 0:
            while high[bar] == high[bar + 1]:
                bar += 1
        SellBuffer[bar] = res
        res = DnFractal[bar]
        if res == 0 and Fine:
            if (LP1 > LP2 and LP2 < LP3) and (HP2 <= HP3 or LP2 < LPi):
                res = LP2
        if FlatShift and res != 0:
            while low[bar] == low[bar + 1]:
                bar += 1
        BuyBuffer[bar] = res
        bar += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FineFractals(_MQL5Indicator):
    name = 'fine_fractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Fine': True,  # Sensibility
        'FlatShift': True,  # Shift
        'UpLable': 164,  # Upper fractal symbol code
        'DnLable': 164,  # Lower fractal symbol code
    }

