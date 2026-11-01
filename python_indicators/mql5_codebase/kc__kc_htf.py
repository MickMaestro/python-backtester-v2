"""kc — converted from MQL5: MQL5 Indicators/KC_HTF/kc.mq5

ATR channel
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [14822282], 2: [255], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 4, 2: 4, 3: 4}, 'labels': {1: 'MA', 2: '+ATR', 3: '-ATR'}, 'levels': [], 'description': ['ATR channel'], 'name': 'kc', 'source': 'MQL5 Indicators/KC_HTF/kc.mq5', 'folder': 'KC_HTF', 'inputs': [{'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения MA', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 20, 'label': 'Период MA', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 20, 'label': 'Период ATR', 'sinput': False}, {'mql': 'Factor', 'py': 'Factor', 'param': 'Factor', 'type': 'double', 'default': 1.5, 'label': 'Девиация канала', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Method = _input('MA_Method', MODE_SMA)  # Метод усреднения MA
MA_Period = _input('MA_Period', 20)  # Период MA
ATR_Period = _input('ATR_Period', 20)  # Период ATR
Factor = _input('Factor', 1.5)  # Девиация канала
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
MA_Buffer = Arr(0, 0.0)
UpATRBuffer = Arr(0, 0.0)
DnATRBuffer = Arr(0, 0.0)
MA_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, MA_Handle, min_rates_total
    min_rates_total = _int(MathMax(MA_Period, ATR_Period))
    MA_Handle = iMA(None, 0, MA_Period, 0, MA_Method, IPC)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора MA')
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, MA_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(MA_Buffer, True)
    SetIndexBuffer(1, UpATRBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnATRBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpATRBuffer, True)
    ArraySetAsSeries(DnATRBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR channel')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    ATR = Arr(0, 0.0)
    atr = 0.0
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA_Buffer) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        atr = Factor * ATR[bar]
        UpATRBuffer[bar] = MA_Buffer[bar] + atr
        DnATRBuffer[bar] = MA_Buffer[bar] - atr
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kc(_MQL5Indicator):
    name = 'kc'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Метод усреднения MA
        'MA_Period': 20,  # Период MA
        'ATR_Period': 20,  # Период ATR
        'Factor': 1.5,  # Девиация канала
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

