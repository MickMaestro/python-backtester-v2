"""Skyscraper_Fix_Cld — converted from MQL5: MQL5 Indicators/Skyscraper_Fix_Cld_HTF/Skyscraper_Fix_Cld.mq5

Индикатор торговой системы pabloski.
Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.20', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 7}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 5, 6: 5, 7: 12}, 'colors': {1: [16770815], 2: [15269855], 3: [3329330], 4: [9639167], 5: [3329330], 6: [9639167], 7: [8421376, 2237106]}, 'widths': {3: 3, 4: 3, 5: 5, 6: 5, 7: 1}, 'styles': {}, 'labels': {1: 'Upper Loss Cloud', 2: 'Lower Loss Cloud', 3: 'Upper Skyscraper', 4: 'Lower Skyscraper', 5: 'Skyscraper Buy', 6: 'Skyscraper Sell', 7: 'Skyscraper Middle'}, 'levels': [], 'description': ['Индикатор торговой системы pabloski.'], 'name': 'Skyscraper_Fix_Cld', 'source': 'MQL5 Indicators/Skyscraper_Fix_Cld_HTF/Skyscraper_Fix_Cld.mq5', 'folder': 'Skyscraper_Fix_Cld_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Период ATR', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 0.9, 'label': 'Фактор чувствительности индикатора', 'sinput': False}, {'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'double', 'default': 0.0, 'label': 'Приближение средней линии к линиям экстремумов', 'sinput': False}, {'mql': 'HighLow', 'py': 'HighLow', 'param': 'HighLow', 'type': 'int', 'default': 0, 'label': 'Расчёт индикатора по High/Low или Close', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Method
MODE_HighLow = 0
MODE_Close = 1
_enum('Method', {0: 'MODE_HighLow', 1: 'MODE_Close'})

# ---- inputs and global variables
Length = _input('Length', 10)  # Период ATR
Kv = _input('Kv', 0.9)  # Фактор чувствительности индикатора
Percentage = _input('Percentage', 0.0)  # Приближение средней линии к линиям экстремумов
HighLow = _input('HighLow', MODE_HighLow)  # Расчёт индикатора по High/Low или Close
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = ATR_Period + _int(Length + 1)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, UpUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpUpBuffer, True)
    SetIndexBuffer(1, UpDnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpDnBuffer, True)
    SetIndexBuffer(2, DnUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnUpBuffer, True)
    SetIndexBuffer(3, DnDnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnDnBuffer, True)
    SetIndexBuffer(4, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(5, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(6, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 172)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(7, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 172)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(8, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_ARROW, 172)
    ArraySetAsSeries(LineBuffer, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(9, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorLineBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Skyscraper_Fix_Cld(' + _str(Length) + ',' + DoubleToString(Kv) + ',' + _str(HighLow) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_trend1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    trend0 = 0
    Step = 0
    to_copy = 0
    ATR = Arr(0, 0.0)
    smin0 = 0.0
    smax0 = 0.0
    ATRmin = 0.0
    ATRmax = 0.0
    xStep = 0.0
    x2Step = 0.0
    Line = 0.0
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_smin1 = Close[limit]
        _s_OnCalculate_smax1 = Close[limit]
        _s_OnCalculate_trend1 = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1 + _int(Length)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        DnBuffer[bar] = 0.0
        UpBuffer[bar] = DnBuffer[bar]
        trend0 = _s_OnCalculate_trend1
        ATRmax = ATR[ArrayMaximum(ATR, bar, Length)]
        ATRmin = ATR[ArrayMinimum(ATR, bar, Length)]
        Step = _int(_fdiv(0.5 * Kv * (ATRmax + ATRmin), Point()))
        xStep = Step * Point()
        x2Step = 2.0 * xStep
        if HighLow == MODE_HighLow:
            smax0 = Low[bar] + x2Step
            smin0 = High[bar] - x2Step
        else:
            smax0 = Close[bar] + x2Step
            smin0 = Close[bar] - x2Step
        if Close[bar] > _s_OnCalculate_smax1:
            trend0 = 1
        if Close[bar] < _s_OnCalculate_smin1:
            trend0 = -1
        if trend0 > 0:
            smin0 = MathMax(smin0, _s_OnCalculate_smin1)
            UpBuffer[bar] = smin0
            Line = smin0 + (Step * Point())
            LineBuffer[bar] = MathMax(Line - ((Percentage / 100.0) * Step * Point()), LineBuffer[bar + 1])
            ColorLineBuffer[bar] = 0.0
            if bar:
                _s_OnCalculate_smax1 = DBL_MAX
            UpUpBuffer[bar] = LineBuffer[bar]
            UpDnBuffer[bar] = UpBuffer[bar]
            DnUpBuffer[bar] = 0.0
            DnDnBuffer[bar] = 0.0
        else:
            smax0 = MathMin(smax0, _s_OnCalculate_smax1)
            DnBuffer[bar] = smax0
            Line = smax0 - (Step * Point())
            LineBuffer[bar] = MathMin(Line + ((Percentage / 100.0) * Step * Point()), LineBuffer[bar + 1])
            ColorLineBuffer[bar] = 1.0
            if bar:
                _s_OnCalculate_smin1 = DBL_MIN
            UpUpBuffer[bar] = 0.0
            UpDnBuffer[bar] = 0.0
            DnUpBuffer[bar] = DnBuffer[bar]
            DnDnBuffer[bar] = LineBuffer[bar]
        if bar:
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
            _s_OnCalculate_trend1 = trend0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    for bar in range(limit, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = SellBuffer[bar]
        if UpBuffer[bar + 1] and DnBuffer[bar]:
            SellBuffer[bar] = DnBuffer[bar]
        if DnBuffer[bar + 1] and UpBuffer[bar]:
            BuyBuffer[bar] = UpBuffer[bar]
    return rates_total

# ---- static local variables
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_trend1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SkyscraperFixCld(_MQL5Indicator):
    name = 'Skyscraper_Fix_Cld'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Период ATR
        'Kv': 0.9,  # Фактор чувствительности индикатора
        'Percentage': 0.0,  # Приближение средней линии к линиям экстремумов
        'HighLow': _Choice({0: 'High/Low', 1: 'Close'}, default=0),  # Расчёт индикатора по High/Low или Close
    }

