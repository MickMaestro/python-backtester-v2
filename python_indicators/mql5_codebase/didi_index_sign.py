"""didi_index_sign — converted from MQL5: MQL5 Indicators/Didi_Index_Sign/didi_index_sign.mq5

Copyright: Copyright © 2016, Rudinei Felipetto; Link: http://www.conttinua.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Rudinei Felipetto', 'link': 'http://www.conttinua.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Didi_Index Sell', 2: 'Didi_Index Buy'}, 'levels': [], 'description': [], 'name': 'didi_index_sign', 'source': 'MQL5 Indicators/Didi_Index_Sign/didi_index_sign.mq5', 'folder': 'Didi_Index_Sign', 'inputs': [{'mql': 'Curta', 'py': 'Curta', 'param': 'Curta', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Longa', 'py': 'Longa', 'param': 'Longa', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Curta = _input('Curta', 3)
Longa = _input('Longa', 20)
MA_Method = _input('MA_Method', MODE_SMA)  # Метод усреднения индикатора
MA_Price = _input('MA_Price', PRICE_CLOSE)  # Ценовая константа
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
K = 0
C_Handle = 0
L_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, C_Handle, L_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(Curta, Longa))
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    C_Handle = iMA(None, 0, Curta, 0, MA_Method, MA_Price)
    if C_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA Curta')
        return INIT_FAILED
    L_Handle = iMA(None, 0, Longa, 0, MA_Method, MA_Price)
    if L_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA Longa')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 170)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 170)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Didi_Index_Sig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_trend
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(C_Handle) < rates_total) or BarsCalculated(L_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    trend = 0.0
    Cur = Arr(0, 0.0)
    Lon = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_prev_trend = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(C_Handle, 0, 0, to_copy, Cur) <= 0:
        return 0
    if CopyBuffer(L_Handle, 0, 0, to_copy, Lon) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(Cur, True)
    ArraySetAsSeries(Lon, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        trend = Cur[bar] - Lon[bar]
        if not trend:
            trend = _s_OnCalculate_prev_trend
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_prev_trend < 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_prev_trend > 0 and trend < 0:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_prev_trend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_trend = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DidiIndexSign(_MQL5Indicator):
    name = 'didi_index_sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Curta': 3,
        'Longa': 20,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Метод усреднения индикатора
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
    }

