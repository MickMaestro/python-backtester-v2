"""j2jmasign — converted from MQL5: MQL5 Indicators/J2JMASign/j2jmasign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'J2JMA Sell', 2: 'J2JMA Buy'}, 'levels': [], 'description': [], 'name': 'j2jmasign', 'source': 'MQL5 Indicators/J2JMASign/j2jmasign.mq5', 'folder': 'J2JMASign', 'inputs': [{'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'double', 'default': 5.0, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'double', 'default': 5.0, 'label': 'Глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'double', 'default': 100.0, 'label': 'Параметр первого сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'double', 'default': 100.0, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Length1 = _input('Length1', 5.0)  # Глубина  первого сглаживания
Length2 = _input('Length2', 5.0)  # Глубина  второго сглаживания
Phase1 = _input('Phase1', 100.0)  # Параметр первого сглаживания
Phase2 = _input('Phase2', 100.0)  # Параметр второго сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_, min_rates_total
    min_rates_ = 30
    min_rates_total = min_rates_ + 31 + 3
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_total)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    shortname = Box("")
    StringConcatenate(shortname, 'J2JMA( Length1 = ', Length1, ', Length2 = ', Length2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length1', _int(Length1))
    JMA.JJMALengthCheck('Length2', _int(Length2))
    JMA.JJMAPhaseCheck('Phase1', _int(Phase1))
    JMA.JJMAPhaseCheck('Phase2', _int(Phase2))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_j2jma1, _s_OnCalculate_j2jma2
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    j1jma = 0.0
    j2jma = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        j1jma = _s_OnCalculate_JMA1.JJMASeries(0, prev_calculated, rates_total, 0, Phase1, Length1, price, bar, False)
        j2jma = _s_OnCalculate_JMA2.JJMASeries(min_rates_, prev_calculated, rates_total, 0, Phase2, Length2, j1jma, bar, False)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_j2jma2 >= _s_OnCalculate_j2jma1 and _s_OnCalculate_j2jma1 < j2jma:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_j2jma2 <= _s_OnCalculate_j2jma1 and _s_OnCalculate_j2jma1 > j2jma:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_j2jma2 = _s_OnCalculate_j2jma1
            _s_OnCalculate_j2jma1 = j2jma
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_j2jma1 = 0.0
_s_OnCalculate_j2jma2 = 0.0
_s_OnCalculate_JMA1 = CJJMA()
_s_OnCalculate_JMA2 = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class J2jmasign(_MQL5Indicator):
    name = 'j2jmasign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length1': 5.0,  # Глубина  первого сглаживания
        'Length2': 5.0,  # Глубина  второго сглаживания
        'Phase1': 100.0,  # Параметр первого сглаживания
        'Phase2': 100.0,  # Параметр второго сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
    }

