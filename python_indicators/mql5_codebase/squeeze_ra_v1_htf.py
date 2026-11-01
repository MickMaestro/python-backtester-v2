"""squeeze_ra_v1_htf — converted from MQL5: MQL5 Indicators/Squeeze_RA_V1_HTF/squeeze_ra_v1_htf.mq5

Индикатор Squeeze_RA_V1 с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 3, 2: 3, 3: 3, 4: 3, 5: 5, 6: 5}, 'colors': {1: [13434880], 2: [4678655], 3: [16748574], 4: [42495], 5: [65280], 6: [16711935]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'SqzFiredLong', 2: 'SqzFiredShort', 3: 'SqzFiredLong_Weak', 4: 'SqzFiredShort_Weak', 5: 'Squeeze_Off', 6: 'Squeeze_On'}, 'levels': [], 'description': ['Индикатор Squeeze_RA_V1 с возможностью изменения таймфрейма во входных параметрах'], 'name': 'squeeze_ra_v1_htf', 'source': 'MQL5 Indicators/Squeeze_RA_V1_HTF/squeeze_ra_v1_htf.mq5', 'folder': 'Squeeze_RA_V1_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer5 = Arr(0, 0.0)
IndBuffer6 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if not TimeFramesCheck('Squeeze_RA_V1', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'Squeeze_RA_V1' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Squeeze_RA_V1')
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Squeeze_RA_V1')
        return INIT_FAILED
    IndInit(0, IndBuffer1, EMPTY_VALUE, min_rates_total, 0)
    IndInit(1, IndBuffer2, EMPTY_VALUE, min_rates_total, 0)
    IndInit(2, IndBuffer3, EMPTY_VALUE, min_rates_total, 0)
    IndInit(3, IndBuffer4, EMPTY_VALUE, min_rates_total, 0)
    IndInit(4, IndBuffer5, EMPTY_VALUE, min_rates_total, 0)
    IndInit(5, IndBuffer6, EMPTY_VALUE, min_rates_total, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'Squeeze_RA_V1', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, IndBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, IndBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, IndBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, IndBuffer5, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, IndBuffer6, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(6, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SqueezeRaV1Htf(_MQL5Indicator):
    name = 'squeeze_ra_v1_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
    }

