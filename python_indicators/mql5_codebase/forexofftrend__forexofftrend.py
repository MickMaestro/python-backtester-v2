"""forexofftrend — converted from MQL5: MQL5 Indicators/ForexOFFTrend/forexofftrend.mq5

Copyright: Copyright © 2006, rewritten by CrazyChart; Link: http://viac.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, rewritten by CrazyChart', 'link': 'http://viac.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10025880, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Buy;Sell'}, 'levels': [], 'description': [], 'name': 'forexofftrend', 'source': 'MQL5 Indicators/ForexOFFTrend/forexofftrend.mq5', 'folder': 'ForexOFFTrend', 'inputs': [{'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'uint', 'default': 7, 'label': 'период поиска экстремумов', 'sinput': False}, {'mql': 'KPer', 'py': 'KPer', 'param': 'KPer', 'type': 'uint', 'default': 7, 'label': 'период сдвига сигнальной огибающей', 'sinput': False}, {'mql': 'Kmax', 'py': 'Kmax', 'param': 'Kmax', 'type': 'double', 'default': 50.6, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SSP = _input('SSP', 7)  # период поиска экстремумов
KPer = _input('KPer', 7)  # период сдвига сигнальной огибающей
Kmax = _input('Kmax', 50.6)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(SSP, KPer) + KPer)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ForexOFFTrend(' + _str(SSP) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - _int(MathMax(SSP, KPer)) - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        HH = High[ArrayMaximum(High, bar, SSP)]
        LL = Low[ArrayMinimum(Low, bar, SSP)]
        ExtABuffer[bar] = HH - (((HH - LL) * Kmax) / 100)
        ExtBBuffer[bar] = ExtABuffer[bar + KPer]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forexofftrend(_MQL5Indicator):
    name = 'forexofftrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SSP': 7,  # период поиска экстремумов
        'KPer': 7,  # период сдвига сигнальной огибающей
        'Kmax': 50.6,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

