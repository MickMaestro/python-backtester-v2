"""TASSKlT_HTF — converted from MQL5: MQL5 Indicators/TASSKlT_HTF/TASSKlT_HTF.mq5

TASSKlT с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.70

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.70', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 11, 2: 5, 3: 5, 4: 1}, 'colors': {1: [16711935, 3329330], 2: [16711935], 3: [65280], 4: [36095]}, 'widths': {1: 4, 2: 2, 3: 2, 4: 2}, 'styles': {4: 0}, 'labels': {1: 'TASSKlT Dn', 2: 'TASSKlT Sell', 3: 'TASSKlT Buy', 4: 'TASSKlT End'}, 'levels': [], 'description': ['TASSKlT с фиксированным во входных параметрах таймфреймом'], 'name': 'TASSKlT_HTF', 'source': 'MQL5 Indicators/TASSKlT_HTF/TASSKlT_HTF.mq5', 'folder': 'TASSKlT_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'ADXperiod1', 'py': 'ADXperiod1', 'param': 'ADXperiod1', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ADXperiod2', 'py': 'ADXperiod2', 'param': 'ADXperiod2', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ADXperiod3', 'py': 'ADXperiod3', 'param': 'ADXperiod3', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
ADXperiod1 = _input('ADXperiod1', 10)
ADXperiod2 = _input('ADXperiod2', 14)
ADXperiod3 = _input('ADXperiod3', 20)
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
Ind4Buffer = Arr(0, 0.0)
Ind5Buffer = Arr(0, 0.0)
Ind6Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('TASSKlT', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, '::Indicators\\TASSKlT', ADXperiod1, ADXperiod2, ADXperiod3)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора TASSKlT')
        return INIT_FAILED
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ind2Buffer, True)
    SetIndexBuffer(2, Ind3Buffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(Ind3Buffer, True)
    SetIndexBuffer(3, Ind4Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind4Buffer, True)
    SetIndexBuffer(4, Ind5Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind5Buffer, True)
    SetIndexBuffer(5, Ind6Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind6Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'TASSKlT', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Ind1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, Ind3Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, Ind4Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, Ind5Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, Ind6Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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


class TASSKlTHTF(_MQL5Indicator):
    name = 'TASSKlT_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'ADXperiod1': 10,
        'ADXperiod2': 14,
        'ADXperiod3': 20,
    }

