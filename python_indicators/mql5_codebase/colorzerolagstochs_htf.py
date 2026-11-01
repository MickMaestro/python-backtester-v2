"""colorzerolagstochs_htf — converted from MQL5: MQL5 Indicators/ColorZerolagStochs_HTF/colorzerolagstochs_htf.mq5

ColorZerolagStochs с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Signal HTF'}, 'levels': [], 'description': ['ColorZerolagStochs с возможностью изменения таймфрейма во входных параметрах'], 'name': 'colorzerolagstochs_htf', 'source': 'MQL5 Indicators/ColorZerolagStochs_HTF/colorzerolagstochs_htf.mq5', 'folder': 'ColorZerolagStochs_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'smoothing', 'py': 'smoothing', 'param': 'smoothing', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'Kperiod1', 'py': 'Kperiod1', 'param': 'Kperiod1', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Dperiod1', 'py': 'Dperiod1', 'param': 'Dperiod1', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Kperiod2', 'py': 'Kperiod2', 'param': 'Kperiod2', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Dperiod2', 'py': 'Dperiod2', 'param': 'Dperiod2', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'Kperiod3', 'py': 'Kperiod3', 'param': 'Kperiod3', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Dperiod3', 'py': 'Dperiod3', 'param': 'Dperiod3', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'Kperiod4', 'py': 'Kperiod4', 'param': 'Kperiod4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Dperiod4', 'py': 'Dperiod4', 'param': 'Dperiod4', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'Kperiod5', 'py': 'Kperiod5', 'param': 'Kperiod5', 'type': 'int', 'default': 89, 'label': '', 'sinput': False}, {'mql': 'Dperiod5', 'py': 'Dperiod5', 'param': 'Dperiod5', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Slowing = _input('Slowing', 3)
smoothing = _input('smoothing', 15)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
Factor1 = _input('Factor1', 0.05)
Kperiod1 = _input('Kperiod1', 8)
Dperiod1 = _input('Dperiod1', 3)
Factor2 = _input('Factor2', 0.1)
Kperiod2 = _input('Kperiod2', 21)
Dperiod2 = _input('Dperiod2', 5)
Factor3 = _input('Factor3', 0.16)
Kperiod3 = _input('Kperiod3', 34)
Dperiod3 = _input('Dperiod3', 8)
Factor4 = _input('Factor4', 0.26)
Kperiod4 = _input('Kperiod4', 55)
Dperiod4 = _input('Dperiod4', 13)
Factor5 = _input('Factor5', 0.43)
Kperiod5 = _input('Kperiod5', 89)
Dperiod5 = _input('Dperiod5', 21)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('ColorZerolagStochs', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ColorZerolagStochs', Slowing, smoothing, MA_Method, Price_field, Factor1, Kperiod1, Dperiod1, Factor2, Kperiod2, Dperiod2, Factor3, Kperiod3, Dperiod3, Factor4, Kperiod4, Dperiod4, Factor5, Kperiod5, Dperiod5)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorZerolagStochs')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorZerolagStochs', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 2, UpIndBuffer, 3, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

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

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorzerolagstochsHtf(_MQL5Indicator):
    name = 'colorzerolagstochs_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Slowing': 3,
        'smoothing': 15,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'Factor1': 0.05,
        'Kperiod1': 8,
        'Dperiod1': 3,
        'Factor2': 0.1,
        'Kperiod2': 21,
        'Dperiod2': 5,
        'Factor3': 0.16,
        'Kperiod3': 34,
        'Dperiod3': 8,
        'Factor4': 0.26,
        'Kperiod4': 55,
        'Dperiod4': 13,
        'Factor5': 0.43,
        'Kperiod5': 89,
        'Dperiod5': 21,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

