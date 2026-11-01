"""solarwinds — converted from MQL5: MQL5 Indicators/SolarWinds/solarwinds.mq5

Copyright: Copyright © 2005, Yura Prokofiev; Link: Yura.prokofiev@gmail.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Yura Prokofiev', 'link': 'Yura.prokofiev@gmail.com', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 2237106, 8421504, 8421376, 65407]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Solar Winds'}, 'levels': [], 'description': [], 'name': 'solarwinds', 'source': 'MQL5 Indicators/SolarWinds/solarwinds.mq5', 'folder': 'SolarWinds', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 10, 'label': 'period of averaging', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 10)  # period of averaging
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = period
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Solar Winds')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Prev_Value
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Value = 0.0
    SolarWinds = 0.0
    price = 0.0
    MinL = 0.0
    MaxH = 0.0
    Res = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_Prev_Value = 0.0
        IndBuffer[limit + 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MaxH = high[ArrayMaximum(high, bar, period)]
        MinL = low[ArrayMinimum(low, bar, period)]
        price = (high[bar] + low[bar]) / 2
        Res = MaxH - MinL
        Value = 0.0
        if Res:
            Value = (0.33 * 2 * (_fdiv(price - MinL, Res) - 0.5)) + (0.67 * _s_OnCalculate_Prev_Value)
        Value = MathMin(MathMax(Value, -0.999), 0.999)
        Res = 1 - Value
        if Res:
            SolarWinds = (0.5 * MathLog(_fdiv(1 + Value, 1 - Value))) + (0.5 * IndBuffer[bar + 1])
        else:
            SolarWinds = 0.0
        if bar:
            _s_OnCalculate_Prev_Value = Value
        IndBuffer[bar] = SolarWinds
        ColorIndBuffer[bar] = 2.0
        if SolarWinds > 0:
            if SolarWinds > IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 4.0
            if SolarWinds < IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 3.0
        if SolarWinds < 0:
            if SolarWinds < IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 0.0
            if SolarWinds > IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Prev_Value = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Solarwinds(_MQL5Indicator):
    name = 'solarwinds'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # period of averaging
    }

