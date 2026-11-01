"""woodiescci — converted from MQL5: MQL5 Indicators/Woodies CCI/woodiescci.mq5

WoodiesCCI
Copyright: Copyright © 2005, Gaba; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Gaba', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [65280, 255], 2: [36095, 8421504, 16711680]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'WoodiesCCI Signal', 2: 'WoodiesCCI'}, 'levels': [200.0, 100.0, 0.0, -100.0, -200.0], 'description': ['WoodiesCCI'], 'name': 'woodiescci', 'source': 'MQL5 Indicators/Woodies CCI/woodiescci.mq5', 'folder': 'Woodies CCI', 'inputs': [{'mql': 'fastPeriod', 'py': 'fastPeriod', 'param': 'fastPeriod', 'type': 'uint', 'default': 6, 'label': 'Fast CCI period', 'sinput': False}, {'mql': 'slowPeriod', 'py': 'slowPeriod', 'param': 'slowPeriod', 'type': 'uint', 'default': 14, 'label': 'Slow CCI period', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
fastPeriod = _input('fastPeriod', 6)  # Fast CCI period
slowPeriod = _input('slowPeriod', 14)  # Slow CCI period
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)  # Price
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
Fast_Handle = 0
Slow_Handle = 0

def OnInit():
    global Fast_Handle, Slow_Handle, min_rates_total
    min_rates_total = _int(MathMax(fastPeriod, slowPeriod) + 8)
    Fast_Handle = iCCI(Symbol(), PERIOD_CURRENT, fastPeriod, CCIPrice)
    if Fast_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Fast CCI indicator')
        return INIT_FAILED
    Slow_Handle = iCCI(Symbol(), PERIOD_CURRENT, slowPeriod, CCIPrice)
    if Slow_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the slow CCI indicator')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WoodiesCCI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Fast_Handle) < rates_total or BarsCalculated(Slow_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    slowCCI = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Fast_Handle, 0, 0, to_copy, UpBuffer) <= 0:
        return 0
    if CopyBuffer(Slow_Handle, 0, 0, to_copy, DnBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = DnBuffer[bar]
        up = 0
        dn = 0
        for kkk in range(0, 8):
            slowCCI = DnBuffer[bar + kkk]
            if slowCCI > 0:
                up += 1
            if slowCCI <= 0:
                dn += 1
        ColorIndBuffer[bar] = 1.0
        if up > 5:
            ColorIndBuffer[bar] = 2.0
        if dn > 5:
            ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Woodiescci(_MQL5Indicator):
    name = 'woodiescci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'fastPeriod': 6,  # Fast CCI period
        'slowPeriod': 14,  # Slow CCI period
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

