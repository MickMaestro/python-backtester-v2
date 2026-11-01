"""ColorParabolic — converted from MQL5: MQL5 Indicators/ColorParabolic_HTF/ColorParabolic.mq5

Copyright: Copyright © 2011, Nikolay Kositsin + lukas1; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin + lukas1', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711935], 2: [16748574], 3: [16711935], 4: [16748574]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower Parabolic', 2: 'Upper Parabolic', 3: 'Parabolic Sell', 4: 'Parabolic Buy'}, 'levels': [], 'description': [], 'name': 'ColorParabolic', 'source': 'MQL5 Indicators/ColorParabolic_HTF/ColorParabolic.mq5', 'folder': 'ColorParabolic_HTF', 'inputs': [{'mql': 'StepH_', 'py': 'StepH_', 'param': 'StepH_', 'type': 'double', 'default': 0.02, 'label': 'Шаг для верхних точек', 'sinput': False}, {'mql': 'MaximumH', 'py': 'MaximumH', 'param': 'MaximumH', 'type': 'double', 'default': 0.5, 'label': 'Максимум для верхних точек', 'sinput': False}, {'mql': 'StepL_', 'py': 'StepL_', 'param': 'StepL_', 'type': 'double', 'default': 0.02, 'label': 'Шаг для нижних точек', 'sinput': False}, {'mql': 'MaximumL', 'py': 'MaximumL', 'param': 'MaximumL', 'type': 'double', 'default': 0.5, 'label': 'Максимум для нижних точек', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StepH_ = _input('StepH_', 0.02)  # Шаг для верхних точек
MaximumH = _input('MaximumH', 0.5)  # Максимум для верхних точек
StepL_ = _input('StepL_', 0.02)  # Шаг для нижних точек
MaximumL = _input('MaximumL', 0.5)  # Максимум для нижних точек
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpSarBuffer = Arr(0, 0.0)
DnSarBuffer = Arr(0, 0.0)
dirlong_ = False
first_ = False
ep_ = 0.0
start_ = 0.0
last_high_ = 0.0
last_low_ = 0.0
prev_sar_ = 0.0
StepH = 0.0
StepL = 0.0
min_rates_total = 0

def OnInit():
    global StepH, StepL, min_rates_total
    min_rates_total = 2
    StepH = MathMin(StepH_, MaximumH)
    StepL = MathMin(StepL_, MaximumL)
    SetIndexBuffer(0, UpSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DnSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Parabolic')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global dirlong_, ep_, first_, last_high_, last_low_, prev_sar_, start_
    if rates_total < min_rates_total:
        return 0
    price_low = 0.0
    price_high = 0.0
    sar = 0.0
    ep = 0.0
    start = 0.0
    last_high = 0.0
    last_low = 0.0
    prev_sar = 0.0
    gfirst = 0
    bar = 0
    dirlong = False
    first = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        gfirst = begin + min_rates_total
        first_ = False
        dirlong_ = False
        last_high_ = 0.0
        last_low_ = 999999999.0
        ep_ = price[min_rates_total - 1]
        prev_sar_ = ep_
        start_ = 0.0
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + min_rates_total)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin + min_rates_total)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, begin + min_rates_total)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, begin + min_rates_total)
    else:
        gfirst = prev_calculated - 1
    ep = ep_
    start = start_
    last_high = last_high_
    last_low = last_low_
    dirlong = dirlong_
    first = first_
    prev_sar = prev_sar_
    bar = gfirst
    for bar in range(bar, rates_total):
        price_low = price[bar]
        price_high = price[bar]
        sar = prev_sar + (start * (ep - prev_sar))
        if dirlong:
            if ep < price_high and (start + StepL) <= MaximumL:
                start += StepL
            if sar >= price_low:
                start = StepL
                dirlong = False
                ep = price_low
                last_low = price_low
                if price_high < last_high:
                    sar = last_high
                else:
                    sar = price_high
            else:
                if ep < price_low and (start + StepL) <= MaximumL:
                    start += StepL
                if ep < price_high:
                    last_high = price_high
                    ep = price_high
        else:
            if ep > price_low and (start + StepH) <= MaximumH:
                start += StepH
            if sar <= price_high:
                start = StepH
                dirlong = True
                ep = price_high
                last_high = price_high
                if price_low > last_low:
                    sar = last_low
                else:
                    sar = price_low
            else:
                if ep > price_high and (start + StepH) <= MaximumH:
                    start += StepH
                if ep > price_low:
                    last_low = price_low
                    ep = price_low
        DnSarBuffer[bar] = EMPTY_VALUE
        UpSarBuffer[bar] = EMPTY_VALUE
        if price[bar] < sar:
            UpSarBuffer[bar] = sar
        else:
            DnSarBuffer[bar] = sar
        if bar == (rates_total - 2):
            ep_ = ep
            start_ = start
            last_high_ = last_high
            last_low_ = last_low
            dirlong_ = dirlong
            first_ = first
            prev_sar_ = sar
        if bar < (rates_total - 1):
            prev_sar = sar
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        gfirst += 1
    bar = gfirst
    for bar in range(bar, rates_total):
        BuyBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        if UpSarBuffer[bar - 1] == EMPTY_VALUE and UpSarBuffer[bar] != EMPTY_VALUE:
            SellBuffer[bar] = UpSarBuffer[bar]
        if DnSarBuffer[bar - 1] == EMPTY_VALUE and DnSarBuffer[bar] != EMPTY_VALUE:
            BuyBuffer[bar] = DnSarBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorParabolic(_MQL5Indicator):
    name = 'ColorParabolic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StepH_': 0.02,  # Шаг для верхних точек
        'MaximumH': 0.5,  # Максимум для верхних точек
        'StepL_': 0.02,  # Шаг для нижних точек
        'MaximumL': 0.5,  # Максимум для нижних точек
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

