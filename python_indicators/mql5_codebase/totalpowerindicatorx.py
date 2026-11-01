"""TotalPowerIndicatorX — converted from MQL5: MQL5 Indicators/TotalPowerIndicatorX/TotalPowerIndicatorX.mq5

Displays the concentration of bull PowerBuffer periods, bear power periods
 and total periods when either bulls or bears had prevailance.
Copyright: Copyright © 2011, www.EarnForex.com; Link: http://www.earnforex.com/; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, www.EarnForex.com', 'link': 'http://www.earnforex.com/', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2, 'indicator_minimum': -5.0, 'indicator_maximum': 105.0}, 'types': {1: 7, 2: 1}, 'colors': {1: [16748574, 16711935], 2: [13382297]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'BullsBears Cloud', 2: 'Power'}, 'levels': [100.0, 50.0, 0.0], 'description': ['Displays the concentration of bull PowerBuffer periods, bear power periods', ' and total periods when either bulls or bears had prevailance.'], 'name': 'TotalPowerIndicatorX', 'source': 'MQL5 Indicators/TotalPowerIndicatorX/TotalPowerIndicatorX.mq5', 'folder': 'TotalPowerIndicatorX', 'inputs': [{'mql': 'PowerPeriod', 'py': 'PowerPeriod', 'param': 'PowerPeriod', 'type': 'int', 'default': 10, 'label': 'период индикатора', 'sinput': False}, {'mql': 'LookbackPeriod', 'py': 'LookbackPeriod', 'param': 'LookbackPeriod', 'type': 'int', 'default': 45, 'label': 'период сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PowerPeriod = _input('PowerPeriod', 10)  # период индикатора
LookbackPeriod = _input('LookbackPeriod', 45)  # период сглаживания
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
PowerBuffer = Arr(0, 0.0)
min_rates_total = 0
Bulls_Handle = 0
Bears_Handle = 0

def OnInit():
    global Bears_Handle, Bulls_Handle, min_rates_total
    min_rates_total = LookbackPeriod + PowerPeriod
    Bulls_Handle = iBullsPower(None, 0, PowerPeriod)
    if Bulls_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Bulls')
        return INIT_FAILED
    Bears_Handle = iBearsPower(None, 0, PowerPeriod)
    if Bears_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Bears')
        return INIT_FAILED
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(2, PowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer, True)
    ArraySetAsSeries(BearsBuffer, True)
    ArraySetAsSeries(PowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Total Power Indicator(', PowerPeriod, ', ', LookbackPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Bulls_Handle) < rates_total or BarsCalculated(Bears_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    bearscount = 0
    bullscount = 0
    BULLS = Arr(0, 0.0)
    BEARS = Arr(0, 0.0)
    ArraySetAsSeries(BULLS, True)
    ArraySetAsSeries(BEARS, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + min_rates_total + 1
    if CopyBuffer(Bulls_Handle, 0, 0, to_copy, BULLS) <= 0:
        return 0
    if CopyBuffer(Bears_Handle, 0, 0, to_copy, BEARS) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bearscount = 0
        bullscount = 0
        for kkk in range(LookbackPeriod - 1, 0 - 1, -1):
            if BULLS[bar + kkk] > 0:
                bullscount += 1
            if BEARS[bar + kkk] < 0:
                bearscount += 1
        PowerBuffer[bar] = MathMax(0, MathMin(100, _idiv(2 * MathAbs(bullscount - bearscount) * 100, LookbackPeriod)))
        BullsBuffer[bar] = MathMax(0, MathMin(100, (_idiv(bullscount * 100, LookbackPeriod) - 50) * 2))
        BearsBuffer[bar] = MathMax(0, MathMin(100, (_idiv(bearscount * 100, LookbackPeriod) - 50) * 2))
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TotalPowerIndicatorX(_MQL5Indicator):
    name = 'TotalPowerIndicatorX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PowerPeriod': 10,  # период индикатора
        'LookbackPeriod': 45,  # период сглаживания
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }
    y_range = (-5.0, 105.0)

