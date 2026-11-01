"""Candle_shadow_percent — converted from MQL5: MQL5 Indicators/Candle shadow percent/Candle_shadow_percent.mq5

Индикатор поиска свечей с заданным соотношением размера тела и тени
Найденные свечи отмечаются символами из набора Wingdings
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Top', 2: 'Lower'}, 'levels': [], 'description': ['Индикатор поиска свечей с заданным соотношением размера тела и тени', 'Найденные свечи отмечаются символами из набора Wingdings'], 'name': 'Candle_shadow_percent', 'source': 'MQL5 Indicators/Candle shadow percent/Candle_shadow_percent.mq5', 'folder': 'Candle shadow percent', 'inputs': [{'mql': '__1__', 'py': '__1__', 'param': None, 'type': 'string', 'default': '', 'label': 'Параметр тела свечи', 'sinput': True}, {'mql': 'min_size_candel', 'py': 'min_size_candel', 'param': 'min_size_candel', 'type': 'ushort', 'default': 50, 'label': 'Минимальный размер тела свечи', 'sinput': False}, {'mql': '__2__', 'py': '__2__', 'param': None, 'type': 'string', 'default': '', 'label': 'Параметры верхней тени', 'sinput': True}, {'mql': 'IsTopShadow', 'py': 'IsTopShadow', 'param': 'IsTopShadow', 'type': 'bool', 'default': True, 'label': 'true -> отображать свечи по верхней тени', 'sinput': False}, {'mql': 'percent_top', 'py': 'percent_top', 'param': 'percent_top', 'type': 'ushort', 'default': 30, 'label': 'Размер верхней тени (в процентах от тела)', 'sinput': False}, {'mql': 'top_min_or_max', 'py': 'top_min_or_max', 'param': 'top_min_or_max', 'type': 'bool', 'default': True, 'label': 'true -> мин. размер, false -> макс. размер', 'sinput': False}, {'mql': 'top_shadow_code', 'py': 'top_shadow_code', 'param': 'top_shadow_code', 'type': 'ushort', 'default': 226, 'label': 'Код символа (32-255)', 'sinput': False}, {'mql': '__3__', 'py': '__3__', 'param': None, 'type': 'string', 'default': '', 'label': 'Параметры низа свечи', 'sinput': True}, {'mql': 'IsLowerShadow', 'py': 'IsLowerShadow', 'param': 'IsLowerShadow', 'type': 'bool', 'default': True, 'label': 'true -> отображать свечи по нижней тени', 'sinput': False}, {'mql': 'percent_lower', 'py': 'percent_lower', 'param': 'percent_lower', 'type': 'ushort', 'default': 80, 'label': 'Размер нижней тени (в процентах от тела)', 'sinput': False}, {'mql': 'lower_min_or_max', 'py': 'lower_min_or_max', 'param': 'lower_min_or_max', 'type': 'bool', 'default': True, 'label': 'true -> мин. размер, false -> макс. размер', 'sinput': False}, {'mql': 'lower_shadow_code', 'py': 'lower_shadow_code', 'param': 'lower_shadow_code', 'type': 'ushort', 'default': 225, 'label': 'Код символа (32-255)', 'sinput': False}, {'mql': '__4__', 'py': '__4__', 'param': None, 'type': 'string', 'default': '', 'label': 'Параметр смещения', 'sinput': True}, {'mql': 'vertical_shift', 'py': 'vertical_shift', 'param': 'vertical_shift', 'type': 'uchar', 'default': 15, 'label': 'Смещение стрелок по вертикали (0-255)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
__1__ = _input('__1__', '')  # Параметр тела свечи
min_size_candel = _input('min_size_candel', 50)  # Минимальный размер тела свечи
__2__ = _input('__2__', '')  # Параметры верхней тени
IsTopShadow = _input('IsTopShadow', True)  # true -> отображать свечи по верхней тени
percent_top = _input('percent_top', 30)  # Размер верхней тени (в процентах от тела)
top_min_or_max = _input('top_min_or_max', True)  # true -> мин. размер, false -> макс. размер
top_shadow_code = _input('top_shadow_code', 226)  # Код символа (32-255)
__3__ = _input('__3__', '')  # Параметры низа свечи
IsLowerShadow = _input('IsLowerShadow', True)  # true -> отображать свечи по нижней тени
percent_lower = _input('percent_lower', 80)  # Размер нижней тени (в процентах от тела)
lower_min_or_max = _input('lower_min_or_max', True)  # true -> мин. размер, false -> макс. размер
lower_shadow_code = _input('lower_shadow_code', 225)  # Код символа (32-255)
__4__ = _input('__4__', '')  # Параметр смещения
vertical_shift = _input('vertical_shift', 15)  # Смещение стрелок по вертикали (0-255)
BufferTop = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)

def OnInit():
    if (not IsTopShadow) and (not IsLowerShadow):
        Print('Оба параметра "отображать свечи по верхней/нижней тени" равны false')
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLower, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, top_shadow_code)
    PlotIndexSetInteger(1, PLOT_ARROW, lower_shadow_code)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -vertical_shift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, vertical_shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_time
    if _s_OnCalculate_prev_time == time[rates_total - 1]:
        return rates_total
    _s_OnCalculate_prev_time = time[rates_total - 1]
    start = 1
    if prev_calculated > 0:
        start = prev_calculated
    for i in range(start, rates_total):
        size = _fdiv(MathAbs(open[i - 1] - close[i - 1]), Point())
        if size > min_size_candel:
            if IsTopShadow:
                size_shadow_top = ((high[1] - close[i - 1]) if (open[i - 1] < close[i - 1]) else (high[i - 1] - open[i - 1]))
                if top_min_or_max:
                    if ((size * percent_top) / 100.0) < _fdiv(size_shadow_top, Point()):
                        BufferTop[i - 1] = high[i - 1]
                else:
                    if ((size * percent_top) / 100.0) > _fdiv(size_shadow_top, Point()):
                        BufferTop[i - 1] = high[i - 1]
            if IsLowerShadow:
                size_shadow_lower = ((open[1] - low[i - 1]) if (open[i - 1] < close[i - 1]) else (close[i - 1] - low[i - 1]))
                if lower_min_or_max:
                    if ((size * percent_lower) / 100.0) < _fdiv(size_shadow_lower, Point()):
                        BufferLower[i - 1] = low[i - 1]
                else:
                    if ((size * percent_lower) / 100.0) > _fdiv(size_shadow_lower, Point()):
                        BufferLower[i - 1] = low[i - 1]
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleShadowPercent(_MQL5Indicator):
    name = 'Candle_shadow_percent'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'min_size_candel': 50,  # Минимальный размер тела свечи
        'IsTopShadow': True,  # true -> отображать свечи по верхней тени
        'percent_top': 30,  # Размер верхней тени (в процентах от тела)
        'top_min_or_max': True,  # true -> мин. размер, false -> макс. размер
        'top_shadow_code': 226,  # Код символа (32-255)
        'IsLowerShadow': True,  # true -> отображать свечи по нижней тени
        'percent_lower': 80,  # Размер нижней тени (в процентах от тела)
        'lower_min_or_max': True,  # true -> мин. размер, false -> макс. размер
        'lower_shadow_code': 225,  # Код символа (32-255)
        'vertical_shift': 15,  # Смещение стрелок по вертикали (0-255)
    }

