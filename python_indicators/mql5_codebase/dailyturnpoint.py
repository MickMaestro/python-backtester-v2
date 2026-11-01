"""dailyturnpoint — converted from MQL5: MQL5 Indicators/DailyTurnPoint/dailyturnpoint.mq5

Daily pivot point
Copyright: Copyright © 2012, Nikolay Kositsin; Link: http://www.forex-instruments.info; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'http://www.forex-instruments.info', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DailyTurnPoint'}, 'levels': [], 'description': ['Daily pivot point'], 'name': 'dailyturnpoint', 'source': 'MQL5 Indicators/DailyTurnPoint/dailyturnpoint.mq5', 'folder': 'DailyTurnPoint', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = 1 + _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DailyTurnPoint')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_day_high, _s_OnCalculate_day_low
    if Period() >= PERIOD_D1:
        Comment('WARNING: Invalid timeframe! Valid value < D1!')
        return 0
    if rates_total < min_rates_total:
        return 0
    yesterday_high = 0.0
    yesterday_low = 0.0
    yesterday_close = 0.0
    P = 0.0
    S = 0.0
    R = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_day_high = high[first - 1]
        _s_OnCalculate_day_low = low[first - 1]
        yesterday_high = _s_OnCalculate_day_high
        yesterday_low = _s_OnCalculate_day_low
        yesterday_close = close[first - 1]
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        TimeToStruct(time[bar], tm0)
        TimeToStruct(time[bar - 1], tm1)
        if tm1.day != tm0.day:
            yesterday_close = close[bar - 1]
            yesterday_high = _s_OnCalculate_day_high
            yesterday_low = _s_OnCalculate_day_low
            P = (yesterday_high + yesterday_low + yesterday_close) / 3
            R = yesterday_high
            S = yesterday_low
            _s_OnCalculate_day_high = high[bar]
            _s_OnCalculate_day_low = low[bar]
        _s_OnCalculate_day_high = MathMax(_s_OnCalculate_day_high, high[bar])
        _s_OnCalculate_day_low = MathMin(_s_OnCalculate_day_low, low[bar])
        IndBuffer[bar] = P + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    P = (yesterday_high + yesterday_low + yesterday_close) / 3
    R = yesterday_high
    S = yesterday_low
    Comment('Current H=', DoubleToString(R, Digits()), ', L=', DoubleToString(S, Digits()), ', HLС/3=', DoubleToString(P, Digits()), ', H-L=', DoubleToString(_fdiv(R - S, Point()), Digits()))
    return rates_total

# ---- static local variables
_s_OnCalculate_day_high = 0.0
_s_OnCalculate_day_low = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailyturnpoint(_MQL5Indicator):
    name = 'dailyturnpoint'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in points
    }

