"""NRTR_ATR_STOP — converted from MQL5: MQL5 Indicators/NRTR_ATR_STOP_HTF/NRTR_ATR_STOP.mq5

Copyright: Copyright © 2006, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [5737262], 2: [8721863], 3: [8388352], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper NRTR_ATR_STOP', 2: 'Lower NRTR_ATR_STOP', 3: 'Buy NRTR_ATR_STOP', 4: 'Sell NRTR_ATR_STOP'}, 'levels': [], 'description': [], 'name': 'NRTR_ATR_STOP', 'source': 'MQL5 Indicators/NRTR_ATR_STOP_HTF/NRTR_ATR_STOP.mq5', 'folder': 'NRTR_ATR_STOP_HTF', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Coeficient', 'py': 'Coeficient', 'param': 'Coeficient', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 20)
Coeficient = _input('Coeficient', 2)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = _int(ATR_Period + 1)
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 171)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 171)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'NRTR_ATR_STOP'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Trend_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Trend = 0
    REZ = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_Trend_ = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    Trend = _s_OnCalculate_Trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp[bar] = 0.0
        ExtMapBufferDown[bar] = 0.0
        ExtMapBufferUp1[bar] = 0.0
        ExtMapBufferDown1[bar] = 0.0
        REZ = Coeficient * ATR[bar]
        if Trend <= 0 and low[bar + 1] > ExtMapBufferDown[bar + 1]:
            ExtMapBufferUp[bar + 1] = low[bar + 1] - REZ
            Trend = 1
        if Trend >= 0 and high[bar + 1] < ExtMapBufferUp[bar + 1]:
            ExtMapBufferDown[bar + 1] = high[bar + 1] + REZ
            Trend = -1
        if Trend >= 0:
            if low[bar + 1] > (ExtMapBufferUp[bar + 1] + REZ):
                ExtMapBufferUp[bar] = low[bar + 1] - REZ
            else:
                ExtMapBufferUp[bar] = ExtMapBufferUp[bar + 1]
        if Trend <= 0:
            if high[bar + 1] < (ExtMapBufferDown[bar + 1] - REZ):
                ExtMapBufferDown[bar] = high[bar + 1] + REZ
            else:
                ExtMapBufferDown[bar] = ExtMapBufferDown[bar + 1]
        if Trend > 0 and _s_OnCalculate_Trend_ <= 0:
            ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
        if Trend < 0 and _s_OnCalculate_Trend_ >= 0:
            ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
        if bar:
            _s_OnCalculate_Trend_ = Trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Trend_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NRTRATRSTOP(_MQL5Indicator):
    name = 'NRTR_ATR_STOP'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 20,
        'Coeficient': 2,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

