"""donchian_fibo_clouds_htf — converted from MQL5: MQL5 Indicators/Donchian_Fibo_Clouds_HTF/donchian_fibo_clouds_htf.mq5

Donchian_Fibo_Clouds с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 0}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7}, 'colors': {1: [16748574], 2: [16760576], 3: [16776960], 4: [65535], 5: [55295], 6: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Fibo 1.000', 2: 'Fibo 0.786', 3: 'Fibo 0.618', 4: 'Fibo 0.500', 5: 'Fibo 0.382', 6: 'Fibo 0.214'}, 'levels': [], 'description': ['Donchian_Fibo_Clouds с возможностью изменения таймфрейма во входных параметрах'], 'name': 'donchian_fibo_clouds_htf', 'source': 'MQL5 Indicators/Donchian_Fibo_Clouds_HTF/donchian_fibo_clouds_htf.mq5', 'folder': 'Donchian_Fibo_Clouds_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'FiboPeriod', 'py': 'FiboPeriod', 'param': 'FiboPeriod', 'type': 'uint', 'default': 72, 'label': 'Period of averaging', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Type of extreme points', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 0.786, 'label': '', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 0.382, 'label': '', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.214, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_Extrem
HIGH_LOW = 0
HIGH_LOW_OPEN = 1
HIGH_LOW_CLOSE = 2
OPEN_HIGH_LOW = 3
CLOSE_HIGH_LOW = 4
_enum('Applied_Extrem', {0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
FiboPeriod = _input('FiboPeriod', 72)  # Period of averaging
Extremes = _input('Extremes', HIGH_LOW)  # Type of extreme points
Margins = _input('Margins', -2)
Level1 = _input('Level1', 0.786)
Level2 = _input('Level2', 0.618)
Level3 = _input('Level3', 0.5)
Level4 = _input('Level4', 0.382)
Level5 = _input('Level5', 0.214)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
Ind_Handle = 0

class CIndBuffers(MqlObject):
    _q_fields = ('m_UpBuffer', 'm_DnBuffer')
    def __init__(self, *args):
        self.m_UpBuffer = Arr(0, 0.0)
        self.m_DnBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Donchian_Fibo_Clouds', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Donchian_Fibo_Clouds', FiboPeriod, Extremes, Margins, Level1, Level2, Level3, Level4, Level5, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Donchian_Fibo_Clouds')
        return INIT_FAILED
    for numb in range(0, 6):
        count = numb * 2
        SetIndexBuffer(count, Ind[numb].m_UpBuffer, INDICATOR_DATA)
        SetIndexBuffer(count + 1, Ind[numb].m_DnBuffer, INDICATOR_DATA)
        PlotIndexSetInteger(numb, PLOT_SHIFT, Shift)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        ArraySetAsSeries(Ind[numb].m_UpBuffer, True)
        ArraySetAsSeries(Ind[numb].m_DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Donchian_Fibo_Clouds', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    for numb in range(0, 6):
        if not CountIndicator(0, "", TimeFrame, Ind_Handle, numb * 2, Ind[numb].m_UpBuffer, (numb * 2) + 1, Ind[numb].m_DnBuffer, time, rates_total, prev_calculated, min_rates_total):
            return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            UpArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = UpArr[0]
            DnIndBuf[bar] = DnArr[0]
        else:
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- global variables initialised from expressions
Ind = Arr(6, 0, dyn=False, factory=CIndBuffers)

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(6, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianFiboCloudsHtf(_MQL5Indicator):
    name = 'donchian_fibo_clouds_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'FiboPeriod': 72,  # Period of averaging
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Type of extreme points
        'Margins': -2,
        'Level1': 0.786,
        'Level2': 0.618,
        'Level3': 0.5,
        'Level4': 0.382,
        'Level5': 0.214,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

