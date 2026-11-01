"""aroonsignal — converted from MQL5: MQL5 Indicators/AroonSignal/aroonsignal.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls Aroon Signal', 2: 'Bears Aroon Signal'}, 'levels': [], 'description': [], 'name': 'aroonsignal', 'source': 'MQL5 Indicators/AroonSignal/aroonsignal.mq5', 'folder': 'AroonSignal', 'inputs': [{'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 85, 'label': 'overbought level', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': 15, 'label': 'oversold level', 'sinput': False}, {'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 9, 'label': 'indicator period', 'sinput': False}, {'mql': 'AroonShift', 'py': 'AroonShift', 'param': 'AroonShift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
HighLevel = _input('HighLevel', 85)  # overbought level
LowLevel = _input('LowLevel', 15)  # oversold level
AroonPeriod = _input('AroonPeriod', 9)  # indicator period
AroonShift = _input('AroonShift', 0)  # horizontal shift of the indicator in bars
BullsAroonBuffer = Arr(0, 0.0)
BearsAroonBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(AroonPeriod, 10)
    SetIndexBuffer(0, BullsAroonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, AroonPeriod)
    PlotIndexSetInteger(0, PLOT_ARROW, 117)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(BullsAroonBuffer, True)
    SetIndexBuffer(1, BearsAroonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, AroonPeriod)
    PlotIndexSetInteger(1, PLOT_ARROW, 117)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(BearsAroonBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'AroonSignal(', AroonPeriod, ', ', AroonShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastTrend
    if rates_total < min_rates_total:
        return 0
    limit = 0
    BULLS = 0.0
    BEARS = 0.0
    Range = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastTrend = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        BullsAroonBuffer[bar] = EMPTY_VALUE
        BearsAroonBuffer[bar] = EMPTY_VALUE
        BULLS = 100 - (((ArrayMaximum(high, bar, AroonPeriod) - bar + 0.5) * 100) / AroonPeriod)
        BEARS = 100 - (((ArrayMinimum(low, bar, AroonPeriod) - bar + 0.5) * 100) / AroonPeriod)
        if BULLS > HighLevel and BEARS < LowLevel:
            if _s_OnCalculate_LastTrend == -1:
                Range = 0.0
                for count in range(bar, bar + 10):
                    Range += MathAbs(high[count] - low[count])
                Range *= 0.5 / 10
                BullsAroonBuffer[bar] = low[bar] - Range
            _s_OnCalculate_LastTrend = 1
            continue
        if BULLS < LowLevel and BEARS > HighLevel:
            if _s_OnCalculate_LastTrend == 1:
                Range = 0.0
                for count in range(bar, bar + 10):
                    Range += MathAbs(high[count] - low[count])
                Range *= 0.5 / 10
                BearsAroonBuffer[bar] = high[bar] + Range
            _s_OnCalculate_LastTrend = -1
            continue
    return rates_total

# ---- static local variables
_s_OnCalculate_LastTrend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Aroonsignal(_MQL5Indicator):
    name = 'aroonsignal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HighLevel': 85,  # overbought level
        'LowLevel': 15,  # oversold level
        'AroonPeriod': 9,  # indicator period
        'AroonShift': 0,  # horizontal shift of the indicator in bars
    }

