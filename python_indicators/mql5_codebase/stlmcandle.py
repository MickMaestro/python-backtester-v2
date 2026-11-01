"""STLMCandle — converted from MQL5: MQL5 Indicators/STLMCandle/STLMCandle.mq5

Индикатор ColorSTLM в свечном виде
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [36095, 8421504, 13749760]}, 'widths': {}, 'styles': {}, 'labels': {1: 'STLMCandle Open;High;Low;Close'}, 'levels': [0.0], 'description': ['Индикатор ColorSTLM в свечном виде'], 'name': 'STLMCandle', 'source': 'MQL5 Indicators/STLMCandle/STLMCandle.mq5', 'folder': 'STLMCandle', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
JLength = _input('JLength', 5)  # глубина сглаживания
JPhase = _input('JPhase', 100)  # параметр сглаживания,
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    STLMPeriod = 91
    min_rates_total = STLMPeriod + 1 + 30
    Ind_Handle[0] = iCustom(None, 0, 'ColorSTLM_HISTOGRAM', JLength, JPhase, PRICE_OPEN, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorSTLM_HISTOGRAM[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'ColorSTLM_HISTOGRAM', JLength, JPhase, PRICE_HIGH, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorSTLM_HISTOGRAM[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'ColorSTLM_HISTOGRAM', JLength, JPhase, PRICE_LOW, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorSTLM_HISTOGRAM[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'ColorSTLM_HISTOGRAM', JLength, JPhase, PRICE_CLOSE, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorSTLM_HISTOGRAM[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ColorSTLMCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class STLMCandle(_MQL5Indicator):
    name = 'STLMCandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 5,  # глубина сглаживания
        'JPhase': 100,  # параметр сглаживания,
    }

