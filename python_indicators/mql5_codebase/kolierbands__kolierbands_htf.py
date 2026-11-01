"""KoliErBands — converted from MQL5: MQL5 Indicators/KoliErBands_HTF/KoliErBands.mq5

Модификация индикатора Боллинджера
Copyright: Copyright 2010, KoliEr Li.; Link: http://kolier.li; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, KoliEr Li.', 'link': 'http://kolier.li', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 7, 5: 7, 6: 7, 7: 7}, 'colors': {1: [14822282], 2: [16711680], 3: [16711680], 4: [13959039], 5: [16760576], 6: [15631086], 7: [12695295]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 4, 2: 4, 3: 4}, 'labels': {1: 'KoliEr Line', 2: 'Up KoliErBands', 3: 'Dn KoliErBands', 4: 'Up KoliErBands Cloud Out', 5: 'Up KoliErBands Cloud In', 6: 'Dn KoliErBands Cloud In', 7: 'Dn KoliErBands Cloud Out'}, 'levels': [], 'description': ['Модификация индикатора Боллинджера'], 'name': 'KoliErBands', 'source': 'MQL5 Indicators/KoliErBands_HTF/KoliErBands.mq5', 'folder': 'KoliErBands_HTF', 'inputs': [{'mql': 'KB_Period', 'py': 'KB_Period', 'param': 'KB_Period', 'type': 'uint', 'default': 14, 'label': 'Peroid of KoliEr Bands', 'sinput': False}, {'mql': 'KB_Deviation', 'py': 'KB_Deviation', 'param': 'KB_Deviation', 'type': 'double', 'default': 2.01, 'label': 'Deviation Level', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KB_Period = _input('KB_Period', 14)  # Peroid of KoliEr Bands
KB_Deviation = _input('KB_Deviation', 2.01)  # Deviation Level
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
ExtLineBuffer9 = Arr(0, 0.0)
ExtLineBuffer10 = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = _int(KB_Period) + 1
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer8, INDICATOR_DATA)
    SetIndexBuffer(9, ExtLineBuffer9, INDICATOR_DATA)
    SetIndexBuffer(10, ExtLineBuffer10, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(9, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(10, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'KoliErBands(', KB_Period, ', ', DoubleToString(KB_Deviation, 3), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    sum_ = 0.0
    kb = 0.0
    val_new = 0.0
    deviation = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = first
    for bar in range(bar, rates_total):
        kb = (high[ArrayMaximum(high, rates_total - 1 - bar, KB_Period)] + low[ArrayMinimum(low, rates_total - 1 - bar, KB_Period)]) / 2
        sum_ = 0.0
        kkk = bar - _int(KB_Period) + 1
        while kkk <= bar:
            val_new = close[kkk] - kb
            sum_ += val_new * val_new
            kkk += 1
        deviation = KB_Deviation * MathSqrt(sum_ / KB_Period)
        ExtLineBuffer0[bar] = kb + dPriceShift
        ExtLineBuffer1[bar] = ExtLineBuffer0[bar] + deviation + dPriceShift
        ExtLineBuffer2[bar] = ExtLineBuffer0[bar] - deviation + dPriceShift
        ExtLineBuffer3[bar] = ExtLineBuffer0[bar] + (deviation * 100) + dPriceShift
        ExtLineBuffer4[bar] = ExtLineBuffer0[bar] + deviation + dPriceShift
        ExtLineBuffer5[bar] = ExtLineBuffer0[bar] + deviation + dPriceShift
        ExtLineBuffer6[bar] = ExtLineBuffer0[bar] + dPriceShift
        ExtLineBuffer7[bar] = ExtLineBuffer0[bar] + dPriceShift
        ExtLineBuffer8[bar] = ExtLineBuffer0[bar] - deviation + dPriceShift
        ExtLineBuffer9[bar] = ExtLineBuffer0[bar] - deviation + dPriceShift
        ExtLineBuffer10[bar] = ExtLineBuffer0[bar] - (deviation * 100) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KoliErBands(_MQL5Indicator):
    name = 'KoliErBands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KB_Period': 14,  # Peroid of KoliEr Bands
        'KB_Deviation': 2.01,  # Deviation Level
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

