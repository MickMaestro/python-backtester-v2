"""hlr — converted from MQL5: MQL5 Indicators/HLR_HTF/hlr.mq5

Hi-Lo Range Oscillator
Copyright: Copyright © 2006, Alexandre; Link: http://www.kroufr.ru/content/view/1184/124/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alexandre', 'link': 'http://www.kroufr.ru/content/view/1184/124/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Hi-Lo Range Oscillator'}, 'levels': [80.0, 50.0, 20.0], 'description': ['Hi-Lo Range Oscillator'], 'name': 'hlr', 'source': 'MQL5 Indicators/HLR_HTF/hlr.mq5', 'folder': 'HLR_HTF', 'inputs': [{'mql': 'HLR_Range', 'py': 'HLR_Range', 'param': 'HLR_Range', 'type': 'uint', 'default': 40, 'label': 'Период усреднения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HLR_Range = _input('HLR_Range', 40)  # Период усреднения индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HLRBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(HLR_Range + 1)
    SetIndexBuffer(0, HLRBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(HLRBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Hi-Lo Range Oscillator(', HLR_Range, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    m_pr = 0.0
    HH = 0.0
    LL = 0.0
    HL = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
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
            HLRBuffer[bar] = _fdiv(100.0 * (m_pr - LL), HL)
        else:
            HLRBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hlr(_MQL5Indicator):
    name = 'hlr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HLR_Range': 40,  # Период усреднения индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

