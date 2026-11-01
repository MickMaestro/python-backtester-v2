"""mi_fractal — converted from MQL5: MQL5 Indicators/MI_Fractal/mi_fractal.mq5

Фракталы с возможностью выбора количества свеч по бокам
Copyright: Copyright © 2009 Орешкин А.В.; Link: http://www.vk.com/mtforex; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009 Орешкин А.В.', 'link': 'http://www.vk.com/mtforex', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [7451452], 2: [4678655]}, 'widths': {1: 3, 2: 3}, 'styles': {}, 'labels': {1: 'Up MI_Fractal', 2: 'Down MI_Fractal'}, 'levels': [], 'description': ['Фракталы с возможностью выбора количества свеч по бокам'], 'name': 'mi_fractal', 'source': 'MQL5 Indicators/MI_Fractal/mi_fractal.mq5', 'folder': 'MI_Fractal', 'inputs': [{'mql': 'LeftCount', 'py': 'LeftCount', 'param': 'LeftCount', 'type': 'uint', 'default': 10, 'label': 'Количество свечей слева', 'sinput': False}, {'mql': 'RightCount', 'py': 'RightCount', 'param': 'RightCount', 'type': 'uint', 'default': 2, 'label': 'Количество свечей справа', 'sinput': False}, {'mql': 'MinDiff', 'py': 'MinDiff', 'param': 'MinDiff', 'type': 'uint', 'default': 10, 'label': 'Минимально допустимое расстояние от экстремумов до пиков', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 217, 'label': 'Метка верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 218, 'label': 'Метка нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LeftCount = _input('LeftCount', 10)  # Количество свечей слева
RightCount = _input('RightCount', 2)  # Количество свечей справа
MinDiff = _input('MinDiff', 10)  # Минимально допустимое расстояние от экстремумов до пиков
UpLable = _input('UpLable', 217)  # Метка верхнего фрактала
DnLable = _input('DnLable', 218)  # Метка нижнего фрактала
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
dMinDiff = 0.0
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, dMinDiff, min_rates_total
    dMinDiff = MinDiff * Point()
    ATR_Period = 10
    min_rates_total = _int(MathMax(ATR_Period, LeftCount + RightCount))
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'MI_Fractal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + 2
    to_copy = limit + min_rates_total
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    for bar in range(limit, 0 - 1, -1):
        UP_Fractal = True
        DOWN_Fractal = True
        for index in range(bar + _int(LeftCount), bar - _int(RightCount) - 1, -1):
            if index == bar:
                continue
            if (high[bar] - high[index]) < dMinDiff:
                UP_Fractal = False
            if (low[index] - low[bar]) < dMinDiff:
                DOWN_Fractal = False
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        if UP_Fractal and (not DOWN_Fractal):
            UpBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if (not UP_Fractal) and DOWN_Fractal:
            DnBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MiFractal(_MQL5Indicator):
    name = 'mi_fractal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LeftCount': 10,  # Количество свечей слева
        'RightCount': 2,  # Количество свечей справа
        'MinDiff': 10,  # Минимально допустимое расстояние от экстремумов до пиков
        'UpLable': 217,  # Метка верхнего фрактала
        'DnLable': 218,  # Метка нижнего фрактала
    }

