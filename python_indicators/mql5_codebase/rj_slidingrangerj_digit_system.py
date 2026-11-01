"""Rj_SlidingRangeRj_Digit_System — converted from MQL5: MQL5 Indicators/Rj_SlidingRangeRj_Digit_System/Rj_SlidingRangeRj_Digit_System.mq5

Copyright: Copyright © 2011,RJ Rjabkov Alexander; Link: rj-a@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011,RJ Rjabkov Alexander', 'link': 'rj-a@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16443110], 2: [3329330], 3: [255], 4: [9639167, 8388736, 8421376, 13749760]}, 'widths': {2: 3, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'Rj_SlidingRangeRj_Digit Channel', 2: 'Rj_SlidingRangeRj_Digit Up Line', 3: 'Rj_SlidingRangeRj_Digit Down Line', 4: 'Rj_SlidingRangeRj_Digit_Open;Rj_SlidingRangeRj_Digit_High;Rj_SlidingRangeRj_Digit_Low;Rj_SlidingRangeRj_Digit_Close'}, 'levels': [], 'description': [], 'name': 'Rj_SlidingRangeRj_Digit_System', 'source': 'MQL5 Indicators/Rj_SlidingRangeRj_Digit_System/Rj_SlidingRangeRj_Digit_System.mq5', 'folder': 'Rj_SlidingRangeRj_Digit_System', 'inputs': [{'mql': 'UpCalcPeriodRange', 'py': 'UpCalcPeriodRange', 'param': 'UpCalcPeriodRange', 'type': 'uint', 'default': 5, 'label': 'Период поиска для хая', 'sinput': False}, {'mql': 'UpCalcPeriodShift', 'py': 'UpCalcPeriodShift', 'param': 'UpCalcPeriodShift', 'type': 'uint', 'default': 0, 'label': 'Период сдвига для хая', 'sinput': False}, {'mql': 'UpDigit', 'py': 'UpDigit', 'param': 'UpDigit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления для хая', 'sinput': False}, {'mql': 'DnCalcPeriodRange', 'py': 'DnCalcPeriodRange', 'param': 'DnCalcPeriodRange', 'type': 'uint', 'default': 5, 'label': 'Период поиска для лоу', 'sinput': False}, {'mql': 'DnCalcPeriodShift', 'py': 'DnCalcPeriodShift', 'param': 'DnCalcPeriodShift', 'type': 'uint', 'default': 0, 'label': 'Период сдвига для лоу', 'sinput': False}, {'mql': 'DnDigit', 'py': 'DnDigit', 'param': 'DnDigit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления для лоу', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpCalcPeriodRange = _input('UpCalcPeriodRange', 5)  # Период поиска для хая
UpCalcPeriodShift = _input('UpCalcPeriodShift', 0)  # Период сдвига для хая
UpDigit = _input('UpDigit', 2)  # количество разрядов округления для хая
DnCalcPeriodRange = _input('DnCalcPeriodRange', 5)  # Период поиска для лоу
DnCalcPeriodShift = _input('DnCalcPeriodShift', 0)  # Период сдвига для лоу
DnDigit = _input('DnDigit', 2)  # количество разрядов округления для лоу
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
UpPointPow10 = 0.0
DnPointPow10 = 0.0
min_rates_total = 0

def OnInit():
    global DnPointPow10, UpPointPow10, min_rates_total
    min_rates_total = _int(MathMax(UpCalcPeriodRange + UpCalcPeriodShift, DnCalcPeriodRange + DnCalcPeriodShift)) + 1
    UpPointPow10 = Point() * MathPow(10, UpDigit)
    DnPointPow10 = Point() * MathPow(10, DnDigit)
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
    shortname = Box("")
    StringConcatenate(shortname, 'Rj_SlidingRangeRj_Digit_System(', UpCalcPeriodRange, ',', UpCalcPeriodShift, ',', DnCalcPeriodRange, ',', DnCalcPeriodShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    iii = 0
    end = 0
    b = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        iii = bar + _int(UpCalcPeriodRange + UpCalcPeriodShift) - 1
        b = 0.0
        end = bar + _int(UpCalcPeriodShift)
        while iii >= end:
            b += high[ArrayMaximum(high, iii, UpCalcPeriodRange)]
            iii -= 1
        b = b / UpCalcPeriodRange
        UpIndBuffer[bar] = UpPointPow10 * MathRound(_fdiv(b, UpPointPow10))
        UpLineBuffer[bar] = UpIndBuffer[bar]
        iii = bar + _int(DnCalcPeriodRange + DnCalcPeriodShift) - 1
        b = 0.0
        end = bar + _int(DnCalcPeriodShift)
        while iii >= end:
            b += low[ArrayMinimum(low, iii, DnCalcPeriodRange)]
            iii -= 1
        b = b / DnCalcPeriodRange
        DnIndBuffer[bar] = DnPointPow10 * MathRound(_fdiv(b, DnPointPow10))
        DnLineBuffer[bar] = DnIndBuffer[bar]
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        ExtColorBuffer[bar] = 4.0
        if close[bar] > UpLineBuffer[bar]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] < DnLineBuffer[bar]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RjSlidingRangeRjDigitSystem(_MQL5Indicator):
    name = 'Rj_SlidingRangeRj_Digit_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UpCalcPeriodRange': 5,  # Период поиска для хая
        'UpCalcPeriodShift': 0,  # Период сдвига для хая
        'UpDigit': 2,  # количество разрядов округления для хая
        'DnCalcPeriodRange': 5,  # Период поиска для лоу
        'DnCalcPeriodShift': 0,  # Период сдвига для лоу
        'DnDigit': 2,  # количество разрядов округления для лоу
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

