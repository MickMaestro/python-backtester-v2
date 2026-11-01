"""BullsBearsEyes_Vol — converted from MQL5: MQL5 Indicators/BullsBearsEyes_Vol/BullsBearsEyes_Vol.mq5

BullsBearsEyes
Copyright: Copyright © 2007, EmeraldKing, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, EmeraldKing, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 10, 4: 1, 5: 1}, 'colors': {1: [16760576], 2: [16711680], 3: [65280, 8421376, 14381203, 2763429, 9639167], 4: [16711680], 5: [16760576]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 1, 5: 1}, 'styles': {1: 4, 2: 4, 3: 0, 4: 4, 5: 4}, 'labels': {1: 'BullsBearsEyes_Vol Max', 2: 'BullsBearsEyes_Vol Res', 3: 'BullsBearsEyes_Vol', 4: 'BullsBearsEyes_Vol Supr', 5: 'BullsBearsEyes_Vol Min'}, 'levels': [], 'description': ['BullsBearsEyes'], 'name': 'BullsBearsEyes_Vol', 'source': 'MQL5 Indicators/BullsBearsEyes_Vol/BullsBearsEyes_Vol.mq5', 'folder': 'BullsBearsEyes_Vol', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 13, 'label': 'период усреднения индикатора', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.6, 'label': 'коэффициент сглаживания индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel2', 'py': 'HighLevel2', 'param': 'HighLevel2', 'type': 'int', 'default': 25, 'label': 'уровень перекупленности 2', 'sinput': False}, {'mql': 'HighLevel1', 'py': 'HighLevel1', 'param': 'HighLevel1', 'type': 'int', 'default': 10, 'label': 'уровень перекупленности 1', 'sinput': False}, {'mql': 'LowLevel1', 'py': 'LowLevel1', 'param': 'LowLevel1', 'type': 'int', 'default': -10, 'label': 'уровень перепроданности 1', 'sinput': False}, {'mql': 'LowLevel2', 'py': 'LowLevel2', 'param': 'LowLevel2', 'type': 'int', 'default': -25, 'label': 'уровень перепроданности 2', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 13)  # период усреднения индикатора
gamma = _input('gamma', 0.6)  # коэффициент сглаживания индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel2 = _input('HighLevel2', 25)  # уровень перекупленности 2
HighLevel1 = _input('HighLevel1', 10)  # уровень перекупленности 1
LowLevel1 = _input('LowLevel1', -10)  # уровень перепроданности 1
LowLevel2 = _input('LowLevel2', -25)  # уровень перепроданности 2
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
MaxIndBuffer = Arr(0, 0.0)
MinIndBuffer = Arr(0, 0.0)
Bears_Handle = 0
Bulls_Handle = 0
min_rates_total = 0

def OnInit():
    global Bears_Handle, Bulls_Handle, min_rates_total
    min_rates_total = _int(period + 1)
    Bears_Handle = iBearsPower(None, 0, _int(period))
    if Bears_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBearsPower')
    Bulls_Handle = iBullsPower(None, 0, _int(period))
    if Bulls_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBullsPower')
    SetIndexBuffer(0, MaxIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(MaxIndBuffer, True)
    SetIndexBuffer(1, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    SetIndexBuffer(4, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(5, MinIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(MinIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'BullsBearsEyes_Vol(', period, ', ', gamma, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_L0_, _s_OnCalculate_L1_, _s_OnCalculate_L2_, _s_OnCalculate_L3_
    if (BarsCalculated(Bears_Handle) < rates_total or BarsCalculated(Bulls_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    result = 0.0
    Bears = Arr(0, 0.0)
    Bulls = Arr(0, 0.0)
    CU = 0.0
    CD = 0.0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    vol = 0.0
    limit = 0
    bar = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Bears, True)
    ArraySetAsSeries(Bulls, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    if CopyBuffer(Bears_Handle, 0, 0, to_copy, Bears) <= 0:
        return 0
    if CopyBuffer(Bulls_Handle, 0, 0, to_copy, Bulls) <= 0:
        return 0
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1.0 - gamma) * (Bears[bar] + Bulls[bar])) + (gamma * L0A)
        L1 = ((-gamma) * L0) + L0A + (gamma * L1A)
        L2 = ((-gamma) * L1) + L1A + (gamma * L2A)
        L3 = ((-gamma) * L2) + L2A + (gamma * L3A)
        CU = 0.0
        CD = 0.0
        result = 0.0
        if L0 >= L1:
            CU = L0 - L1
        else:
            CD = L1 - L0
        if L1 >= L2:
            CU += L1 - L2
        else:
            CD += L2 - L1
        if L2 >= L3:
            CU += L2 - L3
        else:
            CD += L3 - L2
        if (CU + CD) != 0:
            result = _fdiv(CU, CU + CD)
        IndBuffer[bar] = (result * 100) - 50
        if VolumeType == VOLUME_TICK:
            vol = float(tick_volume[bar])
        else:
            vol = float(volume[bar])
        IndBuffer[bar] *= vol
        MaxIndBuffer[bar] = HighLevel2 * vol
        UpIndBuffer[bar] = HighLevel1 * vol
        DnIndBuffer[bar] = LowLevel1 * vol
        MinIndBuffer[bar] = LowLevel2 * vol
        clr = _int(2.0)
        if IndBuffer[bar] > MaxIndBuffer[bar]:
            clr = _int(0.0)
        elif IndBuffer[bar] > UpIndBuffer[bar]:
            clr = _int(1.0)
        elif IndBuffer[bar] < MinIndBuffer[bar]:
            clr = _int(4.0)
        elif IndBuffer[bar] < DnIndBuffer[bar]:
            clr = _int(3.0)
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_L0_ = 0.0
_s_OnCalculate_L1_ = 0.0
_s_OnCalculate_L2_ = 0.0
_s_OnCalculate_L3_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BullsBearsEyesVol(_MQL5Indicator):
    name = 'BullsBearsEyes_Vol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 13,  # период усреднения индикатора
        'gamma': 0.6,  # коэффициент сглаживания индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel2': 25,  # уровень перекупленности 2
        'HighLevel1': 10,  # уровень перекупленности 1
        'LowLevel1': -10,  # уровень перепроданности 1
        'LowLevel2': -25,  # уровень перепроданности 2
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

