"""digitalf-t01 — converted from MQL5: MQL5 Indicators/DigitalF-T01_HTF/digitalf-t01.mq5

Copyright: Copyright © 2006, XXX; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, XXX', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [13382297], 2: [255], 3: [10025880, 11823615]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DigitalF-T01', 2: 'Trigger'}, 'levels': [], 'description': [], 'name': 'digitalf-t01', 'source': 'MQL5 Indicators/DigitalF-T01_HTF/digitalf-t01.mq5', 'folder': 'DigitalF-T01_HTF', 'inputs': [{'mql': 'halfchanel', 'py': 'halfchanel', 'param': 'halfchanel', 'type': 'uint', 'default': 25, 'label': 'Коэффициент срабатывания тригера', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
halfchanel = _input('halfchanel', 25)  # Коэффициент срабатывания тригера
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
DigBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
dHalfchanel = 0.0
min_rates_total = 0

def OnInit():
    global dHalfchanel, min_rates_total
    min_rates_total = 24
    sh = _int(MathRound(_idiv(60 * ((23 * 60) + 59), PeriodSeconds())) + 1)
    min_rates_total = MathMax(min_rates_total, sh)
    dHalfchanel = halfchanel * Point()
    SetIndexBuffer(0, DigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'DigitalF-T01(', halfchanel, ', ', EnumToString(IPC, 'Applied_price_'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 24
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        DigBuffer[bar] = (0.2447098565978 * PriceSeries(IPC, bar, open, low, high, close)) + (0.2313977400697 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.2061379694732 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.1716623034064 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.131469079036 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.0895038754956 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.0496009165125 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.01502270569607 * PriceSeries(IPC, bar - 7, open, low, high, close)) - (0.0118803373443 * PriceSeries(IPC, bar - 8, open, low, high, close)) - (0.02989873856137 * PriceSeries(IPC, bar - 9, open, low, high, close)) - (0.038989671049 * PriceSeries(IPC, bar - 10, open, low, high, close)) - (0.0401411362639 * PriceSeries(IPC, bar - 11, open, low, high, close)) - (0.035119680858 * PriceSeries(IPC, bar - 12, open, low, high, close)) - (0.02611613850342 * PriceSeries(IPC, bar - 13, open, low, high, close)) - (0.01539056955666 * PriceSeries(IPC, bar - 14, open, low, high, close)) - (0.00495353651394 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.00368588764825 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.00963614049782 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.01265138888314 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.01307496106868 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.01169702291063 * PriceSeries(IPC, bar - 20, open, low, high, close)) + (0.00974841844086 * PriceSeries(IPC, bar - 21, open, low, high, close)) + (0.00898900012545 * PriceSeries(IPC, bar - 22, open, low, high, close)) - (0.00649745721156 * PriceSeries(IPC, bar - 23, open, low, high, close))
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        per = _int(MathRound(_idiv(60 * ((tm.hour * 60) + tm.min), PeriodSeconds())) + 1)
        barX = bar - per
        if DigBuffer[bar] >= close[barX]:
            TriggerBuffer[bar] = close[barX] + dHalfchanel
        if DigBuffer[bar] < close[barX]:
            TriggerBuffer[bar] = close[barX] - dHalfchanel
        UpBuffer[bar] = DigBuffer[bar]
        DnBuffer[bar] = TriggerBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DigitalfT01(_MQL5Indicator):
    name = 'digitalf-t01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'halfchanel': 25,  # Коэффициент срабатывания тригера
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

