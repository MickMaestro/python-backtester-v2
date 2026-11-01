"""bullsbearsvolume — converted from MQL5: MQL5 Indicators/BullsBearsVolume/bullsbearsvolume.mq5

Copyright: Shovel; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Shovel', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BUBEVO'}, 'levels': [0.0], 'description': [], 'name': 'bullsbearsvolume', 'source': 'MQL5 Indicators/BullsBearsVolume/bullsbearsvolume.mq5', 'folder': 'BullsBearsVolume', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}, {'mql': 'delta', 'py': 'delta', 'param': 'delta', 'type': 'double', 'default': 1e-05, 'label': 'delta (flat level)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 13)  # Period
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
delta = _input('delta', 1e-05)  # delta (flat level)
ExtEmaHandle = 0
ExtBullsBearsBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ExtTempBuffer = Arr(0, 0.0)
ExtVolumesBuffer = Arr(0, 0.0)

def OnInit():
    global ExtEmaHandle
    SetIndexBuffer(0, ExtBullsBearsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtTempBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtVolumesBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BullsBearsVolume(' + _str(InpPeriod) + '  delta: ' + _str(delta) + ') ')
    ExtEmaHandle = iMA(None, 0, InpPeriod, 0, MODE_EMA, PRICE_CLOSE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    period = InpPeriod
    _bear = 0.0
    _bull = 0.0
    point = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    if rates_total < InpPeriod:
        return 0
    calculated = BarsCalculated(ExtEmaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtEmaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtEmaHandle, 0, 0, to_copy, ExtTempBuffer) <= 0:
        Print('getting ExtEmaHandle is failed! Error', GetLastError())
        return 0
    if prev_calculated < InpPeriod:
        limit = InpPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        _bull = high[i] - ExtTempBuffer[i]
        _bear = low[i] - ExtTempBuffer[i]
        if _bull > 0 and _bear > 0:
            ExtBullsBearsBuffer[i] = _bull - _bear
        elif _bull < 0 and _bear < 0:
            ExtBullsBearsBuffer[i] = -(MathAbs(_bear) - MathAbs(_bull))
        else:
            ExtBullsBearsBuffer[i] = _bull + _bear
        _volume = (tick_volume[i] if (InpVolumeType == VOLUME_TICK) else volume[i])
        ExtBullsBearsBuffer[i] = ExtBullsBearsBuffer[i] * float(_volume) * point
        if MathAbs(ExtBullsBearsBuffer[i]) < delta:
            ExtBullsBearsBuffer[i] = 0.0
        if MathAbs(_bull) > MathAbs(_bear):
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bullsbearsvolume(_MQL5Indicator):
    name = 'bullsbearsvolume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 13,  # Period
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
        'delta': 1e-05,  # delta (flat level)
    }

