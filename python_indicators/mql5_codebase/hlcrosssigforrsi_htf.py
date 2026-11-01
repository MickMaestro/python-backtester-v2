"""HLCrossSigForRSI_HTF — converted from MQL5: MQL5 Indicators/HLCrossSigForRSI_HTF/HLCrossSigForRSI_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [255], 2: [3329330], 3: [16711935], 4: [16760576], 5: [16711935], 6: [16760576], 7: [255], 8: [3329330]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3}, 'styles': {}, 'labels': {1: 'Sell Stop', 2: 'Buy Stop', 3: 'Sell TakeProfit', 4: 'Buy TakeProfit', 5: 'Sell Signal', 6: 'Buy Signal', 7: 'Sell Input', 8: 'Buy Input'}, 'levels': [], 'description': [], 'name': 'HLCrossSigForRSI_HTF', 'source': 'MQL5 Indicators/HLCrossSigForRSI_HTF/HLCrossSigForRSI_HTF.mq5', 'folder': 'HLCrossSigForRSI_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Supr_Period', 'py': 'Supr_Period', 'param': 'Supr_Period', 'type': 'int', 'default': 6, 'label': 'Период пробиваемого диапазона, чем больше значение, тем более поздние сигналы и реже', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 21, 'label': 'Период для Heiken Ashi variable. Служит в качестве доп. фильтра', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'int', 'default': 0, 'label': 'Максимальный риск в пипсах для расчета уровня входа исходя из уровня ближайшего MAX/MIN', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 120, 'label': 'Период АТR. Служит для расчета уровня волатильности.', 'sinput': False}, {'mql': 'Q', 'py': 'Q', 'param': 'Q', 'type': 'double', 'default': 0.7, 'label': 'Параметр для постановки Тейка. - Доля от размера Стопа. если =1, Тейк = Стопу', 'sinput': False}, {'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'int', 'default': 12, 'label': 'Период RSI. Служит в качестве доп. фильтра', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена  RSI', 'sinput': False}, {'mql': 'HLine', 'py': 'HLine', 'param': 'HLine', 'type': 'int', 'default': 60, 'label': 'Верхняя сигнальная линия стопов для RSI', 'sinput': False}, {'mql': 'LLine', 'py': 'LLine', 'param': 'LLine', 'type': 'int', 'default': 40, 'label': 'Нижняя сигнальная линия стопов для RSI', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Supr_Period = _input('Supr_Period', 6)  # Период пробиваемого диапазона, чем больше значение, тем более поздние сигналы и реже
MA_Period = _input('MA_Period', 21)  # Период для Heiken Ashi variable. Служит в качестве доп. фильтра
Risk = _input('Risk', 0)  # Максимальный риск в пипсах для расчета уровня входа исходя из уровня ближайшего MAX/MIN
ATR_Period = _input('ATR_Period', 120)  # Период АТR. Служит для расчета уровня волатильности.
Q = _input('Q', 0.7)  # Параметр для постановки Тейка. - Доля от размера Стопа. если =1, Тейк = Стопу
RSI_Period = _input('RSI_Period', 12)  # Период RSI. Служит в качестве доп. фильтра
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена  RSI
HLine = _input('HLine', 60)  # Верхняя сигнальная линия стопов для RSI
LLine = _input('LLine', 40)  # Нижняя сигнальная линия стопов для RSI
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'HLCrossSigForRSI' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'HLCrossSigForRSI', Supr_Period, MA_Period, Risk, ATR_Period, Q, RSI_Period, RSIPrice, HLine, LLine)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора HLCrossSigForRSI')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer8, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetInteger(2, PLOT_ARROW, 158)
    PlotIndexSetInteger(3, PLOT_ARROW, 158)
    PlotIndexSetInteger(4, PLOT_ARROW, 234)
    PlotIndexSetInteger(5, PLOT_ARROW, 233)
    PlotIndexSetInteger(6, PLOT_ARROW, 177)
    PlotIndexSetInteger(7, PLOT_ARROW, 177)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    shortname = Box("")
    StringConcatenate(shortname, 'HLCrossSigForRSI(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('HLCrossSigForRSI', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, ExtLineBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, ExtLineBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, ExtLineBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, ExtLineBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, ExtLineBuffer5, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, ExtLineBuffer6, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, ExtLineBuffer7, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(7, "", TimeFrame, Ind_Handle, 7, ExtLineBuffer8, time, rates_total, prev_calculated, min_rates_total):
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
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
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
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(8, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HLCrossSigForRSIHTF(_MQL5Indicator):
    name = 'HLCrossSigForRSI_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Supr_Period': 6,  # Период пробиваемого диапазона, чем больше значение, тем более поздние сигналы и реже
        'MA_Period': 21,  # Период для Heiken Ashi variable. Служит в качестве доп. фильтра
        'Risk': 0,  # Максимальный риск в пипсах для расчета уровня входа исходя из уровня ближайшего MAX/MIN
        'ATR_Period': 120,  # Период АТR. Служит для расчета уровня волатильности.
        'Q': 0.7,  # Параметр для постановки Тейка. - Доля от размера Стопа. если =1, Тейк = Стопу
        'RSI_Period': 12,  # Период RSI. Служит в качестве доп. фильтра
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена  RSI
        'HLine': 60,  # Верхняя сигнальная линия стопов для RSI
        'LLine': 40,  # Нижняя сигнальная линия стопов для RSI
    }

