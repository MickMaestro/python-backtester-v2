"""new_fractals_lines — converted from MQL5: MQL5 Indicators/New_Fractals_Lines/new_fractals_lines.mq5

Copyright: Copyright © 2007, olyakish; Link: plutonia-dmb#yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, olyakish', 'link': 'plutonia-dmb#yandex.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [3937500], 2: [3329330]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Down Fractal', 2: 'Up Fractal'}, 'levels': [], 'description': [], 'name': 'new_fractals_lines', 'source': 'MQL5 Indicators/New_Fractals_Lines/new_fractals_lines.mq5', 'folder': 'New_Fractals_Lines', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объём', 'sinput': False}, {'mql': 'UpLabel', 'py': 'UpLabel', 'param': 'UpLabel', 'type': 'int', 'default': 164, 'label': 'Метка верхнего фрактала', 'sinput': False}, {'mql': 'DnLabel', 'py': 'DnLabel', 'param': 'DnLabel', 'type': 'int', 'default': 164, 'label': 'Метка нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объём
UpLabel = _input('UpLabel', 164)  # Метка верхнего фрактала
DnLabel = _input('DnLabel', 164)  # Метка нижнего фрактала
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0
FRA_Handle = 0

def OnInit():
    global FRA_Handle, min_rates_total
    min_rates_total = 3
    FRA_Handle = iFractals(Symbol(), PERIOD_CURRENT)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFractals')
        return INIT_FAILED
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLabel)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLabel)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'New_Fractals_Lines'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_OldFractal
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    AllHLUp = 0.0
    AllMFIUp = 0.0
    AllHLDown = 0.0
    AllMFIDown = 0.0
    UpFractal = Arr(0, 0.0)
    DnFractal = Arr(0, 0.0)
    AllVolDown = 0
    AllVolUp = 0
    Up = False
    Down = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_OldFractal = 0
    else:
        limit = rates_total - prev_calculated + min_rates_total
    to_copy = limit + 1 + min_rates_total
    if CopyBuffer(FRA_Handle, 0, 0, to_copy, UpFractal) <= 0:
        return 0
    if CopyBuffer(FRA_Handle, 1, 0, to_copy, DnFractal) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(UpFractal, True)
    ArraySetAsSeries(DnFractal, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    for bar in range(2, limit + 1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        if UpFractal[bar] and UpFractal[bar] != EMPTY_VALUE:
            Up = True
            Down = False
        if DnFractal[bar] and DnFractal[bar] != EMPTY_VALUE:
            Up = False
            Down = True
        if ((UpFractal[bar] and UpFractal[bar] != EMPTY_VALUE) and DnFractal[bar]) and DnFractal[bar] != EMPTY_VALUE:
            Up = False
            Down = False
        if (not Up) and Down:
            AllHLDown = high[bar + 2] - low[bar + 2] + high[bar + 1] - low[bar + 1] + high[bar] - low[bar] + high[bar - 1] - low[bar - 1] + high[bar - 2] - low[bar - 2]
            AllVolDown = VolSum(VolumeType, tick_volume, volume, bar)
            AllMFIDown = _fdiv(AllHLDown, AllVolDown)
            if (_s_OnCalculate_OldFractal == 1 and AllMFIDown < AllMFIUp) and AllVolDown > AllVolUp:
                DnBuffer[bar] = DnFractal[bar]
            _s_OnCalculate_OldFractal = 0
        if Up and (not Down):
            AllHLUp = high[bar + 2] - low[bar + 2] + high[bar + 1] - low[bar + 1] + high[bar] - low[bar] + high[bar - 1] - low[bar - 1] + high[bar - 2] - low[bar - 2]
            AllVolUp = VolSum(VolumeType, tick_volume, volume, bar)
            AllMFIUp = _fdiv(AllHLUp, AllVolUp)
            if (_s_OnCalculate_OldFractal == 0 and AllMFIUp < AllMFIDown) and AllVolUp > AllVolDown:
                UpBuffer[bar] = UpFractal[bar]
            _s_OnCalculate_OldFractal = 1
    return rates_total

def VolSum(VolType, Tick_Volume, Volume, index):
    Vol = 0
    if VolType == VOLUME_REAL:
        Vol = Volume[index + 2] + Volume[index + 1] + Volume[index] + Volume[index - 1] + Volume[index - 2]
    else:
        Vol = Tick_Volume[index + 2] + Tick_Volume[index + 1] + Tick_Volume[index] + Tick_Volume[index - 1] + Tick_Volume[index - 2]
    return Vol

# ---- static local variables
_s_OnCalculate_OldFractal = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NewFractalsLines(_MQL5Indicator):
    name = 'new_fractals_lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объём
        'UpLabel': 164,  # Метка верхнего фрактала
        'DnLabel': 164,  # Метка нижнего фрактала
    }

