"""ParabolicUsMoving — converted from MQL5: MQL5 Indicators/ParabolicUsMoving/ParabolicUsMoving.mq5

Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16760576, 16711935], 2: [16711935], 3: [16748574], 4: [16711935], 5: [16748574]}, 'widths': {2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {}, 'labels': {1: 'Signal HTF', 2: 'Lower Parabolic', 3: 'Upper Parabolic', 4: 'Parabolic Sell', 5: 'Parabolic Buy'}, 'levels': [], 'description': [], 'name': 'ParabolicUsMoving', 'source': 'MQL5 Indicators/ParabolicUsMoving/ParabolicUsMoving.mq5', 'folder': 'ParabolicUsMoving', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'StepH_', 'py': 'StepH_', 'param': 'StepH_', 'type': 'double', 'default': 0.02, 'label': 'Шаг для верхних точек', 'sinput': False}, {'mql': 'MaximumH', 'py': 'MaximumH', 'param': 'MaximumH', 'type': 'double', 'default': 0.5, 'label': 'Максимум для верхних точек', 'sinput': False}, {'mql': 'StepL_', 'py': 'StepL_', 'param': 'StepL_', 'type': 'double', 'default': 0.02, 'label': 'Шаг для нижних точек', 'sinput': False}, {'mql': 'MaximumL', 'py': 'MaximumL', 'param': 'MaximumL', 'type': 'double', 'default': 0.5, 'label': 'Максимум для нижних точек', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
StepH_ = _input('StepH_', 0.02)  # Шаг для верхних точек
MaximumH = _input('MaximumH', 0.5)  # Максимум для верхних точек
StepL_ = _input('StepL_', 0.02)  # Шаг для нижних точек
MaximumL = _input('MaximumL', 0.5)  # Максимум для нижних точек
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpSarBuffer = Arr(0, 0.0)
DnSarBuffer = Arr(0, 0.0)
SarBuffer = Arr(0, 0.0)
LineBuffer = Arr(0, 0.0)
dirlong_ = False
first_ = False
ep_ = 0.0
start_ = 0.0
last_high_ = 0.0
last_low_ = 0.0
prev_sar_ = 0.0
StepH = 0.0
StepL = 0.0
MA_Handle = 0
min_rates_total = 0

def OnInit():
    global MA_Handle, StepH, StepL, min_rates_total
    min_rates_total = MAPeriod + 2
    StepH = MathMin(StepH_, MaximumH)
    StepL = MathMin(StepL_, MaximumL)
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, SarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, LineBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, DnSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 158)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ParabolicUsMoving')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global dirlong_, ep_, first_, last_high_, last_low_, prev_sar_, start_
    if rates_total < min_rates_total or BarsCalculated(MA_Handle) < rates_total:
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
    to_copy = 0
    dirlong = False
    first = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        gfirst = min_rates_total
        to_copy = rates_total - gfirst + 1
        first_ = False
        dirlong_ = False
        last_high_ = 0.0
        last_low_ = 999999999.0
        ep_ = PriceSeries(MAPrice, min_rates_total - 1, open, low, high, close)
        prev_sar_ = ep_
        start_ = 0.0
    else:
        gfirst = prev_calculated - 1
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, LineBuffer) <= 0:
        return 0
    ep = ep_
    start = start_
    last_high = last_high_
    last_low = last_low_
    dirlong = dirlong_
    first = first_
    prev_sar = prev_sar_
    bar = gfirst
    for bar in range(bar, rates_total):
        price_low = PriceSeries(MAPrice, bar, open, low, high, close)
        price_high = PriceSeries(MAPrice, bar, open, low, high, close)
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
        SarBuffer[bar] = sar
        DnSarBuffer[bar] = EMPTY_VALUE
        UpSarBuffer[bar] = EMPTY_VALUE
        if PriceSeries(MAPrice, bar, open, low, high, close) < sar:
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


class ParabolicUsMoving(_MQL5Indicator):
    name = 'ParabolicUsMoving'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'StepH_': 0.02,  # Шаг для верхних точек
        'MaximumH': 0.5,  # Максимум для верхних точек
        'StepL_': 0.02,  # Шаг для нижних точек
        'MaximumL': 0.5,  # Максимум для нижних точек
    }

