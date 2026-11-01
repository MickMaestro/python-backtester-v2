"""AdaptiveRenko_Cld — converted from MQL5: MQL5 Indicators/AdaptiveRenko_Cld_HTF/AdaptiveRenko_Cld.mq5

Адаптивный Ренко
Copyright: Copyright © 2010,   Svinozavr; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010,   Svinozavr', 'link': '', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 7}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 1, 6: 5, 7: 5}, 'colors': {1: [16511216], 2: [16748574], 3: [16711935], 4: [65280], 5: [255], 6: [65280], 7: [255]}, 'widths': {2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2}, 'styles': {2: 4, 3: 4, 4: 0, 5: 0}, 'labels': {1: 'AdaptiveRenko channel Cloud', 2: 'Lower AdaptiveRenko', 3: 'Upper AdaptiveRenko', 4: 'AdaptiveRenko Support', 5: 'AdaptiveRenko Resistance', 6: 'AdaptiveRenko Support Arrow', 7: 'AdaptiveRenko Resistance Arrow'}, 'levels': [], 'description': ['Адаптивный Ренко'], 'name': 'AdaptiveRenko_Cld', 'source': 'MQL5 Indicators/AdaptiveRenko_Cld_HTF/AdaptiveRenko_Cld.mq5', 'folder': 'AdaptiveRenko_Cld_HTF', 'inputs': [{'mql': 'K', 'py': 'K', 'param': 'K', 'type': 'double', 'default': 1.000001, 'label': 'множитель', 'sinput': False}, {'mql': 'Indicator', 'py': 'Indicator', 'param': 'Indicator', 'type': 'int', 'default': 0, 'label': 'индикатор для расчёта', 'sinput': False}, {'mql': 'VltPeriod', 'py': 'VltPeriod', 'param': 'VltPeriod', 'type': 'uint', 'default': 10, 'label': 'период волатильности', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'способ расчёта цены', 'sinput': False}, {'mql': 'WideMin', 'py': 'WideMin', 'param': 'WideMin', 'type': 'uint', 'default': 2, 'label': 'минимальная толщина кирпича в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum IndMode
ATR = 0
StDev = 1
_enum('IndMode', {0: 'ATR', 1: 'StDev'})

# enum PriceMode
HighLow_ = 0
Close_ = 1
_enum('PriceMode', {0: 'HighLow_', 1: 'Close_'})

# ---- inputs and global variables
K = _input('K', 1.000001)  # множитель
Indicator = _input('Indicator', ATR)  # индикатор для расчёта
VltPeriod = _input('VltPeriod', 10)  # период волатильности
Price = _input('Price', Close_)  # способ расчёта цены
WideMin = _input('WideMin', 2)  # минимальная толщина кирпича в пунктах
sens = 0.0
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnClBuffer = Arr(0, 0.0)
UpClBuffer = Arr(0, 0.0)
UpTrendBuffer = Arr(0, 0.0)
DnTrendBuffer = Arr(0, 0.0)
UpTrendArBuffer = Arr(0, 0.0)
DnTrendArBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total, sens
    min_rates_total = _int(VltPeriod)
    sens = WideMin * Point()
    if Indicator == ATR:
        Ind_Handle = iATR(None, 0, VltPeriod)
    else:
        Ind_Handle = iStdDev(None, 0, VltPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора')
    SetIndexBuffer(0, UpClBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpClBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(1, DnClBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnClBuffer, True)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(4, UpTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpTrendBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(5, DnTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnTrendBuffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(6, UpTrendArBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpTrendArBuffer, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(7, DnTrendArBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnTrendArBuffer, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, None)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'AdaptiveRenko_Cld(' + DoubleToString(K, 3) + ',' + EnumToString(Indicator, 'IndMode') + ',' + _str(VltPeriod) + ',' + EnumToString(Price, 'PriceMode') + ',' + _str(WideMin) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_Brick_, _s_OnCalculate_Dn_, _s_OnCalculate_Up_, _s_OnCalculate_trend_
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    trend = 0
    Hi = 0.0
    Lo = 0.0
    vlt = 0.0
    Brick = 0.0
    Up = 0.0
    Dn = 0.0
    IndArray = Arr(0, 0.0)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(IndArray, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        if Price == Close_:
            Hi = Close[limit]
            Lo = Hi
        else:
            Hi = High[limit]
            Lo = Low[limit]
        _s_OnCalculate_Brick_ = MathMax(K * (Hi - Lo), sens)
        _s_OnCalculate_Up_ = Hi
        _s_OnCalculate_Dn_ = Lo
        _s_OnCalculate_trend_ = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, IndArray) <= 0:
        return 0
    Up = _s_OnCalculate_Up_
    Dn = _s_OnCalculate_Dn_
    Brick = _s_OnCalculate_Brick_
    trend = _s_OnCalculate_trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if Price == Close_:
            Hi = Close[bar]
            Lo = Hi
        else:
            Hi = High[bar]
            Lo = Low[bar]
        vlt = MathMax(K * IndArray[bar], sens)
        if Hi > (Up + Brick):
            if Brick:
                Up += MathFloor(_fdiv(Hi - Up, Brick)) * Brick
            Brick = vlt
            Dn = Up - Brick
        if Lo < (Dn - Brick):
            if Brick:
                Dn -= MathFloor(_fdiv(Dn - Lo, Brick)) * Brick
            Brick = vlt
            Up = Dn + Brick
        UpClBuffer[bar] = Up
        UpBuffer[bar] = UpClBuffer[bar]
        DnClBuffer[bar] = Dn
        DnBuffer[bar] = DnClBuffer[bar]
        DnTrendArBuffer[bar] = 0.0
        UpTrendArBuffer[bar] = DnTrendArBuffer[bar]
        DnTrendBuffer[bar] = UpTrendArBuffer[bar]
        UpTrendBuffer[bar] = DnTrendBuffer[bar]
        if UpBuffer[bar + 1] < Up:
            trend = 1
        if DnBuffer[bar + 1] > Dn:
            trend = -1
        if trend > 0:
            UpTrendBuffer[bar] = Dn - Brick
            UpTrendArBuffer[bar] = UpTrendBuffer[bar]
        if trend < 0:
            DnTrendBuffer[bar] = Up + Brick
            DnTrendArBuffer[bar] = DnTrendBuffer[bar]
        if bar:
            _s_OnCalculate_Up_ = Up
            _s_OnCalculate_Dn_ = Dn
            _s_OnCalculate_Brick_ = Brick
            _s_OnCalculate_trend_ = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Brick_ = 0.0
_s_OnCalculate_Up_ = 0.0
_s_OnCalculate_Dn_ = 0.0
_s_OnCalculate_trend_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveRenkoCld(_MQL5Indicator):
    name = 'AdaptiveRenko_Cld'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'K': 1.000001,  # множитель
        'Indicator': _Choice({0: 'ATR индикатор', 1: 'StDev индикатор'}, default=0),  # индикатор для расчёта
        'VltPeriod': 10,  # период волатильности
        'Price': _Choice({0: 'High/Low', 1: 'Close'}, default=1),  # способ расчёта цены
        'WideMin': 2,  # минимальная толщина кирпича в пунктах
    }

