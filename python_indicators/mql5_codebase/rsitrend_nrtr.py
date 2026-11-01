"""RSITrend_NRTR — converted from MQL5: MQL5 Indicators/RSITrend_NRTR/RSITrend_NRTR.mq5

Copyright: Ramdass - Conversion only; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Ramdass - Conversion only', 'link': '', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [16760576], 2: [16711935], 3: [16711680], 4: [13828244], 5: [3329330], 6: [255]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 5, 6: 5}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'NRTR Line Up', 2: 'NRTR Line Down', 3: 'NRTR Up', 4: 'NRTR Down', 5: 'Buy RSITrend signal', 6: 'Sell RSITrend signal'}, 'levels': [], 'description': [], 'name': 'RSITrend_NRTR', 'source': 'MQL5 Indicators/RSITrend_NRTR/RSITrend_NRTR.mq5', 'folder': 'RSITrend_NRTR', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'AtrRatio', 'py': 'AtrRatio', 'param': 'AtrRatio', 'type': 'double', 'default': 0.375, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RISK = _input('RISK', 2)
SSP = _input('SSP', 9)
AtrRatio = _input('AtrRatio', 0.375)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
K = 0
RSI_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, K, RSI_Handle, min_rates_total
    K = 33 - _int(RISK)
    ATR_Period = 15
    min_rates_total = _int(MathMax(SSP, ATR_Period)) + 1
    RSI_Handle = iRSI(None, 0, SSP, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer1, True)
    SetIndexBuffer(1, DnBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer1, True)
    SetIndexBuffer(2, UpBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer2, True)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer2, True)
    SetIndexBuffer(4, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 175)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(5, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 175)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(SellBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RSITrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_oldtrend
    if (BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    trend = 0
    RSI = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    range_ = 0.0
    stop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_oldtrend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DnBuffer2[bar] = 0.0
        UpBuffer2[bar] = DnBuffer2[bar]
        DnBuffer1[bar] = UpBuffer2[bar]
        UpBuffer1[bar] = DnBuffer1[bar]
        SellBuffer[bar] = UpBuffer1[bar]
        BuyBuffer[bar] = SellBuffer[bar]
        trend = _s_OnCalculate_oldtrend
        if RSI[bar] < K:
            trend = -1
        if RSI[bar] > (100 - K):
            trend = 1
        range_ = AtrRatio * ATR[bar]
        if _s_OnCalculate_oldtrend < 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - range_
        if _s_OnCalculate_oldtrend > 0 and trend < 0:
            SellBuffer[bar] = high[bar] + range_
        if trend > 0:
            if BuyBuffer[bar]:
                UpBuffer2[bar] = BuyBuffer[bar]
                UpBuffer1[bar] = UpBuffer2[bar]
                DnBuffer1[bar] = DnBuffer1[bar + 1]
            else:
                stop = low[bar] - range_
                if stop < UpBuffer1[bar + 1]:
                    stop = UpBuffer1[bar + 1]
                UpBuffer2[bar] = stop
                UpBuffer1[bar] = UpBuffer2[bar]
        if trend < 0:
            if SellBuffer[bar]:
                DnBuffer2[bar] = SellBuffer[bar]
                DnBuffer1[bar] = DnBuffer2[bar]
                UpBuffer1[bar] = UpBuffer1[bar + 1]
            else:
                stop = high[bar] + range_
                if stop > DnBuffer1[bar + 1]:
                    stop = DnBuffer1[bar + 1]
                DnBuffer2[bar] = stop
                DnBuffer1[bar] = DnBuffer2[bar]
        if bar:
            _s_OnCalculate_oldtrend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_oldtrend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSITrendNRTR(_MQL5Indicator):
    name = 'RSITrend_NRTR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 2,
        'SSP': 9,
        'AtrRatio': 0.375,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

