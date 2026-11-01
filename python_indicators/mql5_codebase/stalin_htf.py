"""Stalin_HTF — converted from MQL5: MQL5 Indicators/Stalin_HTF/Stalin_HTF.mq5

Индикатор Stalin с возможностью изменения таймфрема во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 2, 2: 3}, 'styles': {}, 'labels': {1: 'Stalin Sell', 2: 'Stalin Buy'}, 'levels': [], 'description': ['Индикатор Stalin с возможностью изменения таймфрема во входных параметрах'], 'name': 'Stalin_HTF', 'source': 'MQL5 Indicators/Stalin_HTF/Stalin_HTF.mq5', 'folder': 'Stalin_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Fast', 'py': 'Fast', 'param': 'Fast', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Slow', 'py': 'Slow', 'param': 'Slow', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': 'RSI', 'type': 'int', 'default': 17, 'label': '', 'sinput': False}, {'mql': 'Confirm', 'py': 'Confirm', 'param': 'Confirm', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Flat', 'py': 'Flat', 'param': 'Flat', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SoundAlert', 'py': 'SoundAlert', 'param': 'SoundAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SellSymb', 'py': 'SellSymb', 'param': 'SellSymb', 'type': 'uint', 'default': 234, 'label': 'Значек продажи', 'sinput': False}, {'mql': 'BuySymb', 'py': 'BuySymb', 'param': 'BuySymb', 'type': 'uint', 'default': 233, 'label': 'Значек покупки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
MAMethod = _input('MAMethod', MODE_EMA)
MAShift = _input('MAShift', 0)
Fast = _input('Fast', 14)
Slow = _input('Slow', 21)
RSI = _input('RSI', 17)
Confirm = _input('Confirm', _int(0.0))
Flat = _input('Flat', _int(0.0))
SoundAlert = _input('SoundAlert', False)
EmailAlert = _input('EmailAlert', False)
SellSymb = _input('SellSymb', 234)  # Значек продажи
BuySymb = _input('BuySymb', 233)  # Значек покупки
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Stalin', MAMethod, MAShift, Fast, Slow, RSI, Confirm, Flat, SoundAlert, EmailAlert)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Stalin')
        return INIT_FAILED
    IndInit(0, DnBuffer, 0.0, min_rates_total, 0, SellSymb)
    IndInit(1, UpBuffer, 0.0, min_rates_total, 0, BuySymb)
    shortname = Box("")
    StringConcatenate(shortname, 'Stalin', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('Stalin', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, DnBuffer, 1, UpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift, Symb):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_ARROW, Symb)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf1[bar] = 0.0
        IndBuf2[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr1 = Arr(1, 0.0, dyn=False)
            Arr2 = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr1) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr2) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr1[0]
            IndBuf2[bar] = Arr2[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StalinHTF(_MQL5Indicator):
    name = 'Stalin_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAShift': 0,
        'Fast': 14,
        'Slow': 21,
        'RSI': 17,
        'Confirm': 0,
        'Flat': 0,
        'SoundAlert': False,
        'EmailAlert': False,
        'SellSymb': 234,  # Значек продажи
        'BuySymb': 233,  # Значек покупки
    }

