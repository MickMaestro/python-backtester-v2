"""hlr_histogram — converted from MQL5: MQL5 Indicators/HLR_Histogram_HTF/hlr_histogram.mq5

Hi-Lo Range Oscillator
Copyright: Copyright © 2006, Alexandre; Link: http://www.kroufr.ru/content/view/1184/124/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alexandre', 'link': 'http://www.kroufr.ru/content/view/1184/124/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [65280, 13749760, 14381203, 36095, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Hi-Lo Range Oscillator'}, 'levels': [], 'description': ['Hi-Lo Range Oscillator'], 'name': 'hlr_histogram', 'source': 'MQL5 Indicators/HLR_Histogram_HTF/hlr_histogram.mq5', 'folder': 'HLR_Histogram_HTF', 'inputs': [{'mql': 'HLR_Range', 'py': 'HLR_Range', 'param': 'HLR_Range', 'type': 'uint', 'default': 40, 'label': 'Период усреднения индикатора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HLR_Range = _input('HLR_Range', 40)  # Период усреднения индикатора
HighLevel = _input('HighLevel', 80)  # Уровень перекупленности
LowLevel = _input('LowLevel', 20)  # Уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(HLR_Range + 1)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Hi-Lo Range Oscillator Histogram(', HLR_Range, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev
    if rates_total < min_rates_total:
        return 0
    m_pr = 0.0
    HH = 0.0
    LL = 0.0
    HL = 0.0
    res = 0.0
    limit = 0
    bar = 0
    trend = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, HLR_Range)]
        LL = low[ArrayMinimum(low, bar, HLR_Range)]
        m_pr = (high[bar] + low[bar]) / 2.0
        HL = HH - LL
        if HL:
            res = _fdiv(100.0 * (m_pr - LL), HL)
        else:
            res = 50.0
        UpBuffer[bar] = res
        DnBuffer[bar] = 50.0
        clr = 2
        trend = _s_OnCalculate_trend_prev
        if res > HighLevel:
            if _s_OnCalculate_trend_prev < 0:
                clr = 0
            else:
                clr = 1
            trend = 1
        elif res < LowLevel:
            if _s_OnCalculate_trend_prev > 0:
                clr = 4
            else:
                clr = 3
            trend = -1
        ColorBuffer[bar] = clr
        if bar and trend:
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HlrHistogram(_MQL5Indicator):
    name = 'hlr_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HLR_Range': 40,  # Период усреднения индикатора
        'HighLevel': 80,  # Уровень перекупленности
        'LowLevel': 20,  # Уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

