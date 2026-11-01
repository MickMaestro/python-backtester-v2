"""AroonHornSign — converted from MQL5: MQL5 Indicators/AroonHornSign/AroonHornSign.mq5

Copyright: Copyright © 2011, tonyc2a; Link: mailto:tonyc2a@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, tonyc2a', 'link': 'mailto:tonyc2a@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [3937500], 2: [3329330]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'AroonHornSign Sell', 2: 'AroonHornSign Buy'}, 'levels': [], 'description': [], 'name': 'AroonHornSign', 'source': 'MQL5 Indicators/AroonHornSign/AroonHornSign.mq5', 'folder': 'AroonHornSign', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'uint', 'default': 9, 'label': 'период индикатора', 'sinput': False}, {'mql': 'AroonShift', 'py': 'AroonShift', 'param': 'AroonShift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 9)  # период индикатора
AroonShift = _input('AroonShift', 0)  # сдвиг индикатора по горизонтали в барах
BullsAroonBuffer = Arr(0, 0.0)
BearsAroonBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 10
    min_rates_total = _int(MathMax(AroonPeriod, ATR_Period))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, BearsAroonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, AroonPeriod)
    SetIndexBuffer(1, BullsAroonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, AroonPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'AroonHornSign(', AroonPeriod, ', ', AroonShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    trend = 0
    BULLS = 0.0
    BEARS = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
        _s_OnCalculate_trend_prev = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        barx = rates_total - bar - 1
        BULLS = NormalizeDouble(100 - (((ArrayMaximum(high, barx, AroonPeriod) - barx + 0.5) * 100) / AroonPeriod), 0)
        BEARS = NormalizeDouble(100 - (((ArrayMinimum(low, barx, AroonPeriod) - barx + 0.5) * 100) / AroonPeriod), 0)
        BullsAroonBuffer[bar] = 0.0
        BearsAroonBuffer[bar] = 0.0
        trend = _s_OnCalculate_trend_prev
        if BULLS > BEARS and BULLS >= 50:
            trend = 1
        if BULLS < BEARS and BEARS >= 50:
            trend = -1
        if _s_OnCalculate_trend_prev < 0 and trend > 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BullsAroonBuffer[bar] = low[barx] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_trend_prev > 0 and trend < 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BearsAroonBuffer[bar] = high[barx] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonHornSign(_MQL5Indicator):
    name = 'AroonHornSign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 9,  # период индикатора
        'AroonShift': 0,  # сдвиг индикатора по горизонтали в барах
    }

