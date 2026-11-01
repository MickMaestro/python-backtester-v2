"""wasd_fr — converted from MQL5: MQL5 Indicators/WASD_FR/wasd_fr.mq5

Фракталы строятся по 3 предыдущим барам (они не перерисовываются т.к. текущий бар не участвует в расчете)
Copyright: Copyright © 2015, WASD; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, WASD', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': ['Фракталы строятся по 3 предыдущим барам (они не перерисовываются т.к. текущий бар не участвует в расчете)'], 'name': 'wasd_fr', 'source': 'MQL5 Indicators/WASD_FR/wasd_fr.mq5', 'folder': 'WASD_FR', 'inputs': [{'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 217, 'label': 'Метка верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 218, 'label': 'Метка нижнего фрактала', 'sinput': False}, {'mql': 'Range', 'py': 'Range', 'param': 'Range', 'type': 'double', 'default': 0.1, 'label': 'Отступ фрактала от свечи в значениях ATR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpLable = _input('UpLable', 217)  # Метка верхнего фрактала
DnLable = _input('DnLable', 218)  # Метка нижнего фрактала
Range = _input('Range', 0.1)  # Отступ фрактала от свечи в значениях ATR
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 4)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'WASD_FR'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + 2
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    for bar in range(2, limit + 1):
        UpBuffer[bar + 1] = EMPTY_VALUE
        DnBuffer[bar + 1] = EMPTY_VALUE
        if low[bar + 1] < low[bar] and low[bar + 1] < low[bar + 2]:
            DnBuffer[bar + 1] = low[bar + 1] - (ATR[bar] * Range)
        if high[bar + 1] > high[bar] and high[bar + 1] > high[bar + 2]:
            UpBuffer[bar + 1] = high[bar + 1] + (ATR[bar] * Range)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WasdFr(_MQL5Indicator):
    name = 'wasd_fr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'UpLable': 217,  # Метка верхнего фрактала
        'DnLable': 218,  # Метка нижнего фрактала
        'Range': 0.1,  # Отступ фрактала от свечи в значениях ATR
    }

