"""sfx_tor_htf — converted from MQL5: MQL5 Indicators/SFX_TOR_HTF/sfx_tor_htf.mq5

SFX_TOR_HTF с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [16711935], 3: [16748574]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ATR', 2: 'StdDev', 3: 'StdDev MA'}, 'levels': [88.0, 50.0, 12.0], 'description': ['SFX_TOR_HTF с фиксированным во входных параметрах таймфреймом'], 'name': 'sfx_tor_htf', 'source': 'MQL5 Indicators/SFX_TOR_HTF/sfx_tor_htf.mq5', 'folder': 'SFX_TOR_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'ATR_period', 'py': 'ATR_period', 'param': 'ATR_period', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Std_period', 'py': 'Std_period', 'param': 'Std_period', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Std_method', 'py': 'Std_method', 'param': 'Std_method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Std_price', 'py': 'Std_price', 'param': 'Std_price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'Сдвиг ATR', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'Сдвиг Std', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'int', 'default': 0, 'label': 'Сдвиг Std Ma', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
ATR_period = _input('ATR_period', 12)
Std_period = _input('Std_period', 12)
Std_method = _input('Std_method', MODE_EMA)
Std_price = _input('Std_price', PRICE_CLOSE)
MAPeriod = _input('MAPeriod', 3)
MAType = _input('MAType', MODE_SMMA)
Shift1 = _input('Shift1', 0)  # Сдвиг ATR
Shift2 = _input('Shift2', 0)  # Сдвиг Std
Shift3 = _input('Shift3', 0)  # Сдвиг Std Ma
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('SFX_TOR', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'SFX_TOR', ATR_period, Std_period, Std_method, Std_price, MAPeriod, MAType)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SFX_TOR')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, EMPTY_VALUE, min_rates_total, Shift1)
    IndInit(1, Ind2Buffer, EMPTY_VALUE, min_rates_total, Shift2)
    IndInit(2, Ind3Buffer, EMPTY_VALUE, min_rates_total, Shift3)
    shortname = Box("")
    StringConcatenate(shortname, 'SFX_TOR', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, 2, Ind3Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf2[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb3, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf3[bar] = Arr_[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SfxTorHtf(_MQL5Indicator):
    name = 'sfx_tor_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'ATR_period': 12,
        'Std_period': 12,
        'Std_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'Std_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MAPeriod': 3,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),
        'Shift1': 0,  # Сдвиг ATR
        'Shift2': 0,  # Сдвиг Std
        'Shift3': 0,  # Сдвиг Std Ma
    }

