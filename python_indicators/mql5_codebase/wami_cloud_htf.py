"""WAMI_Cloud_HTF — converted from MQL5: MQL5 Indicators/WAMI_Cloud_HTF/WAMI_Cloud_HTF.mq5

WAMI с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16760576, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Signal HTF'}, 'levels': [0.0], 'description': ['WAMI с возможностью изменения таймфрейма во входных параметрах'], 'name': 'WAMI_Cloud_HTF', 'source': 'MQL5 Indicators/WAMI_Cloud_HTF/WAMI_Cloud_HTF.mq5', 'folder': 'WAMI_Cloud_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 4, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethodMA1', 'py': 'InpMethodMA1', 'param': 'InpMethodMA1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 13, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethodMA2', 'py': 'InpMethodMA2', 'param': 'InpMethodMA2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpPeriodMA3', 'py': 'InpPeriodMA3', 'param': 'InpPeriodMA3', 'type': 'uint', 'default': 13, 'label': 'Third MA period', 'sinput': False}, {'mql': 'InpMethodMA3', 'py': 'InpMethodMA3', 'param': 'InpMethodMA3', 'type': 'int', 'default': 0, 'label': 'Third MA method', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 4, 'label': 'Signal MA period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 0, 'label': 'Signal MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
InpPeriodMA1 = _input('InpPeriodMA1', 4)  # First MA period
InpMethodMA1 = _input('InpMethodMA1', MODE_SMA)  # First MA method
InpPeriodMA2 = _input('InpPeriodMA2', 13)  # Second MA period
InpMethodMA2 = _input('InpMethodMA2', MODE_SMA)  # Second MA method
InpPeriodMA3 = _input('InpPeriodMA3', 13)  # Third MA period
InpMethodMA3 = _input('InpMethodMA3', MODE_SMA)  # Third MA method
InpPeriodSig = _input('InpPeriodSig', 4)  # Signal MA period
InpMethodSig = _input('InpMethodSig', MODE_SMA)  # Signal MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('WAMI', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'WAMI', InpPeriodMA1, InpMethodMA1, InpPeriodMA2, InpMethodMA2, InpPeriodMA3, InpMethodMA3, InpPeriodSig, InpMethodSig, InpAppliedPrice)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора WAMI')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'WAMI', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpIndBuffer, 1, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
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


class WAMICloudHTF(_MQL5Indicator):
    name = 'WAMI_Cloud_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'InpPeriodMA1': 4,  # First MA period
        'InpMethodMA1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpPeriodMA2': 13,  # Second MA period
        'InpMethodMA2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
        'InpPeriodMA3': 13,  # Third MA period
        'InpMethodMA3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Third MA method
        'InpPeriodSig': 4,  # Signal MA period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

