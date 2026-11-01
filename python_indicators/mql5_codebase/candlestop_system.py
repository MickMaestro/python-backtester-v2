"""CandleStop_System — converted from MQL5: MQL5 Indicators/CandleStop_System/CandleStop_System.mq5

Индикатор для подтягивания трейлинстопов
Copyright: Copyright © 2009, CrushD; Link: CrushD; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, CrushD', 'link': 'CrushD', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16443110], 2: [3329330], 3: [42495], 4: [9639167, 8388736, 16711680, 16748574]}, 'widths': {2: 3, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'CandleStop Channel', 2: 'CandleStop Up Line', 3: 'CandleStop Down Line', 4: 'CandleStop_Open;CandleStop_High;CandleStop_Low;CandleStop_Close'}, 'levels': [], 'description': ['Индикатор для подтягивания трейлинстопов'], 'name': 'CandleStop_System', 'source': 'MQL5 Indicators/CandleStop_System/CandleStop_System.mq5', 'folder': 'CandleStop_System', 'inputs': [{'mql': 'UpTrailPeriods', 'py': 'UpTrailPeriods', 'param': 'UpTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Период поиска для хая', 'sinput': False}, {'mql': 'UpTrailShift', 'py': 'UpTrailShift', 'param': 'UpTrailShift', 'type': 'uint', 'default': 5, 'label': 'Период сдвига для хая', 'sinput': False}, {'mql': 'DnTrailPeriods', 'py': 'DnTrailPeriods', 'param': 'DnTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Период поиска для лоу', 'sinput': False}, {'mql': 'DnTrailShift', 'py': 'DnTrailShift', 'param': 'DnTrailShift', 'type': 'uint', 'default': 5, 'label': 'Период сдвига для хая', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpTrailPeriods = _input('UpTrailPeriods', 5)  # Период поиска для хая
UpTrailShift = _input('UpTrailShift', 5)  # Период сдвига для хая
DnTrailPeriods = _input('DnTrailPeriods', 5)  # Период поиска для лоу
DnTrailShift = _input('DnTrailShift', 5)  # Период сдвига для хая
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(UpTrailPeriods + UpTrailShift, DnTrailPeriods + DnTrailShift))
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(2, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(UpIndBuffer, True)
    ArraySetAsSeries(DnIndBuffer, True)
    ArraySetAsSeries(UpLineBuffer, True)
    ArraySetAsSeries(DnLineBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CandleStop_System')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    limit = 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar + UpTrailShift, UpTrailPeriods)]
        LL = low[ArrayMinimum(low, bar + DnTrailShift, DnTrailPeriods)]
        UpIndBuffer[bar] = HH
        UpLineBuffer[bar] = UpIndBuffer[bar]
        DnIndBuffer[bar] = LL
        DnLineBuffer[bar] = DnIndBuffer[bar]
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        ExtColorBuffer[bar] = 4.0
        if close[bar] > HH:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] < LL:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleStopSystem(_MQL5Indicator):
    name = 'CandleStop_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UpTrailPeriods': 5,  # Период поиска для хая
        'UpTrailShift': 5,  # Период сдвига для хая
        'DnTrailPeriods': 5,  # Период поиска для лоу
        'DnTrailShift': 5,  # Период сдвига для хая
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

