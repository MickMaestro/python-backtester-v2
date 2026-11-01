"""Skyscraper_Fix_Candle — converted from MQL5: MQL5 Indicators/Skyscraper_Fix_Candle/Skyscraper_Fix_Candle.mq5

Индикатор торговой системы pabloski.
Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.20', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 8421376, 2763429, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Skyscraper_Fix Open;Skyscraper_Fix High;Skyscraper_Fix Low;Skyscraper_Fix Close'}, 'levels': [], 'description': ['Индикатор торговой системы pabloski.'], 'name': 'Skyscraper_Fix_Candle', 'source': 'MQL5 Indicators/Skyscraper_Fix_Candle/Skyscraper_Fix_Candle.mq5', 'folder': 'Skyscraper_Fix_Candle', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Период ATR', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 0.9, 'label': 'Фактор чувствительности индикатора', 'sinput': False}, {'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'double', 'default': 0.0, 'label': 'Приближение средней линии к линиям экстремумов', 'sinput': False}, {'mql': 'HighLow', 'py': 'HighLow', 'param': 'HighLow', 'type': 'int', 'default': 0, 'label': 'Расчёт индикатора по High/Low или Close', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Method
MODE_HighLow = 0
MODE_Close = 1
_enum('Method', {0: 'MODE_HighLow', 1: 'MODE_Close'})

# ---- inputs and global variables
Length = _input('Length', 10)  # Период ATR
Kv = _input('Kv', 0.9)  # Фактор чувствительности индикатора
Percentage = _input('Percentage', 0.0)  # Приближение средней линии к линиям экстремумов
HighLow = _input('HighLow', MODE_HighLow)  # Расчёт индикатора по High/Low или Close
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
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
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotInit(0, 0.0, min_rates_total, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Skyscraper_Fix_Candle(' + _str(Length) + ',' + DoubleToString(Kv) + ',' + _str(HighLow) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

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
    ArraySetAsSeries(Open, True)
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
        ExtOpenBuffer[bar] = Open[bar]
        ExtHighBuffer[bar] = High[bar]
        ExtLowBuffer[bar] = Low[bar]
        ExtCloseBuffer[bar] = Close[bar]
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
            if Close[bar] >= Open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
            if bar:
                _s_OnCalculate_smax1 = DBL_MAX
        else:
            smax0 = MathMin(smax0, _s_OnCalculate_smax1)
            if Close[bar] <= Open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
            if bar:
                _s_OnCalculate_smin1 = DBL_MIN
        if bar:
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
            _s_OnCalculate_trend1 = trend0
    return rates_total

# ---- static local variables
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_trend1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SkyscraperFixCandle(_MQL5Indicator):
    name = 'Skyscraper_Fix_Candle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Период ATR
        'Kv': 0.9,  # Фактор чувствительности индикатора
        'Percentage': 0.0,  # Приближение средней линии к линиям экстремумов
        'HighLow': _Choice({0: 'High/Low', 1: 'Close'}, default=0),  # Расчёт индикатора по High/Low или Close
    }

