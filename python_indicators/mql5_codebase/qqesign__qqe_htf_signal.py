"""qqesign — converted from MQL5: MQL5 Indicators/QQE_HTF_Signal/qqesign.mq5

QQE - Qualitative Quantitative Estimation.
Calculated as two indicators:
1) MA on RSI
2) Difference of MA on RSI and MA of MA of ATR of MA of RSI
The signal for buy is when blue line crosses level 50 from below
after crossing the yellow line from below.
The signal for sell is when blue line crosses level 50 from above
after crossing the yellow line from above.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'QQESign Sell', 2: 'QQESign Buy'}, 'levels': [], 'description': ['QQE - Qualitative Quantitative Estimation.', 'Calculated as two indicators:', '1) MA on RSI', '2) Difference of MA on RSI and MA of MA of ATR of MA of RSI', 'The signal for buy is when blue line crosses level 50 from below', 'after crossing the yellow line from below.', 'The signal for sell is when blue line crosses level 50 from above', 'after crossing the yellow line from above.'], 'name': 'qqesign', 'source': 'MQL5 Indicators/QQE_HTF_Signal/qqesign.mq5', 'folder': 'QQE_HTF_Signal', 'inputs': [{'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'uint', 'default': 123, 'label': '', 'sinput': False}, {'mql': 'SF', 'py': 'SF', 'param': 'SF', 'type': 'uint', 'default': 41, 'label': '', 'sinput': False}, {'mql': 'DARFACTOR', 'py': 'DARFACTOR', 'param': 'DARFACTOR', 'type': 'double', 'default': 4.236, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSI_Period = _input('RSI_Period', 123)
SF = _input('SF', 41)
DARFACTOR = _input('DARFACTOR', 4.236)
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
RSI_Handle = 0
ATR_Handle = 0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
Wilders_Period = 0

def OnInit():
    global ATR_Handle, RSI_Handle, Wilders_Period, min_rates_1, min_rates_2, min_rates_3, min_rates_total
    Wilders_Period = _int((RSI_Period * 2) - 1)
    min_rates_1 = _int(RSI_Period + 1)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, SF, XPhase) + 1
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, Wilders_Period, XPhase)
    min_rates_total = min_rates_3 + XMA1.GetStartBars(XMA_Method, Wilders_Period, XPhase)
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_total) + 1
    RSI_Handle = iRSI(None, 0, RSI_Period, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора RSI')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 93)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 93)
    shortname = 'Qualitative Quantitative Estimation Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_tr, _s_OnCalculate_prev_xrsi
    if (BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    RSI = Arr(1, 0.0, dyn=False)
    ATR = Arr(1, 0.0, dyn=False)
    xrsi = 0.0
    momxrsi = 0.0
    xmomxrsi = 0.0
    xxmomxrsi = 0.0
    dar = 0.0
    tr = 0.0
    dv = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
        _s_OnCalculate_prev_xrsi = 50.0
        _s_OnCalculate_prev_tr = 50.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if CopyBuffer(RSI_Handle, 0, rates_total - 1 - bar, 1, RSI) <= 0:
            return 0
        xrsi = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, SF, RSI[0], bar, False)
        momxrsi = MathAbs(_s_OnCalculate_prev_xrsi - xrsi)
        xmomxrsi = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, Wilders_Period, momxrsi, bar, False)
        xxmomxrsi = XMA3.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, Wilders_Period, xmomxrsi, bar, False)
        dar = xxmomxrsi * DARFACTOR
        tr = _s_OnCalculate_prev_tr
        dv = tr
        if xrsi < tr:
            tr = xrsi + dar
            if _s_OnCalculate_prev_xrsi < dv and tr > dv:
                tr = dv
        elif xrsi > tr:
            tr = xrsi - dar
            if _s_OnCalculate_prev_xrsi > dv and tr < dv:
                tr = dv
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_prev_xrsi <= _s_OnCalculate_prev_tr and xrsi > tr:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_prev_xrsi >= _s_OnCalculate_prev_tr and xrsi < tr:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_prev_xrsi = xrsi
            _s_OnCalculate_prev_tr = tr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()

# ---- static local variables
_s_OnCalculate_prev_xrsi = 0.0
_s_OnCalculate_prev_tr = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Qqesign(_MQL5Indicator):
    name = 'qqesign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI_Period': 123,
        'SF': 41,
        'DARFACTOR': 4.236,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XPhase': 15,  # Параметр сглаживания
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

