"""StodivCandle — converted from MQL5: MQL5 Indicators/StodivCandle/StodivCandle.mq5

Индикатор окрашивает свечи на основе Стохастика
Copyright: Copyright © 2006, RickD; Link: http://e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, RickD', 'link': 'http://e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 8388736, 8421504, 8421376, 65280]}, 'widths': {}, 'styles': {}, 'labels': {1: 'StodivCandle Open;StodivCandle High;StodivCandle Low;StodivCandle Close'}, 'levels': [], 'description': ['Индикатор окрашивает свечи на основе Стохастика'], 'name': 'StodivCandle', 'source': 'MQL5 Indicators/StodivCandle/StodivCandle.mq5', 'folder': 'StodivCandle', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
HighLevel = _input('HighLevel', 60)  # уровень перезакупа
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Stochastic_Handle = 0

def OnInit():
    global Stochastic_Handle, min_rates_total
    min_rates_total = KPeriod + DPeriod + Slowing
    Stochastic_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
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
    short_name = 'StodivCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Stochastic_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    Sto = Arr(0, 0.0)
    Sign = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Stochastic_Handle, MAIN_LINE, 0, to_copy, Sto) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle, SIGNAL_LINE, 0, to_copy, Sign) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    ArraySetAsSeries(Sto, True)
    ArraySetAsSeries(Sign, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if Sto[bar] > HighLevel:
            clr = 4
        elif Sto[bar] < LowLevel:
            clr = 0
        elif Sto[bar] > Sign[bar]:
            clr = 3
        elif Sto[bar] < Sign[bar]:
            clr = 1
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StodivCandle(_MQL5Indicator):
    name = 'StodivCandle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'HighLevel': 60,  # уровень перезакупа
        'LowLevel': 40,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

